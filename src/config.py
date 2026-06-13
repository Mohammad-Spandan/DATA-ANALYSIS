"""
Configuration settings for the agricultural crop analysis project.
"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
REPORTS_DIR = PROJECT_ROOT / "reports"
VIZ_DIR = PROJECT_ROOT / "visualizations"
LOGS_DIR = PROJECT_ROOT / "logs"

# Ensure directories exist
for directory in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, REPORTS_DIR, VIZ_DIR, LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Data configuration
RAW_DATA_FILE = RAW_DATA_DIR / "consolidated_crop_data.csv"
PROCESSED_DATA_FILE = PROCESSED_DATA_DIR / "processed_crop_data.csv"

# Analysis parameters
CROP_CATEGORIES = {
    "Major Crops": [1, 2, 3, 4, 5, 6, 7, 8],
    "Cereals": [9, 10, 11, 12],
    "Pulses": [13, 14, 15, 16, 17],
    "Condiments and Spices": [18, 19, 20],
    "Misc Cash Crops": [21, 22, 23, 24, 25, 26],
}

CROP_NAMES = {
    1: "Rice",
    2: "Jute",
    3: "Sugarcane",
    4: "Tea",
    5: "Pulses",
    6: "Oilseeds",
    7: "Condiments",
    8: "Tobacco",
    9: "Maize",
    10: "Jowar",
    11: "Barley",
    12: "Bajra",
    13: "Masur",
    14: "Moong",
    15: "Gram",
    16: "Mashkalai",
    17: "Arhar",
    18: "Chilies",
    19: "Onion",
    20: "Garlic",
    21: "Potato",
    22: "Sweet Potato",
    23: "Betelnut",
    24: "Cotton",
    25: "Hemp",
    26: "Mulberry",
}

# Visualization defaults
FIGURE_DPI = 300
FIGURE_SIZE = (12, 6)
STYLE = "seaborn-v0_8-darkgrid"
COLOR_PALETTE = "husl"

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
