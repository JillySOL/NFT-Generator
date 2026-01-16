import os
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

from PIL import Image

from src.common.validate import validate_config
from src.utils.calc import calculate_possible_combinations
from src.utils.io import read_json, write_file, write_json
from src.utils.logger import get_logger, get_progress_bar
from src.utils.random import seeded_weighted_selection


class Generator:
    def __init__(self, **args):
        # set verbosity level and initialize logger
        self.logger = get_logger(args["verbose"])

        if args["command"] in ["generate", "validate"]:
            if not args["config"]:
                raise ValueError("No configuration file was provided.")
            elif not args["config"].endswith(".json"):
                raise ValueError(
                    "Invalid configuration file '{}'".format(args["config"])
                )

            if not args["amount"]:
                raise ValueError("No amount was provided.")
            elif not args["amount"].isnumeric():
                raise ValueError("Invalid amount '{}'".format(args["amount"]))
            self.amount = int(args["amount"])
            self.no_pad = args["no_pad"]
            self.pad_amount = 0 if self.no_pad else len(str(self.amount))

            # read configuration and validate it
            self.logger.debug("Loading configuration from '%s'", args["config"])
            self.config = read_json(args["config"])
            self.logger.debug("Validating configuration")
            validate_config(self.config)

        # set arguments
        self.seed = (
            int(args["seed"])
            if args["seed"] is not None
            else int.from_bytes(random.randbytes(16), byteorder="little")
        )
        self.start_at = int(args["start_at"])
        self.output = args["output"]
        self.allow_duplicates = args["allow_duplicates"]
        self.image_path = args["image_path"]

        # initialize state
        self.nonce = 0
        self.all_genomes = []
        self.all_combinations = []
        
        # initialize quota tracking if quotas are specified
        if "quotas" in self.config:
            self.quotas = {q["background"]: {} for q in self.config["quotas"]}
            for quota in self.config["quotas"]:
                self.quotas[quota["background"]][quota["shirt"]] = {
                    "target": quota["amount"],
                    "generated": 0
                }
            self.use_quotas = True
        else:
            self.use_quotas = False
            self.quotas = None

    def __tomlify(self) -> str:
        """
        Converts a dictionary to TOML format.
        """
        toml = ""
        obj = {
            "amount": self.amount,
            "seed": self.seed,
            "start_at": self.start_at,
            "output": self.output,
            "allow_duplicates": self.allow_duplicates,
            "no_pad": self.no_pad,
        }
        for key, value in obj.items():
            if isinstance(value, dict):
                toml += "[{}]\n".format(key)
                toml += self.__tomlify(value)
            else:
                toml += "{} = {}\n".format(key, value)
        return toml

    def __build_genome_metadata(self, token_id: int = 0, forced_traits: dict = None):
        """
        Builds the generation / NFT metadata for a single NFT.
        
        :param token_id: The token ID for this NFT
        :param forced_traits: Optional dict of forced trait values (for quota-based generation)
        """

        genome_traits = {}

        # select traits for each layer
        for layer in self.config["layers"]:
            if forced_traits and layer["name"] in forced_traits:
                # Use forced trait value (for quota-based generation)
                genome_traits[layer["name"]] = forced_traits[layer["name"]]
            else:
                # Use weighted random selection
                trait_values_and_weights = list(zip(layer["values"], layer["weights"]))
                genome_traits[layer["name"]] = seeded_weighted_selection(
                    trait_values_and_weights, seed=self.seed, nonce=self.nonce
                )
                self.nonce += 1

        # check for incompatibilities
        for incompatibility in self.config["incompatibilities"]:
            for trait in genome_traits:
                if (
                    genome_traits[incompatibility["layer"]] == incompatibility["value"]
                    and genome_traits[trait] in incompatibility["incompatible_with"]
                ):
                    # if a default incompatibility value is set, use it instead
                    if "default" in incompatibility:
                        genome_traits[trait] = incompatibility["default"]["value"]
                    else:
                        return self.__build_genome_metadata(token_id)

        if genome_traits in self.all_combinations and not self.allow_duplicates:
            return self.__build_genome_metadata(token_id)
        else:
            self.all_combinations.append(genome_traits)
            metadata = {
                "token_id": token_id,
                "image": "{}/images/{}.png".format(self.output, token_id),
                "name": self.config["name"] + str(token_id).zfill(self.pad_amount),
                "description": self.config["description"],
                "attributes": [
                    {
                        "trait_type": layer["name"],
                        "value": genome_traits[layer["name"]],
                    }
                    for layer in self.config["layers"]
                ],
            }
            
            # Add symbol if specified in config
            if "symbol" in self.config:
                metadata["symbol"] = self.config["symbol"]
            
            self.all_genomes.append(metadata)

    def __build_genome_image(self, metadata: dict):
        """
        Builds the NFT image for a single NFT.
        """
        layers = []
        try:
            for index, attr in enumerate(metadata["attributes"]):
                # get the image for the trait
                for i, trait in enumerate(self.config["layers"][index]["values"]):
                    if trait == attr["value"]:
                        layers.append(
                            Image.open(
                                f'{self.config["layers"][index]["trait_path"]}/{self.config["layers"][index]["filename"][i]}.png'
                            ).convert("RGBA")
                        )
                        break

            if len(layers) == 1:
                rgb_im = layers[0].convert("RGBA")
            elif len(layers) == 2:
                main_composite = Image.alpha_composite(layers[0], layers[1])
                rgb_im = main_composite.convert("RGBA")
            elif len(layers) >= 3:
                main_composite = Image.alpha_composite(layers[0], layers[1])
                for index, remaining in enumerate(layers):
                    main_composite = Image.alpha_composite(main_composite, remaining)
                rgb_im = main_composite.convert("RGBA")

            # create folder structure if it doesn't exist
            rgb_im.save("{}/images/{}.png".format(self.output, metadata["token_id"]))

        except Exception as e:
            self.logger.error(
                "Error generating image for token %d: %s", metadata["token_id"], e
            )

    def __generate_with_quotas(self):
        """
        Generates NFTs using quota-based generation (exact counts per Background+Shirt).
        """
        self.logger.info("Generating NFTs using quota-based generation")
        
        # Find Model and Headwear layers (case-insensitive search)
        model_layer = None
        headwear_layer = None
        background_layer = None
        shirt_layer = None
        
        for layer in self.config["layers"]:
            layer_name_lower = layer["name"].lower()
            if layer_name_lower == "model" or layer_name_lower == "models":
                model_layer = layer
            elif layer_name_lower == "headwear":
                headwear_layer = layer
            elif layer_name_lower == "background" or layer_name_lower == "backgrounds":
                background_layer = layer
            elif layer_name_lower in ["shirt", "jersey", "jerseys", "jerseys-shirts"]:
                shirt_layer = layer
        
        if not all([model_layer, headwear_layer, background_layer, shirt_layer]):
            available_layers = [l["name"] for l in self.config["layers"]]
            raise ValueError(
                f"Quota-based generation requires Model, Headwear, Background, and Shirt/Jersey layers. "
                f"Found layers: {available_layers}"
            )
        
        token_id = self.start_at
        model_values = model_layer["values"]
        headwear_values = headwear_layer["values"]
        
        # Generate all Model×Headwear combinations
        model_headwear_combos = []
        for model in model_values:
            for headwear in headwear_values:
                model_headwear_combos.append({"Model": model, "Headwear": headwear})
        
        # Generate NFTs for each quota
        total_generated = 0
        with get_progress_bar(self.amount) as bar:
            for quota_entry in self.config["quotas"]:
                background = quota_entry["background"]
                shirt = quota_entry["shirt"]
                amount = quota_entry["amount"]
                
                # Generate 'amount' NFTs for this Background+Shirt combination
                # Each NFT will have a different Model×Headwear combination
                # If amount > 12, we'll cycle through combinations to fill the quota
                for i in range(amount):
                    combo = model_headwear_combos[i % len(model_headwear_combos)]
                    
                    forced_traits = {
                        background_layer["name"]: background,
                        shirt_layer["name"]: shirt,
                        model_layer["name"]: combo["Model"],
                        headwear_layer["name"]: combo["Headwear"]
                    }
                    
                    self.__build_genome_metadata(token_id, forced_traits)
                    write_json(
                        "{}/metadata/{}.json".format(self.output, token_id),
                        self.all_genomes[-1],
                    )
                    token_id += 1
                    total_generated += 1
                    bar()
        
        return total_generated

    def generate(self):
        """
        Generates the NFTs with the given configuration.
        """
        self.logger.info("Starting generation")

        if self.use_quotas:
            # Calculate total amount from quotas
            total_from_quotas = sum(q["amount"] for q in self.config["quotas"])
            
            # Test mode: If requested amount is much smaller than quota total, use weighted random instead
            # This allows testing without generating the full collection
            if self.amount < 100 or self.amount < (total_from_quotas * 0.01):
                self.logger.info(
                    "Test mode detected: Requested amount (%d) is much smaller than quota total (%d). "
                    "Using weighted random generation instead of quotas for testing.",
                    self.amount, total_from_quotas
                )
                # Temporarily disable quotas for this generation
                self.use_quotas = False
            elif self.amount != total_from_quotas:
                self.logger.warning(
                    "Amount specified (%d) doesn't match quota total (%d). Using quota total.",
                    self.amount, total_from_quotas
                )
                self.amount = total_from_quotas
        
        if self.use_quotas:
            total_generated = self.__generate_with_quotas()
        else:
            # Use standard weighted random generation
            max_combinations = calculate_possible_combinations(self.config)
            self.logger.debug(
                "There are {:,} possible unique combinations of this configuration".format(
                    max_combinations
                )
            )
            if self.amount > max_combinations and not self.allow_duplicates:
                raise ValueError(
                    "Amount of NFTs to generate ({:,}) is greater than the number of possible unique combinations ({:,})".format(
                        self.amount, max_combinations
                    )
                )

            self.logger.info("Generating %d NFTs", self.amount)
            with get_progress_bar(self.amount) as bar:
                for i in range(self.amount):
                    token_id = self.start_at + i
                    self.__build_genome_metadata(token_id)
                    write_json(
                        "{}/metadata/{}.json".format(self.output, token_id),
                        self.all_genomes[-1],
                    )
                    bar()
            total_generated = self.amount
            write_json(
                "{}/metadata/all-objects.json".format(
                    self.output,
                ),
                self.all_genomes,
            )
            write_file(
                "{}/.generatorrc".format(
                    self.output,
                ),
                self.__tomlify(),
            )

        self.logger.info("Generating layered images for %d NFTs", self.amount)

        # make folder structure
        os.makedirs("{}/images/".format(self.output), exist_ok=True)

        with get_progress_bar(len(self.all_genomes)) as bar:
            with ThreadPoolExecutor(max_workers=25) as pool:
                try:
                    futures = [
                        pool.submit(self.__build_genome_image, genome)
                        for genome in self.all_genomes
                    ]
                    for _ in as_completed(futures):
                        bar()
                except KeyboardInterrupt:
                    self.logger.error("Generation interrupted by user")
                    return

        self.logger.info("Generation complete!")
