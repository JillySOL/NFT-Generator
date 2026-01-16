"""
Script to generate reserved NFT entries from spreadsheet data.
Reserved NFTs include 1/1s and unique "Gamba Dogs" NFTs.
"""

import json
import sys

# Model mapping: spreadsheet -> config value
MODEL_MAP = {
    "black": "Black",
    "grey": "White",  # Grey model = White in config
    "beige": "Beige"
}

# Headwear mapping: spreadsheet -> config value
HEADWEAR_MAP = {
    "white": "White Cap",
    "black": "Black Cap",
    "grey": "Grey Cap",
    "no cap": "No Cap"
}

# Background mapping: spreadsheet -> config value
BACKGROUND_MAP = {
    "spicerqq": "SpicerQQ",
    "bet it like": "BET IT LIKE",
    "solana": "SOLANA",
    "nfts are dead": "NFTs ARE DEAD",
    "allergic to money": "ALLERGIC TO MONEY",
    "gamba dogs": "GAMBA DOGS"
}

# Jersey mapping: spreadsheet -> config value
JERSEY_MAP = {
    "georgia": "Georgia Jersey",
    "palestine 1/1": "Palestine 1 of 1",
    "netherlands 1/1": "Holland 1 of 1",  # Netherlands = Holland in files
    "france 1/1": "France 1 of 1",
    "greece 1/1": "Greece 1 of 1",
    "brasil 1/1": "Brazil 1 of 1",
    "germany 1/1": "Germany 1 of 1",
    "belgium": "Belgium Jersey",
    "curacao": "Curacao Jersey",
    "japan": "Japan Jersey",
    "france": "France Jersey",
    "germany": "Germany Jersey",
    "turkey": "Turkey Jersey",
    "brasil": "Brazil Jersey",
    "senegal": "Senegal Jersey",
    "usa": "USA Jersey",
    # Batch 2
    "argentinia 1/1": "Argentina 1 of 1",
    "uruguay 1/1": "Uruguay 1 of 1",
    "uddsr 1/1": "UDSSR 1 of 1",
    "spain 1/1": "Spain 1 of 1",
    "portugal 1/1": "Portugal 1 of 1",
    "italy 1/1": "Italy 1 of 1",
    "denmark 1/1": "Denmark 1 of 1",
    "england 1/1": "England 1 of 1",
    "south korea": "South Korea Jersey",
    "poland": "Poland Jersey",
    "croatia": "Croatia Jersey",
    "argentinia": "Argentina Jersey",
    "russia": "Russia Jersey",
    "mexico": "Mexico Jersey",
    "spain": "Spain Jersey",
    "switzerland": "Switzerland Jersey",
    "egypt": "Egypt Jersey"  # Placeholder
}

# Batch 1: Fixed token IDs
BATCH_1_DATA = [
    {"token_id": 9999, "background": "spicerqq", "jersey": "georgia", "model": "black", "headwear": "white", "type": "1/1", "id": "9999"},
    {"token_id": 9000, "background": "bet it like", "jersey": "palestine 1/1", "model": "grey", "headwear": "white", "type": "1/1", "id": "9000"},
    {"token_id": 9393, "background": "solana", "jersey": "netherlands 1/1", "model": "beige", "headwear": "no cap", "type": "1/1", "id": "9393"},
    {"token_id": 9223, "background": "solana", "jersey": "france 1/1", "model": "grey", "headwear": "black", "type": "1/1", "id": "9223"},
    {"token_id": 9696, "background": "nfts are dead", "jersey": "greece 1/1", "model": "grey", "headwear": "no cap", "type": "1/1", "id": "9696"},
    {"token_id": 9876, "background": "allergic to money", "jersey": "brasil 1/1", "model": "grey", "headwear": "white", "type": "1/1", "id": "9876"},
    {"token_id": 9090, "background": "solana", "jersey": "germany 1/1", "model": "grey", "headwear": "grey", "type": "1/1", "id": "9090"},
    {"token_id": 9997, "background": "gamba dogs", "jersey": "belgium", "model": "black", "headwear": "no cap", "type": "unique", "id": "xxxx"},
    {"token_id": 9040, "background": "gamba dogs", "jersey": "curacao", "model": "grey", "headwear": "no cap", "type": "unique", "id": "xxxx"},
    {"token_id": 9998, "background": "gamba dogs", "jersey": "japan", "model": "grey", "headwear": "black", "type": "unique", "id": "xxxx"},
    {"token_id": 9993, "background": "gamba dogs", "jersey": "france", "model": "black", "headwear": "no cap", "type": "unique", "id": "xxxx"},
    {"token_id": 9996, "background": "gamba dogs", "jersey": "germany", "model": "grey", "headwear": "white", "type": "unique", "id": "xxxx"},
    {"token_id": 9992, "background": "gamba dogs", "jersey": "turkey", "model": "beige", "headwear": "no cap", "type": "unique", "id": "xxxx"},
    {"token_id": 9994, "background": "gamba dogs", "jersey": "brasil", "model": "beige", "headwear": "black", "type": "unique", "id": "xxxx"},
    {"token_id": 9991, "background": "gamba dogs", "jersey": "senegal", "model": "grey", "headwear": "no cap", "type": "unique", "id": "xxxx"},
    {"token_id": 9995, "background": "gamba dogs", "jersey": "usa", "model": "black", "headwear": "white", "type": "unique", "id": "xxxx"},
]

