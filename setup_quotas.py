"""
Script to generate config.json with quotas from the allocation table.
Includes reserved NFTs (1/1s and unique Gamba Dogs).
"""

import json
import sys
from setup_reserved import generate_reserved_section

# Background name mapping (table name -> filename without .png)
BACKGROUND_MAP = {
    "Poor": "POOR",
    "NFT's are dead": "NFTs ARE DEAD",  # Note: filename has no apostrophe
    "Solana": "SOLANA",
    "Bet it like": "BET IT LIKE",
    "Allergic to money": "ALLERGIC TO MONEY"
}

# Table data: (Rarity, Background, Shirt Type, Shirt Name, Amount)
TABLE_DATA = [
    # Common - Poor
    ("Common", "Poor", "Basic Shirt", "Basic Blue", 12),
    ("Common", "Poor", "Basic Shirt", "Basic Brown", 12),
    ("Common", "Poor", "Basic Shirt", "Basic Dark Blue", 12),
    ("Common", "Poor", "Basic Shirt", "Basic Green", 12),
    ("Common", "Poor", "Basic Shirt", "Basic Grey", 12),
    ("Common", "Poor", "Basic Shirt", "Basic Light Blue", 12),
    ("Common", "Poor", "Basic Shirt", "Basic Magenta", 12),
    ("Common", "Poor", "Basic Shirt", "Basic Mint", 12),
    ("Common", "Poor", "Basic Shirt", "Basic Pink", 12),
    ("Common", "Poor", "Basic Shirt", "Basic Purple", 12),
    ("Common", "Poor", "Basic Shirt", "Basic Red", 12),
    ("Common", "Poor", "Basic Shirt", "Basic Sky Blue", 12),
    ("Common", "Poor", "Basic Shirt", "Basic Yellow", 12),
    ("Common", "Poor", "Basic Shirt", "Polo Black&White", 12),
    ("Common", "Poor", "Basic Shirt", "Polo Black", 12),
    ("Common", "Poor", "Basic Shirt", "Polo Blue&Red", 12),
    ("Common", "Poor", "Basic Shirt", "Polo Blue&White", 12),
    ("Common", "Poor", "Basic Shirt", "Polo Blue&Yellow", 12),
    ("Common", "Poor", "Basic Shirt", "Polo Blue", 12),
    ("Common", "Poor", "Basic Shirt", "Polo Brown", 12),
    ("Common", "Poor", "Basic Shirt", "Polo Dark Blue", 12),
    ("Common", "Poor", "Basic Shirt", "Polo Dark Grey", 12),
    ("Common", "Poor", "Basic Shirt", "Polo Green&White", 12),
    ("Common", "Poor", "Basic Shirt", "Polo Green", 12),
    ("Common", "Poor", "Basic Shirt", "Polo Grey", 12),
    ("Common", "Poor", "Basic Shirt", "Polo Light Blue", 12),
    ("Common", "Poor", "Basic Shirt", "Polo Lime", 12),
    ("Common", "Poor", "Basic Shirt", "Polo Magenta", 12),
    ("Common", "Poor", "Basic Shirt", "Polo Mint", 12),
    ("Common", "Poor", "Basic Shirt", "Polo Orange", 12),
    ("Common", "Poor", "Basic Shirt", "Polo Pink", 12),
    ("Common", "Poor", "Basic Shirt", "Polo Purple", 12),
    ("Common", "Poor", "Basic Shirt", "Polo Red&Black", 12),
    ("Common", "Poor", "Basic Shirt", "Polo Red&White", 12),
    ("Common", "Poor", "Basic Shirt", "Polo Red&Yellow", 12),
    ("Common", "Poor", "Basic Shirt", "Polo Red", 12),
    ("Common", "Poor", "Basic Shirt", "Polo Turquoise", 12),
    ("Common", "Poor", "Basic Shirt", "Polo White&Black", 12),
    ("Common", "Poor", "Basic Shirt", "Polo White&Blue", 12),
    ("Common", "Poor", "Basic Shirt", "Polo White&Red", 12),
    ("Common", "Poor", "Basic Shirt", "Polo White", 12),
    ("Common", "Poor", "Basic Shirt", "Polo Yellow", 12),
    ("Common", "Poor", "Basic Shirt", "Striped Blue", 12),
    ("Common", "Poor", "Basic Shirt", "Striped Green", 12),
    ("Common", "Poor", "Basic Shirt", "Striped Light Blue", 12),
    ("Common", "Poor", "Basic Shirt", "Striped Lime", 12),
    ("Common", "Poor", "Basic Shirt", "Striped Mint", 12),
    ("Common", "Poor", "Basic Shirt", "Striped Neon", 12),
    ("Common", "Poor", "Basic Shirt", "Striped Pink", 12),
    ("Common", "Poor", "Basic Shirt", "Striped Purple", 12),
    ("Common", "Poor", "Basic Shirt", "Striped Red", 12),
    ("Common", "Poor", "Basic Shirt", "Striped Turquoise", 12),
    ("Common", "Poor", "Basic Shirt", "Striped Yellow", 12),
    ("Common", "Poor", "Basic Shirt", "Striped Sky Blue", 12),
    ("Common", "Poor", "Basic Shirt", "V-Neck Blue", 12),
    ("Common", "Poor", "Basic Shirt", "V-Neck Light Blue", 12),
    ("Common", "Poor", "Basic Shirt", "V-Neck Magenta", 12),
    ("Common", "Poor", "Basic Shirt", "V-Neck Mint", 12),
    ("Common", "Poor", "Basic Shirt", "V-Neck Orange", 12),
    ("Common", "Poor", "Basic Shirt", "V-Neck Pink", 12),
    ("Common", "Poor", "Basic Shirt", "V-Neck Purple", 12),
    ("Common", "Poor", "Basic Shirt", "V-Neck Red", 12),
    ("Common", "Poor", "Basic Shirt", "V-Neck Turquoise", 12),
    ("Common", "Poor", "Basic Shirt", "V-Neck White", 12),
    ("Common", "Poor", "Basic Shirt", "V-Neck Yellow", 12),
    # Uncommon - NFT's are dead
    ("Uncommon", "NFT's are dead", "Country Jersey", "Argentina Jersey", 7),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Germany Jersey", 7),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Brazil Jersey", 7),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Italy Jersey", 7),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Spain Jersey", 7),
    ("Uncommon", "NFT's are dead", "Country Jersey", "France Jersey", 7),
    ("Uncommon", "NFT's are dead", "Country Jersey", "England Jersey", 7),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Portugal Jersey", 7),
    ("Uncommon", "NFT's are dead", "Country Jersey", "USA Jersey", 7),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Japan Jersey", 7),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Holland Jersey", 7),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Mexico Jersey", 7),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Canada Jersey", 7),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Belgium Jersey", 6),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Croatia Jersey", 6),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Morocco Jersey", 6),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Nigeria Jersey", 6),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Poland Jersey", 6),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Sweden Jersey", 6),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Switzerland Jersey", 6),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Turkey Jersey", 6),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Uruguay Jersey", 6),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Algeria Jersey", 6),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Ghana Jersey", 6),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Serbia Jersey", 6),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Colombia Jersey", 6),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Hungary Jersey", 6),
    ("Uncommon", "NFT's are dead", "Country Jersey", "South Korea Jersey", 6),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Senegal Jersey", 6),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Australia Jersey", 5),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Panama Jersey", 5),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Tunesia Jersey", 5),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Norway Jersey", 5),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Scotland Jersey", 5),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Saudi Arabia Jersey", 5),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Ecuador Jersey", 5),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Ivory Coast Jersey", 5),
    ("Uncommon", "NFT's are dead", "Country Jersey", "South Africa Jersey", 5),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Paraguay Jersey", 5),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Austria Jersey", 5),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Jordan Jersey", 4),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Iran Jersey", 4),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Uzbekistan Jersey", 4),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Curacao Jersey", 4),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Cape Verde Jersey", 4),
    ("Uncommon", "NFT's are dead", "Country Jersey", "New Zealand Jersey", 4),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Haiti Jersey", 4),
    ("Uncommon", "NFT's are dead", "Country Jersey", "China Jersey", 4),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Russia Jersey", 4),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Georgia Jersey", 4),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Czech Jersey", 4),
    ("Uncommon", "NFT's are dead", "Country Jersey", "Thailand Jersey", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Basic Blue", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Basic Brown", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Basic Dark Blue", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Basic Green", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Basic Grey", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Basic Light Blue", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Basic Magenta", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Basic Mint", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Basic Pink", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Basic Purple", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Basic Red", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Basic Sky Blue", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Basic Yellow", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Polo Black&White", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Polo Black", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Polo Blue&Red", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Polo Blue&White", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Polo Blue&Yellow", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Polo Blue", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Polo Brown", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Polo Dark Blue", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Polo Dark Grey", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Polo Green&White", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Polo Green", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Polo Grey", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Polo Light Blue", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Polo Lime", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Polo Magenta", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Polo Mint", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Polo Orange", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Polo Pink", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Polo Purple", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Polo Red&Black", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Polo Red&White", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Polo Red&Yellow", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Polo Red", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Polo Turquoise", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Polo White&Black", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Polo White&Blue", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Polo White&Red", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Polo White", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Polo Yellow", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Striped Blue", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Striped Green", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Striped Light Blue", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Striped Lime", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Striped Mint", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Striped Neon", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Striped Pink", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Striped Purple", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Striped Red", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Striped Turquoise", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Striped Yellow", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "Striped Sky Blue", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "V-Neck Blue", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "V-Neck Light Blue", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "V-Neck Magenta", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "V-Neck Mint", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "V-Neck Orange", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "V-Neck Pink", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "V-Neck Purple", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "V-Neck Red", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "V-Neck Turquoise", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "V-Neck White", 4),
    ("Uncommon", "NFT's are dead", "Basic Shirt", "V-Neck Yellow", 4),
    # Rare - Solana
    ("Rare", "Solana", "Country Jersey", "Germany Jersey", 6),
    ("Rare", "Solana", "Country Jersey", "Brazil Jersey", 6),
    ("Rare", "Solana", "Country Jersey", "Argentina Jersey", 6),
    ("Rare", "Solana", "Country Jersey", "England Jersey", 6),
    ("Rare", "Solana", "Country Jersey", "France Jersey", 6),
    ("Rare", "Solana", "Country Jersey", "Spain Jersey", 6),
    ("Rare", "Solana", "Country Jersey", "Italy Jersey", 5),
    ("Rare", "Solana", "Country Jersey", "Turkey Jersey", 5),
    ("Rare", "Solana", "Country Jersey", "Russia Jersey", 5),
    ("Rare", "Solana", "Country Jersey", "Portugal Jersey", 5),
    ("Rare", "Solana", "Country Jersey", "Holland Jersey", 5),
    ("Rare", "Solana", "Country Jersey", "Mexico Jersey", 5),
    ("Rare", "Solana", "Country Jersey", "USA Jersey", 5),
    ("Rare", "Solana", "Country Jersey", "Japan Jersey", 5),
    ("Rare", "Solana", "Country Jersey", "Belgium Jersey", 5),
    ("Rare", "Solana", "Country Jersey", "Croatia Jersey", 5),
    ("Rare", "Solana", "Country Jersey", "Uruguay Jersey", 5),
    ("Rare", "Solana", "Country Jersey", "Colombia Jersey", 5),
    ("Rare", "Solana", "Country Jersey", "South Korea Jersey", 5),
    ("Rare", "Solana", "Country Jersey", "Morocco Jersey", 5),
    ("Rare", "Solana", "Country Jersey", "Nigeria Jersey", 4),
    ("Rare", "Solana", "Country Jersey", "Poland Jersey", 4),
    ("Rare", "Solana", "Country Jersey", "Sweden Jersey", 4),
    ("Rare", "Solana", "Country Jersey", "Switzerland Jersey", 4),
    ("Rare", "Solana", "Country Jersey", "Serbia Jersey", 4),
    ("Rare", "Solana", "Country Jersey", "Austria Jersey", 3),
    ("Rare", "Solana", "Country Jersey", "Ghana Jersey", 3),
    ("Rare", "Solana", "Country Jersey", "Senegal Jersey", 3),
    ("Rare", "Solana", "Country Jersey", "Australia Jersey", 3),
    ("Rare", "Solana", "Country Jersey", "China Jersey", 3),
    ("Rare", "Solana", "Country Jersey", "Iran Jersey", 3),
    ("Rare", "Solana", "Country Jersey", "Canada Jersey", 3),
    ("Rare", "Solana", "Country Jersey", "Russia Jersey", 3),
    ("Rare", "Solana", "Basic Shirt", "Basic Blue", 3),
    ("Rare", "Solana", "Basic Shirt", "Basic Brown", 3),
    ("Rare", "Solana", "Basic Shirt", "Basic Dark Blue", 3),
    ("Rare", "Solana", "Basic Shirt", "Basic Green", 3),
    ("Rare", "Solana", "Basic Shirt", "Basic Grey", 3),
    ("Rare", "Solana", "Basic Shirt", "Basic Light Blue", 3),
    ("Rare", "Solana", "Basic Shirt", "Basic Magenta", 3),
    ("Rare", "Solana", "Basic Shirt", "Basic Mint", 3),
    ("Rare", "Solana", "Basic Shirt", "Basic Pink", 3),
    ("Rare", "Solana", "Basic Shirt", "Basic Purple", 3),
    ("Rare", "Solana", "Basic Shirt", "Basic Red", 3),
    ("Rare", "Solana", "Basic Shirt", "Basic Sky Blue", 4),
    ("Rare", "Solana", "Basic Shirt", "Basic Yellow", 4),
    ("Rare", "Solana", "Basic Shirt", "Polo Black&White", 4),
    ("Rare", "Solana", "Basic Shirt", "Polo Black", 4),
    ("Rare", "Solana", "Basic Shirt", "Polo Blue&Red", 3),
    ("Rare", "Solana", "Basic Shirt", "Polo Blue&White", 3),
    ("Rare", "Solana", "Basic Shirt", "Polo Blue&Yellow", 3),
    ("Rare", "Solana", "Basic Shirt", "Polo Blue", 4),
    ("Rare", "Solana", "Basic Shirt", "Polo Brown", 4),
    ("Rare", "Solana", "Basic Shirt", "Polo Dark Blue", 4),
    ("Rare", "Solana", "Basic Shirt", "Polo Dark Grey", 4),
    ("Rare", "Solana", "Basic Shirt", "Polo Green&White", 3),
    ("Rare", "Solana", "Basic Shirt", "Polo Green", 3),
    ("Rare", "Solana", "Basic Shirt", "Polo Grey", 3),
    ("Rare", "Solana", "Basic Shirt", "Polo Light Blue", 3),
    ("Rare", "Solana", "Basic Shirt", "Polo Lime", 3),
    ("Rare", "Solana", "Basic Shirt", "Polo Magenta", 3),
    ("Rare", "Solana", "Basic Shirt", "Polo Mint", 3),
    ("Rare", "Solana", "Basic Shirt", "Polo Orange", 3),
    ("Rare", "Solana", "Basic Shirt", "Polo Pink", 3),
    ("Rare", "Solana", "Basic Shirt", "Polo Purple", 4),
    ("Rare", "Solana", "Basic Shirt", "Polo Red&Black", 3),
    ("Rare", "Solana", "Basic Shirt", "Polo Red&White", 3),
    ("Rare", "Solana", "Basic Shirt", "Polo Red&Yellow", 3),
    ("Rare", "Solana", "Basic Shirt", "Polo Red", 3),
    ("Rare", "Solana", "Basic Shirt", "Polo Turquoise", 3),
    ("Rare", "Solana", "Basic Shirt", "Polo White&Black", 3),
    ("Rare", "Solana", "Basic Shirt", "Polo White&Blue", 3),
    ("Rare", "Solana", "Basic Shirt", "Polo White&Red", 3),
    ("Rare", "Solana", "Basic Shirt", "Polo White", 4),
    ("Rare", "Solana", "Basic Shirt", "Polo Yellow", 4),
    ("Rare", "Solana", "Basic Shirt", "Striped Blue", 3),
    ("Rare", "Solana", "Basic Shirt", "Striped Green", 3),
    ("Rare", "Solana", "Basic Shirt", "Striped Light Blue", 2),
    ("Rare", "Solana", "Basic Shirt", "Striped Lime", 3),
    ("Rare", "Solana", "Basic Shirt", "Striped Mint", 3),
    ("Rare", "Solana", "Basic Shirt", "Striped Neon", 2),
    ("Rare", "Solana", "Basic Shirt", "Striped Pink", 2),
    ("Rare", "Solana", "Basic Shirt", "Striped Purple", 2),
    ("Rare", "Solana", "Basic Shirt", "Striped Red", 3),
    ("Rare", "Solana", "Basic Shirt", "Striped Turquoise", 3),
    ("Rare", "Solana", "Basic Shirt", "Striped Yellow", 2),
    ("Rare", "Solana", "Basic Shirt", "Striped Sky Blue", 2),
    ("Rare", "Solana", "Basic Shirt", "V-Neck Blue", 3),
    ("Rare", "Solana", "Basic Shirt", "V-Neck Light Blue", 3),
    ("Rare", "Solana", "Basic Shirt", "V-Neck Magenta", 3),
    ("Rare", "Solana", "Basic Shirt", "V-Neck Mint", 3),
    ("Rare", "Solana", "Basic Shirt", "V-Neck Orange", 3),
    ("Rare", "Solana", "Basic Shirt", "V-Neck Pink", 3),
    ("Rare", "Solana", "Basic Shirt", "V-Neck Purple", 3),
    ("Rare", "Solana", "Basic Shirt", "V-Neck Red", 3),
    ("Rare", "Solana", "Basic Shirt", "V-Neck Turquoise", 3),
    ("Rare", "Solana", "Basic Shirt", "V-Neck White", 3),
    ("Rare", "Solana", "Basic Shirt", "V-Neck Yellow", 3),
    # Super Rare - Bet it like
    ("Super Rare", "Bet it like", "Country Jersey", "Germany Jersey", 6),
    ("Super Rare", "Bet it like", "Country Jersey", "Brazil Jersey", 6),
    ("Super Rare", "Bet it like", "Country Jersey", "Argentina Jersey", 6),
    ("Super Rare", "Bet it like", "Country Jersey", "England Jersey", 6),
    ("Super Rare", "Bet it like", "Country Jersey", "France Jersey", 6),
    ("Super Rare", "Bet it like", "Country Jersey", "Spain Jersey", 6),
    ("Super Rare", "Bet it like", "Country Jersey", "Italy Jersey", 6),
    ("Super Rare", "Bet it like", "Country Jersey", "Turkey Jersey", 6),
    ("Super Rare", "Bet it like", "Country Jersey", "Russia Jersey", 6),
    ("Super Rare", "Bet it like", "Country Jersey", "Portugal Jersey", 5),
    ("Super Rare", "Bet it like", "Country Jersey", "Holland Jersey", 5),
    ("Super Rare", "Bet it like", "Country Jersey", "Mexico Jersey", 5),
    ("Super Rare", "Bet it like", "Country Jersey", "USA Jersey", 5),
    ("Super Rare", "Bet it like", "Country Jersey", "Japan Jersey", 5),
    ("Super Rare", "Bet it like", "Country Jersey", "Belgium Jersey", 5),
    ("Super Rare", "Bet it like", "Country Jersey", "Croatia Jersey", 5),
    ("Super Rare", "Bet it like", "Country Jersey", "Uruguay Jersey", 5),
    ("Super Rare", "Bet it like", "Country Jersey", "Colombia Jersey", 4),
    ("Super Rare", "Bet it like", "Country Jersey", "South Korea Jersey", 4),
    ("Super Rare", "Bet it like", "Country Jersey", "Morocco Jersey", 4),
    ("Super Rare", "Bet it like", "Country Jersey", "Nigeria Jersey", 4),
    ("Super Rare", "Bet it like", "Country Jersey", "Canada Jersey", 4),
    ("Super Rare", "Bet it like", "Country Jersey", "Poland Jersey", 4),
    ("Super Rare", "Bet it like", "Country Jersey", "Sweden Jersey", 4),
    ("Super Rare", "Bet it like", "Country Jersey", "Switzerland Jersey", 4),
    ("Super Rare", "Bet it like", "Country Jersey", "Serbia Jersey", 4),
    ("Super Rare", "Bet it like", "Country Jersey", "Austria Jersey", 4),
    ("Super Rare", "Bet it like", "Country Jersey", "Ghana Jersey", 4),
    ("Super Rare", "Bet it like", "Country Jersey", "Senegal Jersey", 3),
    ("Super Rare", "Bet it like", "Country Jersey", "Australia Jersey", 3),
    # Note: "Egypt" jersey doesn't exist in files, skipping
    # ("Super Rare", "Bet it like", "Country Jersey", "Egypt", 3),
    ("Super Rare", "Bet it like", "Country Jersey", "Iran Jersey", 3),
    ("Super Rare", "Bet it like", "Basic Shirt", "Basic Blue", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Basic Brown", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Basic Dark Blue", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Basic Green", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Basic Grey", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Basic Light Blue", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Basic Magenta", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Basic Mint", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Basic Pink", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Basic Purple", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Basic Red", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Basic Sky Blue", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Basic Yellow", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Polo Black&White", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Polo Black", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Polo Blue&Red", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Polo Blue&White", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Polo Blue&Yellow", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Polo Blue", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Polo Brown", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Polo Dark Blue", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Polo Dark Grey", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Polo Green&White", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Polo Grey", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Polo Light Blue", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Polo Magenta", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Polo Orange", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Polo Pink", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Polo Purple", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Polo Red&Yellow", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Polo Red", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Polo Turquoise", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Polo White&Black", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Polo White&Blue", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Polo White&Red", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Polo White", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "V-Neck Blue", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Striped Red", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Striped Mint", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "Striped Turquoise", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "V-Neck Light Blue", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "V-Neck Magenta", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "V-Neck Mint", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "V-Neck Orange", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "V-Neck Pink", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "V-Neck Purple", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "V-Neck Red", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "V-Neck Turquoise", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "V-Neck White", 1),
    ("Super Rare", "Bet it like", "Basic Shirt", "V-Neck Yellow", 1),
    # Epic - Allergic to money
    ("Epic", "Allergic to money", "Country Jersey", "Germany Jersey", 5),
    ("Epic", "Allergic to money", "Country Jersey", "Brazil Jersey", 5),
    ("Epic", "Allergic to money", "Country Jersey", "Argentina Jersey", 5),
    ("Epic", "Allergic to money", "Country Jersey", "England Jersey", 5),
    ("Epic", "Allergic to money", "Country Jersey", "France Jersey", 4),
    ("Epic", "Allergic to money", "Country Jersey", "Spain Jersey", 4),
    ("Epic", "Allergic to money", "Country Jersey", "Italy Jersey", 3),
    ("Epic", "Allergic to money", "Country Jersey", "Turkey Jersey", 3),
    ("Epic", "Allergic to money", "Country Jersey", "Russia Jersey", 3),
    ("Epic", "Allergic to money", "Country Jersey", "Portugal Jersey", 3),
    ("Epic", "Allergic to money", "Country Jersey", "Holland Jersey", 2),
    ("Epic", "Allergic to money", "Country Jersey", "Mexico Jersey", 2),
    ("Epic", "Allergic to money", "Country Jersey", "USA Jersey", 2),
    ("Epic", "Allergic to money", "Country Jersey", "Japan Jersey", 1),
    ("Epic", "Allergic to money", "Country Jersey", "Belgium Jersey", 1),
    ("Epic", "Allergic to money", "Country Jersey", "Croatia Jersey", 1),
    ("Epic", "Allergic to money", "Country Jersey", "Uruguay Jersey", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "Basic Blue", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "Basic Brown", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "Basic Dark Blue", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "Basic Green", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "Basic Grey", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "Basic Light Blue", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "Basic Mint", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "Basic Purple", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "Basic Red", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "Basic Sky Blue", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "Basic Yellow", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "Polo Black&White", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "Polo Black", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "Polo Blue&Red", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "Polo Blue&White", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "Polo Blue&Yellow", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "Polo Blue", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "Polo Brown", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "Polo Dark Blue", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "Polo Dark Grey", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "Polo Green&White", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "Polo Green", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "Polo Grey", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "Polo Light Blue", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "Polo Lime", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "Polo Mint", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "Striped Red", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "Striped Mint", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "Striped Turquoise", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "Polo Red&White", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "Polo Red", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "Polo White", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "V-Neck Blue", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "V-Neck Light Blue", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "V-Neck Mint", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "V-Neck Turquoise", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "V-Neck White", 1),
    ("Epic", "Allergic to money", "Basic Shirt", "V-Neck Yellow", 1),
]

def generate_config():
    """Generate the complete config.json with quotas."""
    
    # Build quotas from table data
    quotas = []
    for rarity, background, shirt_type, shirt_name, amount in TABLE_DATA:
        # Map background name to filename
        bg_filename = BACKGROUND_MAP.get(background, background.upper())
        
        # Shirt name should match layer value (not filename)
        # The filename mapping is handled in the layer definition
        # Keep shirt_name as-is for quota (matches layer value)
        shirt_filename = shirt_name
        
        quotas.append({
            "background": bg_filename,
            "shirt": shirt_filename,
            "amount": amount
        })
    
    # Get reserved NFT data
    reserved = generate_reserved_section()
    
    # Get unique backgrounds - include GAMBA DOGS and SpicerQQ from reserved NFTs
    unique_backgrounds = sorted(set(BACKGROUND_MAP.values()))
    # Add GAMBA DOGS and SpicerQQ if not already present
    reserved_backgrounds = set()
    for entry in reserved["fixed"] + reserved["random"]:
        reserved_backgrounds.add(entry["background"])
    unique_backgrounds = sorted(set(unique_backgrounds) | reserved_backgrounds)
    
    # Get unique shirts - include 1/1 jerseys and Egypt placeholder from reserved NFTs
    unique_shirts = sorted(set(shirt_name for _, _, _, shirt_name, _ in TABLE_DATA))
    # Add 1/1 jerseys and Egypt from reserved NFTs
    reserved_jerseys = set()
    for entry in reserved["fixed"] + reserved["random"]:
        reserved_jerseys.add(entry["jersey"])
    # Add Egypt placeholder
    reserved_jerseys.add("Egypt Jersey")
    unique_shirts = sorted(set(unique_shirts) | reserved_jerseys)
    
    # Fix filename mismatches - ensure layer values match actual filenames
    jersey_filename_map = {}
    jersey_filenames = []
    for jersey in unique_shirts:
        if jersey == "V-Neck Orange":
            jersey_filename_map[jersey] = "V-Neck orange"  # File is lowercase
            jersey_filenames.append("V-Neck orange")
        elif jersey == "Egypt Jersey":
            # Placeholder - file doesn't exist yet
            jersey_filename_map[jersey] = "Egypt Jersey"
            jersey_filenames.append("Egypt Jersey")
        elif jersey.endswith(" 1 of 1"):
            # 1/1 jerseys - filename matches value
            jersey_filename_map[jersey] = jersey
            jersey_filenames.append(jersey)
        else:
            jersey_filename_map[jersey] = jersey
            jersey_filenames.append(jersey)
    
    # Calculate total NFTs
    total_nfts = sum(amount for _, _, _, _, amount in TABLE_DATA)
    
    # Create config
    # Layer order determines stacking order: Background (bottom) -> Model -> Jersey -> Headwear (top)
    config = {
        "layers": [
            {
                "name": "Background",
                "values": unique_backgrounds,
                "trait_path": "./trait-layers/backgrounds",
                "filename": unique_backgrounds,
                "weights": [100.0 / len(unique_backgrounds)] * len(unique_backgrounds)
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
                "values": unique_shirts,
                "trait_path": "./trait-layers/JERSEYS-SHIRTS",
                "filename": jersey_filenames,
                "weights": [100.0 / len(unique_shirts)] * len(unique_shirts)
            },
            {
                "name": "Headwear",
                "values": ["White Cap", "Black Cap", "Grey Cap", "No Cap"],
                "trait_path": "./trait-layers/HEADWEAR",
                "filename": ["White Cap", "Black Cap", "Grey Cap", "No Cap"],
                "weights": [16.67, 16.67, 16.66, 50.0]
            }
        ],
        "quotas": quotas,
        "reserved": reserved,
        "incompatibilities": [],
        "baseURI": ".",
        "name": "Gamba Dog #",
        "description": "The most exclusive Gamba community.",
        "symbol": "GMB"
    }
    
    # Write to file
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    # Configure stdout for Unicode on Windows
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8')
    
    print("Generated config.json")
    print(f"  - {len(quotas)} quota entries")
    print(f"  - Total quota NFTs: {total_nfts}")
    print(f"  - Reserved NFTs (fixed): {len(reserved['fixed'])}")
    print(f"  - Reserved NFTs (random): {len(reserved['random'])}")
    print(f"  - Total NFTs: {total_nfts + len(reserved['fixed']) + len(reserved['random'])}")
    print(f"  - Unique backgrounds: {len(unique_backgrounds)}")
    print(f"  - Unique shirts: {len(unique_shirts)}")
    
    return config

if __name__ == "__main__":
    generate_config()
