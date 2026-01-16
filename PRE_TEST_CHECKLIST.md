# Pre-Test Checklist for NFT Generator

## ✅ Setup & Installation
- [x] Dependencies installed (`python -m pip install -r requirements.txt`)
- [x] All required packages available (Pillow, argparse, pytest-cov, black, pre-commit, etc.)

## ✅ File Structure
- [x] `trait-layers/MODELS/` - Contains: BLACK.png, GREY.png (White), BEIGE.png
- [x] `trait-layers/HEADWEAR/` - Contains: White Cap.png, Black Cap.png, Grey Cap.png, No Cap.png
- [x] `trait-layers/backgrounds/` - Contains: POOR.png, NFTs ARE DEAD.png, SOLANA.png, BET IT LIKE.png, ALLERGIC TO MONEY.png, GAMBA DOGS.png, SpicerQQ.png
- [x] `trait-layers/JERSEYS-SHIRTS/` - Contains 131 PNG files (all required jerseys/shirts)
- [x] `config.json` - Configuration file exists and is properly formatted

## ✅ Configuration File (`config.json`)

### Layer Configuration
- [x] **Model Layer**: 3 values (Black, White, Beige) with 33.3% distribution each
- [x] **Headwear Layer**: 4 values (White Cap, Black Cap, Grey Cap, No Cap) with 50% No Cap, 16.67% each cap
- [x] **Background Layer**: 5 backgrounds (POOR, NFTs ARE DEAD, SOLANA, BET IT LIKE, ALLERGIC TO MONEY)
- [x] **Jersey Layer**: 117 unique shirts/jerseys
- [x] All layer weights sum to 100
- [x] All `trait_path` values are correct
- [x] All `filename` values match actual PNG files (without .png extension)

### Quota System
- [x] `quotas` array present in config
- [x] 416 quota entries defined
- [x] Each quota has: `background`, `shirt`, `amount`
- [x] Total NFTs from quotas: 1,965 (Note: 3 missing due to "Egypt" jersey not existing)
- [x] Background names in quotas match Background layer values
- [x] Shirt names in quotas match Jersey layer values

### Metadata Configuration
- [x] `name`: "Gamba Dog #" (matches requirements)
- [x] `description`: "Gamba Dog NFT Collection"
- [x] `baseURI`: "." (can be updated later for hosting)

## ⚠️ Requirements vs Current Setup

### Trait Requirements
- [x] Model: Black, White, Beige (3 total) ✅
- [x] Headwear: White Cap, Black Cap, Grey Cap, No Cap (4 total) ✅
- [x] Backgrounds: 7 total mentioned in requirements, but only 5 used in quotas (POOR, NFTs ARE DEAD, SOLANA, BET IT LIKE, ALLERGIC TO MONEY)
  - ⚠️ Missing from quotas: GAMBA DOGS, SpicerQQ (1/1 reserved)
- [x] Jerseys/Shirts: All specified in quotas ✅

### Batch ID Ranges
- [ ] **Batch 1**: Gamba Dog #9000–9999 (1000 NFTs)
- [ ] **Batch 2**: Gamba Dog #8000–8999 (1000 NFTs)
- ⚠️ **Current total**: 1,965 NFTs (need to decide on ID range)
- ⚠️ **Note**: `--start-at` parameter controls starting token ID

### NFT Allocation
- [x] Total NFTs: 1,965 (from quotas) - 3 short of 1,968 due to missing "Egypt" jersey
- [x] Model distribution: 33.3% per color (handled by quota system)
- [x] Headwear distribution: 50% No Cap, 16.6% each cap (handled by quota system)
- [x] Shirt/Background combinations: Exact counts specified in quotas ✅

## ⚠️ Known Issues
1. **Missing "Egypt" Jersey**: Table specifies 3 NFTs with "Egypt" jersey, but file doesn't exist
   - Impact: 3 NFTs missing (1,965 instead of 1,968)
   - Action: Need to either add file or remove from requirements

2. **Background Count Mismatch**: Requirements mention 7 backgrounds, but only 5 are in quotas
   - GAMBA DOGS and SpicerQQ backgrounds exist but not used in quotas
   - Action: Clarify if these should be included

3. **Batch ID Ranges**: Need to decide starting token ID
   - Option A: Start at 8000 for Batch 2 (8000-9964)
   - Option B: Start at 9000 for Batch 1 (9000-10964, exceeds range)
   - Option C: Use different range

## ✅ Code Functionality
- [x] Quota system implemented in `src/core/main.py`
- [x] Quota validation in `src/common/validate.py`
- [x] Config validation passes (`python main.py validate --config config.json --amount 1965`) ✅ VERIFIED
- [x] Generator can handle quota-based generation
- [x] All files verified to exist (`python verify_setup.py`) ✅ VERIFIED - NO ERRORS, NO WARNINGS

## 📋 Pre-Test Verification Steps

### 1. Validate Configuration
```bash
python main.py validate --config config.json --amount 1965
```
**Status**: ✅ PASSED (Verified: 2026-01-16)

### 2. Verify File Existence
```bash
python verify_setup.py
```
**Status**: ✅ PASSED (All 121 files verified, no errors, no warnings)

### 2. Verify File Existence
- [ ] Run script to verify all referenced PNG files exist
- [ ] Check for any filename mismatches (case sensitivity, special characters)

### 3. Test Small Generation
- [ ] Generate small test batch (e.g., 12 NFTs) to verify:
  - Images are created correctly
  - Metadata JSON files are correct
  - Layer composition works
  - Token IDs are correct

### 4. Verify Quota Distribution
- [ ] After test generation, verify:
  - Each Background+Shirt combination has correct count
  - Model×Headwear combinations are distributed correctly
  - No unexpected duplicates

## 🚀 Ready for Test Generation?

### Before Running Full Generation:
1. [ ] **Decide on starting token ID** (`--start-at` parameter)
   - For Batch 2: `--start-at 8000`
   - For Batch 1: `--start-at 9000`
   - Or custom range

2. [ ] **Resolve missing "Egypt" jersey** (3 NFTs)
   - Add file or adjust expectations

3. [ ] **Clarify background usage**
   - Should GAMBA DOGS and SpicerQQ be included?

4. [ ] **Set output directory**
   - Default: `./output`
   - Or specify: `--output ./gamba-dogs-output`

5. [ ] **Optional: Set seed for reproducibility**
   - `--seed <number>` for reproducible results

### Test Command (Small Batch):
```bash
python main.py generate --config config.json --amount 12 --output ./test-output --start-at 8000
```

### Full Generation Command (When Ready):
```bash
python main.py generate --config config.json --amount 1965 --output ./output --start-at 8000
```

## 📝 Notes
- Token IDs will be padded based on total amount (e.g., 1965 = 4 digits: 8000, 8001, ..., 9964)
- Images will be saved to `{output}/images/`
- Metadata will be saved to `{output}/metadata/`
- All metadata will also be in `{output}/metadata/all-objects.json`