# Batch 2: Random token IDs (will be assigned sequentially after quota NFTs)
BATCH_2_DATA = [
    {"background": "bet it like", "jersey": "argentinia 1/1", "model": "black", "headwear": "no cap", "type": "1/1", "id": "random"},
    {"background": "nfts are dead", "jersey": "uruguay 1/1", "model": "beige", "headwear": "no cap", "type": "1/1", "id": "random"},
    {"background": "gamba dogs", "jersey": "uddsr 1/1", "model": "black", "headwear": "no cap", "type": "1/1", "id": "random"},
    {"background": "bet it like", "jersey": "spain 1/1", "model": "beige", "headwear": "grey", "type": "1/1", "id": "random"},
    {"background": "bet it like", "jersey": "portugal 1/1", "model": "black", "headwear": "black", "type": "1/1", "id": "random"},
    {"background": "solana", "jersey": "italy 1/1", "model": "grey", "headwear": "no cap", "type": "1/1", "id": "random"},
    {"background": "allergic to money", "jersey": "denmark 1/1", "model": "grey", "headwear": "white", "type": "1/1", "id": "random"},
    {"background": "solana", "jersey": "england 1/1", "model": "grey", "headwear": "grey", "type": "1/1", "id": "random"},
    {"background": "gamba dogs", "jersey": "south korea", "model": "beige", "headwear": "white", "type": "unique", "id": "xxxx"},
    {"background": "gamba dogs", "jersey": "poland", "model": "beige", "headwear": "no cap", "type": "unique", "id": "xxxx"},
    {"background": "gamba dogs", "jersey": "croatia", "model": "grey", "headwear": "no cap", "type": "unique", "id": "xxxx"},
    {"background": "gamba dogs", "jersey": "argentinia", "model": "black", "headwear": "white", "type": "unique", "id": "xxxx"},
    {"background": "gamba dogs", "jersey": "russia", "model": "grey", "headwear": "no cap", "type": "unique", "id": "xxxx"},
    {"background": "gamba dogs", "jersey": "mexico", "model": "grey", "headwear": "black", "type": "unique", "id": "xxxx"},
    {"background": "gamba dogs", "jersey": "spain", "model": "black", "headwear": "no cap", "type": "unique", "id": "xxxx"},
    {"background": "gamba dogs", "jersey": "switzerland", "model": "grey", "headwear": "grey", "type": "unique", "id": "xxxx"},
]

def normalize_key(key):
    """Normalize keys to lowercase for matching."""
    return key.lower().strip()

def map_reserved_entry(entry, is_fixed=False):
    """Map spreadsheet entry to config format."""
    background_key = normalize_key(entry["background"])
    jersey_key = normalize_key(entry["jersey"])
    model_key = normalize_key(entry["model"])
    headwear_key = normalize_key(entry["headwear"])
    
    mapped = {
        "background": BACKGROUND_MAP.get(background_key, entry["background"].upper()),
        "jersey": JERSEY_MAP.get(jersey_key, entry["jersey"]),
        "model": MODEL_MAP.get(model_key, entry["model"].capitalize()),
        "headwear": HEADWEAR_MAP.get(headwear_key, entry["headwear"].capitalize() + " Cap" if headwear_key != "no cap" else "No Cap"),
        "type": entry["type"],
        "id": entry["id"]
    }
    
    if is_fixed:
        mapped["token_id"] = entry["token_id"]
    
    return mapped

def generate_reserved_section():
    """Generate reserved section for config.json."""
    fixed = [map_reserved_entry(entry, is_fixed=True) for entry in BATCH_1_DATA]
    random = [map_reserved_entry(entry, is_fixed=False) for entry in BATCH_2_DATA]
    
    return {
        "fixed": fixed,
        "random": random
    }

if __name__ == "__main__":
    reserved = generate_reserved_section()
    
    # Configure stdout for Unicode
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8')
    
    print("Reserved NFT Configuration:")
    print(f"  Fixed (Batch 1): {len(reserved['fixed'])} NFTs")
    print(f"  Random (Batch 2): {len(reserved['random'])} NFTs")
    print(f"  Total Reserved: {len(reserved['fixed']) + len(reserved['random'])} NFTs")
    print("\nFixed NFTs:")
    for entry in reserved['fixed']:
        print(f"  Token {entry['token_id']}: {entry['background']} + {entry['jersey']} ({entry['type']})")
    
    print("\nRandom NFTs:")
    for entry in reserved['random']:
        print(f"  {entry['background']} + {entry['jersey']} ({entry['type']})")
    
    # Save to JSON file for inspection
    with open("reserved_nfts.json", "w", encoding="utf-8") as f:
        json.dump(reserved, f, indent=2, ensure_ascii=False)
    
    print("\n✓ Reserved NFT data saved to reserved_nfts.json")
