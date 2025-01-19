# Import configuration variables
from config import DATA_FILE, MODEL_FILE, DB_FILE, PREDICTIONS_FILE, EXPECTED_FEATURES, logger

from typing import List, Tuple
import pandas as pd
import os

from csv_processor.preprocessor import preprocess_housing_data
from models.model import load_model, predict
from sklearn.metrics import mean_absolute_error
from db_handler.db_connector import create_connection, close_connection
from db_handler.db_query import (
    create_cleaned_data_table,
    create_predictions_table,
    insert_cleaned_data,
    insert_predictions
)

def run_pipeline() -> None:
    """
    Main function to run the house price prediction pipeline.
    Includes preprocessing, database insertion, prediction, and saving outputs.
    """
    logger.info("Starting the house price prediction pipeline...")
    conn = None

    try:
        # Step 1: Preprocess the data
        logger.info("Step 1: Preprocessing data...")
        features, target = preprocess_housing_data(DATA_FILE)
        logger.info(f"Preprocessing completed. Features shape: {features.shape}, Target size: {len(target)}")
        
        # Combine features and target into tuples for database insertion
        cleaned_data: List[Tuple] = [(*features.iloc[i], target.iloc[i]) for i in range(len(features))]

        # Step 2: Ingest data into SQLite database
        logger.info("Step 2: Connecting to the database...")
        conn = create_connection(DB_FILE)

        logger.info("Creating tables in the database...")
        create_cleaned_data_table(conn, EXPECTED_FEATURES)
        create_predictions_table(conn)

        logger.info("Inserting cleaned data into the database...")
        insert_cleaned_data(conn, EXPECTED_FEATURES, cleaned_data)
        logger.info(f"Inserted {len(cleaned_data)} rows into the database.")

        # Step 3: Load the trained model
        logger.info("Step 3: Loading the trained model...")
        model = load_model(MODEL_FILE)

        # Step 4: Make predictions
        logger.info("Step 4: Making predictions using the model...")
        predictions = predict(features, model)
        logger.info(f"Predictions completed. Number of predictions: {len(predictions)}")

        # Step 5: Evaluate model performance
        logger.info("Step 5: Evaluating model performance...")
        error = mean_absolute_error(target, predictions)
        logger.info(f"Mean Absolute Error (MAE): {error}")

        # Step 6: Save predictions to a CSV file
        logger.info("Step 6: Saving predictions to a CSV file...")
        predictions_df = pd.DataFrame({
            "Actual": target,
            "Predicted": predictions
        })
        predictions_df.to_csv(PREDICTIONS_FILE, index=False)
        logger.info(f"Predictions saved to {PREDICTIONS_FILE}")

        # Step 7: Save predictions to SQLite database
        logger.info("Step 7: Saving predictions to the database...")
        prediction_data: List[Tuple] = [(target.iloc[i], predictions[i]) for i in range(len(predictions))]
        insert_predictions(conn, prediction_data)
        logger.info("Predictions saved to the database.")

        # Display the first few predictions
        logger.debug("Predictions (first 5 rows):")
        logger.debug(f"\n{predictions_df.head()}")

    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        raise  # Re-raise the exception
    except pd.errors.EmptyDataError as e:
        logger.error(f"Data error: {e}")
        raise  # Re-raise the exception
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise  # Re-raise the exception
    finally:
        if conn:
            logger.info("Closing database connection...")
            close_connection(conn)

if __name__ == "__main__":
    run_pipeline()
