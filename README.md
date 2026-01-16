# Gamba Dogs NFT Generator

A customized NFT generation system built for the **Gamba Dogs** collection, featuring quota-based generation, precise trait distribution, and support for 1/1 and unique NFTs.

![Gamba Dogs](preview.png)

## Overview

This NFT generator has been customized specifically for the Gamba Dogs collection with the following features:

- **Quota-Based Generation**: Generate exact counts for each Background+Jersey combination
- **Reserved NFTs**: Support for 1/1s and unique "Gamba Dogs" NFTs with fixed or sequential token IDs
- **Precise Layer Stacking**: Background → Model → Jersey → Headwear (bottom to top)
- **Test Mode**: Automatically uses weighted random generation for small test batches
- **Symbol Support**: Includes `symbol` field in metadata (GMB)
- **Batch Support**: Handles Batch 1 (9000-9999) and Batch 2 (8000-8999) token ID ranges

## Getting Started

### Prerequisites

- Python 3.7 or higher
- All trait layer images in PNG format

### Installation

```bash
git clone https://github.com/JillySOL/NFT-Generator.git
cd NFT-Generator
python -m pip install -r requirements.txt
```

### Quick Start

1. **Validate your configuration:**
   ```bash
   python main.py validate --config config.json --amount 1965
   ```

2. **Test with a small batch:**
   ```bash
   python main.py generate --config config.json --amount 5 --output ./test-output --start-at 8000
   ```

3. **Generate full collection (including reserved NFTs):**
   ```bash
   python main.py generate --config config.json --amount 1965 --output ./output --start-at 8000
   ```
   
   This will automatically generate:
   - 1,965 quota NFTs (starting at token ID 8000)
   - 16 fixed reserved NFTs at their specified token IDs (9000-9999 range)
   - 16 random reserved NFTs sequentially after quota NFTs
   - **Total: 1,997 NFTs**

## CLI Commands

| Command | Usage | Description |
|---------|-------|-------------|
| `generate` | `python main.py generate --config <config> [options]` | Generates NFTs using the provided configuration file |
| `build_config` | `python main.py build_config --trait-dir <trait_dir> [options]` | Builds a configuration file from a directory of traits |
| `validate` | `python main.py validate --config <config> [options]` | Validates a configuration file |
| `update_metadata` | `python main.py update_metadata --image-path <path> [options]` | Updates metadata files for generated images |

### Command Arguments

| Argument | Description |
|----------|-------------|
| `-o <output>`, `--output <output>` | Output directory for generated images and metadata (default: `./output`) |
| `-c <config>`, `--config <config>` | Path to configuration JSON file |
| `-n <amount>`, `--amount <amount>` | Number of NFTs to generate |
| `--start-at <start_at>` | Starting token ID (default: 0). Use `8000` for Batch 2 or `9000` for Batch 1 |
| `-s <seed>`, `--seed <seed>` | Random seed for reproducible generation |
| `-v`, `--verbose` | Enable verbose logging |
| `--allow-duplicates` | Allow duplicate trait combinations |
| `--no-pad` | Disable zero-padding of token IDs |

## Configuration

### Gamba Dogs Configuration Structure

```json
{
  "layers": [
    {
      "name": "Background",
      "values": ["POOR", "NFTs ARE DEAD", "SOLANA", "BET IT LIKE", "ALLERGIC TO MONEY"],
      "trait_path": "./trait-layers/backgrounds",
      "filename": ["POOR", "NFTs ARE DEAD", "SOLANA", "BET IT LIKE", "ALLERGIC TO MONEY"],
      "weights": [20.0, 20.0, 20.0, 20.0, 20.0]
    },
    {
      "name": "Model",
      "values": ["Black", "White", "Beige"],
      "trait_path": "./trait-layers/MODELS",
      "filename": ["BLACK", "GREY", "BEIGE"],
      "weights": [33.33, 33.33, 33.34]
    },
    {
      "name": "Jersey",
      "values": ["Basic Blue", "Argentina Jersey", ...],
      "trait_path": "./trait-layers/JERSEYS-SHIRTS",
      "filename": ["Basic Blue", "Argentina Jersey", ...],
      "weights": [...]
    },
    {
      "name": "Headwear",
      "values": ["White Cap", "Black Cap", "Grey Cap", "No Cap"],
      "trait_path": "./trait-layers/HEADWEAR",
      "filename": ["White Cap", "Black Cap", "Grey Cap", "No Cap"],
      "weights": [16.67, 16.67, 16.66, 50.0]
    }
  ],
  "quotas": [
    {
      "background": "POOR",
      "shirt": "Basic Blue",
      "amount": 12
    }
  ],
  "baseURI": ".",
  "name": "Gamba Dog #",
  "description": "The most exclusive Gamba community.",
  "symbol": "GMB"
}
```

### Layer Stacking Order

Layers are composited in this order (bottom to top):
1. **Background** - Base layer
2. **Model** - Character model (Black, White, Beige)
3. **Jersey** - Shirt/jersey layer
4. **Headwear** - Top layer (Caps or No Cap)

### Quota System

