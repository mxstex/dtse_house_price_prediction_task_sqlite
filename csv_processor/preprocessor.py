import pandas as pd
import numpy as np
from typing import Tuple
from config import EXPECTED_FEATURES, logger, TARGET_COLUMN

def preprocess_housing_data(input_data_path: str) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Preprocess the housing data to prepare it for model training or inference.

    Args:
        input_data_path (str): Path to the input CSV file.

    Returns:
        Tuple[pd.DataFrame, pd.Series]: Processed features (X) and target (y).

    Raises:
        FileNotFoundError: If the input file is not found.
        ValueError: If the target column is missing or the file format is invalid.
    """
    logger.info(f"Starting preprocessing for file: {input_data_path}")
    try:
        # Load the data
        df = pd.read_csv(input_data_path)
        logger.info(f"File {input_data_path} loaded successfully. Data shape: {df.shape}")
    except FileNotFoundError:
        logger.error(f"Input file not found at path: {input_data_path}")
        raise FileNotFoundError(f"Input file not found at path: {input_data_path}")
    except pd.errors.ParserError:
        logger.error(f"Invalid file format for file: {input_data_path}")
        raise ValueError(f"Invalid file format for file: {input_data_path}")
    except Exception as e:
        logger.error(f"Error loading file {input_data_path}: {e}")
        raise

    # Validate that the DataFrame has at least the expected minimum columns
    if df.shape[1] < 2:
        logger.error(f"Invalid file format or insufficient columns in file: {input_data_path}")
        raise ValueError(f"Invalid file format or insufficient columns in file: {input_data_path}")

    # Convert all column names to lowercase
    df.columns = df.columns.str.lower()
    logger.debug(f"Column names converted to lowercase: {list(df.columns)}")

    # Rename columns to match model training
    df.rename(columns={
        'lat': 'latitude',
        'bedrooms': 'total_bedrooms',
        'median_age': 'housing_median_age',
        'pop': 'population',
        'rooms': 'total_rooms',
    }, inplace=True)
    logger.debug(f"Columns renamed where applicable: {list(df.columns)}")

    # Convert 'YES'/'NO' to 1/0 for 'agency'
    if 'agency' in df.columns:
        df['agency'] = df['agency'].map({'YES': 1, 'NO': 0})
        logger.debug("'agency' column mapped to binary values.")

    # Handle categorical variables
    if "ocean_proximity" in df.columns:
        df = pd.get_dummies(df, columns=["ocean_proximity"], drop_first=True)
        logger.debug(f"Categorical 'ocean_proximity' column encoded. Columns now: {list(df.columns)}")
    else:
        logger.warning("'ocean_proximity' column not found. Skipping encoding.")

    # Handle missing or unexpected values
    df.replace("Null", 0, inplace=True)
    df.fillna(0, inplace=True)
    logger.debug("Missing or unexpected values handled (replaced 'Null', filled NaNs with 0).")

    # Define the target column
    target = TARGET_COLUMN
    if target not in df.columns:
        logger.error(f"Target column '{target}' not found in the dataset. Available columns: {list(df.columns)}")
        raise ValueError(f"Target column '{target}' not found in the dataset. Available columns: {list(df.columns)}")

    # Separate features and target
    y = df[target]
    X = df.drop(columns=[target])
    logger.info(f"Target column '{target}' separated. Features shape: {X.shape}, Target shape: {y.shape}")

    # Align with expected features
    for col in EXPECTED_FEATURES:
        if col not in X.columns:
            X[col] = 0  # Add missing columns as 0
            logger.debug(f"Missing column '{col}' added with default value 0.")
    X = X[EXPECTED_FEATURES]  # Filter columns to keep only expected features
    logger.info(f"Features aligned with expected schema. Final shape: {X.shape}")

    logger.info("Data preprocessing completed successfully.")
    return X, y
