# Quota-Based Generation System

## Overview

The NFT generator now supports **quota-based generation**, which allows you to specify exact counts for each Background+Shirt combination. This ensures precise control over the number of NFTs generated for each trait combination.

## How It Works

When a `quotas` section is present in your `config.json`, the generator will:

1. Generate exactly the specified number of NFTs for each Background+Shirt combination
2. Automatically combine each Background+Shirt with all Model×Headwear combinations
3. Cycle through Model×Headwear combinations if the amount exceeds 12 (3 Models × 4 Headwear)

## Config Structure

Add a `quotas` array to your `config.json`:

```json
{
  "layers": [
    {
      "name": "Model",
      "values": ["Black", "White", "Beige"],
      "trait_path": "./trait-layers/MODELS",
      "filename": ["BLACK", "GREY", "BEIGE"],
      "weights": [33.33, 33.33, 33.34]
    },
    {
      "name": "Headwear",
      "values": ["White Cap", "Black Cap", "Grey Cap", "No Cap"],
      "trait_path": "./trait-layers/HEADWEAR",
      "filename": ["White Cap", "Black Cap", "Grey Cap", "No Cap"],
      "weights": [16.6, 16.6, 16.6, 50.0]
    },
    {
      "name": "Background",
      "values": ["POOR", "NFTs ARE DEAD", "SOLANA", "BET IT LIKE", "ALLERGIC TO MONEY", "GAMBA DOGS", "SpicerQQ"],
      "trait_path": "./trait-layers/backgrounds",
      "filename": ["POOR", "NFTs ARE DEAD", "SOLANA", "BET IT LIKE", "ALLERGIC TO MONEY", "GAMBA DOGS", "SpicerQQ"],
      "weights": [14.3, 14.3, 14.3, 14.3, 14.3, 14.3, 14.2]
    },
    {
      "name": "Jersey",
      "values": ["Basic Blue", "Basic Brown", ...],
      "trait_path": "./trait-layers/JERSEYS-SHIRTS",
      "filename": ["Basic Blue", "Basic Brown", ...],
      "weights": [1.0, 1.0, ...]
    }
  ],
  "quotas": [
    {
      "background": "Poor",
      "shirt": "Basic Blue",
      "amount": 12
    },
    {
      "background": "Poor",
      "shirt": "Basic Brown",
      "amount": 12
    },
    {
      "background": "NFT's are dead",
      "shirt": "Argentina Jersey",
      "amount": 7
    }
    // ... more quota entries
  ],
  "incompatibilities": [],
  "baseURI": ".",
  "name": "Gamba Dog #",
  "description": "Gamba Dog NFT Collection"
}
```

## Quota Entry Format

Each quota entry has three fields:

- **background**: The background name (must match exactly with a value in the Background layer)
- **shirt**: The shirt/jersey name (must match exactly with a value in the Jersey layer)
- **amount**: The exact number of NFTs to generate for this combination (integer, >= 0)

## Important Notes

1. **Layer Name Matching**: The generator searches for layers case-insensitively:
   - Model/Models
   - Headwear
   - Background/Backgrounds
   - Shirt/Jersey/Jerseys/Jerseys-Shirts

2. **Model×Headwear Combinations**: 
   - Each Background+Shirt combination will be paired with Model×Headwear combinations
   - If amount ≤ 12: Each NFT gets a unique Model×Headwear combination
   - If amount > 12: Model×Headwear combinations will cycle (some duplicates)

3. **Total NFT Count**: The generator automatically calculates the total from quotas. If you specify `--amount`, it should match the sum of all quota amounts.

4. **Weights**: When using quotas, the weights in layers are still required but are overridden by the quota system. They're only used for layers not controlled by quotas.

## Converting Your Table Data

To convert your allocation table into quotas:

1. For each row: `(Rarity, Background, Shirt Type, Shirt Name, Amount)`
2. Create a quota entry: `{"background": Background, "shirt": Shirt Name, "amount": Amount}`
3. Add all quota entries to the `quotas` array

## Example

If your table has:
```
Common | Poor | Basic Shirt | Basic Blue | 12
Common | Poor | Basic Shirt | Basic Brown | 12
Uncommon | NFT's are dead | Country Jersey | Argentina Jersey | 7
```

Your quotas would be:
```json
"quotas": [
  {"background": "Poor", "shirt": "Basic Blue", "amount": 12},
  {"background": "Poor", "shirt": "Basic Brown", "amount": 12},
  {"background": "NFT's are dead", "shirt": "Argentina Jersey", "amount": 7}
]
```

## Usage

Generate NFTs with quotas:

```bash
python main.py generate --config config.json --amount 1968 --output ./output
```

The `--amount` should match the sum of all quota amounts, or the generator will warn you and use the quota total.