The quota system allows you to specify exact counts for each Background+Jersey combination:

```json
"quotas": [
  {
    "background": "POOR",
    "shirt": "Basic Blue",
    "amount": 12
  }
]
```

- Each quota entry generates exactly the specified number of NFTs
- Each Background+Jersey combination is automatically paired with all Model×Headwear variations (3 Models × 4 Headwear = 12 combinations)
- If `amount > 12`, Model×Headwear combinations will cycle to fill the quota

**Total NFTs from quotas:** 1,965 NFTs

### Reserved NFTs (1/1s and Uniques)

The generator supports reserved NFTs that are generated separately from quota NFTs:

```json
"reserved": {
  "fixed": [
    {
      "token_id": 9999,
      "background": "SpicerQQ",
      "jersey": "Georgia Jersey",
      "model": "Black",
      "headwear": "White Cap",
      "type": "1/1",
      "id": "9999"
    }
  ],
  "random": [
    {
      "background": "BET IT LIKE",
      "jersey": "Argentina 1 of 1",
      "model": "Black",
      "headwear": "No Cap",
      "type": "1/1",
      "id": "random"
    }
  ]
}
```

**Generation Flow:**
1. **Step 1**: Generate quota NFTs (1,965 NFTs starting at `--start-at`)
2. **Step 2**: Generate fixed reserved NFTs at their specified token IDs (Batch 1: 9000-9999 range)
3. **Step 3**: Generate random reserved NFTs sequentially after quota NFTs (Batch 2)

**Reserved NFT Types:**
- **Fixed**: Have a specific `token_id` assigned (e.g., 9999, 9000, 9393)
- **Random**: Assigned token IDs sequentially after quota NFTs complete

**Total Reserved NFTs:** 32 (16 fixed + 16 random)

### Test Mode

When generating small batches for testing, the generator automatically switches to weighted random generation:

- **Test mode activates when:** Requested amount < 100 OR < 1% of quota total
- **Behavior:** Uses weighted random selection instead of quotas
- **Use case:** Test image generation and layer stacking without generating the full collection

Example:
```bash
# Generates 5 NFTs using weighted random (test mode)
python main.py generate --config config.json --amount 5 --output ./test-output
```

### Metadata Fields

Each generated NFT includes:

- `token_id`: Unique token identifier
- `name`: "Gamba Dog #XXXX" (e.g., "Gamba Dog #8000")
- `description`: "The most exclusive Gamba community."
- `symbol`: "GMB"
- `image`: Path to generated image
- `attributes`: Array of trait types and values

## Gamba Dogs Collection Structure

### Trait Layers

- **Models**: 3 variants (Black, White, Beige) - 33.3% distribution each
- **Headwear**: 4 variants (White Cap, Black Cap, Grey Cap, No Cap) - 50% No Cap, 16.6% each cap
- **Backgrounds**: 7 backgrounds (POOR, NFTs ARE DEAD, SOLANA, BET IT LIKE, ALLERGIC TO MONEY, GAMBA DOGS, SpicerQQ)
- **Jerseys/Shirts**: 117 unique jerseys and shirts

### Batch Structure

- **Batch 1**: Token IDs 9000-9999 (contains fixed reserved NFTs)
- **Batch 2**: Token IDs 8000-8999 (contains quota NFTs + random reserved NFTs)
- **Total Collection**: 1,997 NFTs (1,965 quota + 32 reserved)

### File Structure

```
trait-layers/
├── MODELS/
│   ├── BLACK.png
│   ├── GREY.png (White model)
│   └── BEIGE.png
├── HEADWEAR/
│   ├── White Cap.png
│   ├── Black Cap.png
│   ├── Grey Cap.png
│   └── No Cap.png
├── backgrounds/
│   ├── POOR.png
│   ├── NFTs ARE DEAD.png
│   ├── SOLANA.png
│   ├── BET IT LIKE.png
│   ├── ALLERGIC TO MONEY.png
│   ├── GAMBA DOGS.png
│   └── SpicerQQ.png
└── JERSEYS-SHIRTS/
    ├── Basic Blue.png
    ├── Argentina Jersey.png
    ├── Argentina 1 of 1.png
    └── ... (131 total files)
```

## Setup Scripts

### `setup_quotas.py`

Generates `config.json` with quotas and reserved NFTs from allocation table data. Run this to regenerate the config after updating quota or reserved NFT data:

```bash
python setup_quotas.py
```

This script:
- Generates quota entries from the allocation table
- Includes reserved NFTs (1/1s and uniques) from `setup_reserved.py`
- Adds GAMBA DOGS and SpicerQQ backgrounds
- Adds all 1/1 jerseys
- Includes Egypt Jersey placeholder

### `setup_reserved.py`

Generates reserved NFT entries from spreadsheet data. This is automatically called by `setup_quotas.py`, but can be run independently:

```bash
python setup_reserved.py
```

### `verify_setup.py`

Verifies all files referenced in `config.json` exist and validates the configuration:

```bash
python verify_setup.py
```

## How to Generate Your Collection

### Step-by-Step Instructions

