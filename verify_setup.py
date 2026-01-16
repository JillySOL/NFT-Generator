"""
Script to verify all files referenced in config.json actually exist.
"""

import json
import os
from pathlib import Path

def verify_setup():
    """Verify all files in config exist."""
    print("=" * 60)
    print("NFT Generator Setup Verification")
    print("=" * 60)
    
    # Load config
    with open("config.json", "r") as f:
        config = json.load(f)
    
    errors = []
    warnings = []
    
    # Verify layers
    print("\n[1] Verifying Layer Files...")
    for layer in config["layers"]:
        layer_name = layer["name"]
        print(f"\n  Layer: {layer_name}")
        
        for i, (value, filename) in enumerate(zip(layer["values"], layer["filename"])):
            file_path = Path(layer["trait_path"]) / f"{filename}.png"
            if file_path.exists():
                print(f"    [OK] {value} -> {file_path}")
            else:
                error_msg = f"    [ERROR] {value} -> {file_path} (FILE NOT FOUND)"
                print(error_msg)
                errors.append(f"{layer_name} layer: {error_msg}")
    
    # Verify quotas
    print("\n[2] Verifying Quota Entries...")
    quotas = config.get("quotas", [])
    print(f"  Total quota entries: {len(quotas)}")
    
    total_nfts = sum(q["amount"] for q in quotas)
    print(f"  Total NFTs from quotas: {total_nfts}")
    
    # Check quota background/shirt matching
    background_values = set(config["layers"][2]["values"])  # Background layer
    jersey_values = set(config["layers"][3]["values"])      # Jersey layer
    
    quota_backgrounds = set(q["background"] for q in quotas)
    quota_shirts = set(q["shirt"] for q in quotas)
    
    missing_bg = quota_backgrounds - background_values
    missing_jersey = quota_shirts - jersey_values
    
    if missing_bg:
        warnings.append(f"Quota backgrounds not in layer: {missing_bg}")
        print(f"  [WARNING] Quota backgrounds not in Background layer: {missing_bg}")
    
    if missing_jersey:
        warnings.append(f"Quota shirts not in layer: {missing_jersey}")
        print(f"  [WARNING] Quota shirts not in Jersey layer: {missing_jersey}")
    
    if not missing_bg and not missing_jersey:
        print("  [OK] All quota backgrounds and shirts match layer values")
    
    # Verify weights
    print("\n[3] Verifying Layer Weights...")
    for layer in config["layers"]:
        weights = layer["weights"]
        total = sum(weights)
        if abs(total - 100.0) < 0.01:
            print(f"  [OK] {layer['name']}: weights sum to {total:.2f}")
        else:
            error_msg = f"  [ERROR] {layer['name']}: weights sum to {total:.2f} (should be 100)"
            print(error_msg)
            errors.append(error_msg)
    
    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    if errors:
        print(f"\n[ERRORS] Found: {len(errors)}")
        for error in errors:
            print(f"  - {error}")
    else:
        print("\n[SUCCESS] No errors found!")
    
    if warnings:
        print(f"\n[WARNINGS] Found: {len(warnings)}")
        for warning in warnings:
            print(f"  - {warning}")
    else:
        print("\n[SUCCESS] No warnings!")
    
    print(f"\nConfiguration Stats:")
    print(f"  - Total quota entries: {len(quotas)}")
    print(f"  - Total NFTs to generate: {total_nfts}")
    print(f"  - Unique backgrounds: {len(background_values)}")
    print(f"  - Unique jerseys: {len(jersey_values)}")
    print(f"  - Model options: {len(config['layers'][0]['values'])}")
    print(f"  - Headwear options: {len(config['layers'][1]['values'])}")
    
    return len(errors) == 0

if __name__ == "__main__":
    success = verify_setup()
    exit(0 if success else 1)
