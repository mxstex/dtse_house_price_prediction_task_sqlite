import os
import logging
from typing import List


# Filepaths
DATA_FILE: str = os.path.join("data", "housing.csv")
MODEL_FILE: str = os.path.join("models", "model.joblib")
DB_FILE: str = "housing_data.db"
PREDICTIONS_FILE: str = "predictions.csv"

# Used in preprocessor to work properly
TARGET_COLUMN = "median_house_value"

# Expected features for database schema
EXPECTED_FEATURES: List[str] = [
    'longitude', 'latitude', 'housing_median_age', 'total_rooms',
    'total_bedrooms', 'population', 'households', 'median_income',
    'ocean_proximity__LT_1H_OCEAN', 'ocean_proximity_INLAND',
    'ocean_proximity_ISLAND', 'ocean_proximity_NEAR_BAY',
    'ocean_proximity_NEAR_OCEAN'
]


# Logging Configuration
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_FILE = "app.log"

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set to DEBUG to capture all log levels

# File handler for logging to a file
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.INFO)  # Log INFO and above to the file
file_formatter = logging.Formatter(LOG_FORMAT)
file_handler.setFormatter(file_formatter)

# Console handler for logging to the terminal
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Log INFO and above to the console
console_formatter = logging.Formatter(LOG_FORMAT)
console_handler.setFormatter(console_formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