1. **Verify Setup** (Recommended)
   ```bash
   python verify_setup.py
   ```
   This checks that all trait files exist and the configuration is valid.

2. **Validate Configuration**
   ```bash
   python main.py validate --config config.json --amount 1965
   ```
   This ensures your `config.json` is properly formatted.

3. **Test Generation** (Optional but Recommended)
   ```bash
   python main.py generate --config config.json --amount 5 --output ./test-output --start-at 8000
   ```
   This generates 5 test NFTs to verify everything works. Check the output in `./test-output/`.

4. **Generate Full Collection**
   ```bash
   python main.py generate --config config.json --amount 1965 --output ./output --start-at 8000
   ```
   
   **What this does:**
   - Generates 1,965 quota NFTs (token IDs 8000-9964)
   - Generates 16 fixed reserved NFTs at their specified IDs (9000-9999 range)
   - Generates 16 random reserved NFTs sequentially (token IDs 9965-9980)
   - **Total: 1,997 NFTs**

5. **Check Output**
   - Images: `./output/images/` (1,997 PNG files)
   - Metadata: `./output/metadata/` (1,997 JSON files)
   - All metadata: `./output/metadata/all-objects.json` (complete collection)

### Important Notes

- **Starting Token ID**: Use `--start-at 8000` for Batch 2. The generator will automatically handle reserved NFTs in the 9000-9999 range.
- **Amount Parameter**: Always use `1965` (the quota total). Reserved NFTs are generated automatically.
- **Output Directory**: Change `./output` to your desired output path.
- **Generation Time**: Full collection generation takes approximately 5-10 minutes depending on your system.

### After Generation

1. Verify all files were created:
   ```bash
   # Count images
   dir output\images\*.png | find /c ".png"
   
   # Count metadata
   dir output\metadata\*.json | find /c ".json"
   ```
   Should show 1,997 for both.

2. Check specific reserved NFTs:
   - Fixed reserved: Check token IDs 9000, 9090, 9223, 9393, 9696, 9876, 9991-9999
   - Random reserved: Check token IDs 9965-9980

3. Verify metadata structure:
   - Open any JSON file in `output/metadata/`
   - Ensure it has `token_id`, `name`, `description`, `symbol`, `image`, and `attributes`

## Troubleshooting

### Common Issues

1. **"File not found" errors**
   - Ensure all PNG files exist in the specified `trait_path` directories
   - Check filename spelling matches exactly (case-sensitive)
   - Run `python verify_setup.py` to check all files

2. **"Weights must sum to 100" errors**
   - Verify all layer weights sum to exactly 100.0
   - Check for floating-point precision issues (use 33.33, 33.33, 33.34 instead of 33.3, 33.3, 33.4)

3. **Test mode not activating**
   - Test mode activates when amount < 100 or < 1% of quota total
   - For quota-based generation, use the full quota amount (1965)

4. **Layer stacking issues**
   - Verify layer order in `config.json`: Background → Model → Jersey → Headwear
   - All images must be the same size (typically 1000x1000 pixels)

### Image Requirements

- All images must be in PNG format
- All images must be the same pixel dimensions (e.g., 1000x1000)
- Filenames in config should omit the `.png` extension
- Filenames are case-sensitive

## Custom Features for Gamba Dogs

### Quota-Based Generation

Unlike standard weighted random generation, the quota system ensures:
- Exact counts per Background+Jersey combination
- Predictable distribution matching allocation tables
- Support for complex rarity distributions

### Reserved NFT System

The reserved NFT system handles special NFTs separately from quota generation:
- **Fixed Reserved NFTs**: Generated at their specified token IDs (e.g., 9999, 9000)
- **Random Reserved NFTs**: Generated sequentially after quota NFTs complete
- **Automatic Generation**: Reserved NFTs are generated automatically when quotas are used
- **No Manual Configuration**: All reserved NFTs are defined in `config.json` under the `reserved` section

### Automatic Test Mode

Small test batches automatically use weighted random generation, allowing you to:
- Test image generation quickly
- Verify layer stacking
- Check metadata structure
- Without generating the full 1,965 NFT collection

**Note**: Test mode bypasses both quotas and reserved NFTs. To test reserved NFTs, generate at least 100 NFTs.

### Symbol Field

Metadata includes a `symbol` field set to "GMB" for compatibility with Solana and other blockchain standards.

## Output Structure

Generated files are organized as follows:

```
output/
├── images/
│   ├── 8000.png
│   ├── 8001.png
│   └── ...
├── metadata/
│   ├── 8000.json
│   ├── 8001.json
│   ├── all-objects.json
│   └── ...
└── .generatorrc
```

- **images/**: Generated composite PNG images
- **metadata/**: Individual JSON metadata files
- **all-objects.json**: Complete metadata for all generated NFTs
- **.generatorrc**: Generation configuration and seed information

## License

See [LICENSE](LICENSE) file for details.

## Credits

Built for **Gamba Dogs** - The most exclusive Gamba community.

Based on [nft-generator-py](https://github.com/Jon-Becker/nft-generator-py) with customizations for quota-based generation and Gamba Dogs collection requirements.
