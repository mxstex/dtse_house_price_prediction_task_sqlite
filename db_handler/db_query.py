import sqlite3
import pandas as pd
from sqlite3 import Connection
from typing import List, Tuple
from config import logger


def create_cleaned_data_table(conn: Connection, features: List[str]) -> None:
    """
    Create a table for storing cleaned housing data.

    Args:
        conn (Connection): SQLite connection object.
        features (List[str]): List of feature column names.

    Raises:
        sqlite3.Error: If table creation fails.
    """
    # Replace invalid characters with underscores
    sanitized_features = [
        feature.replace(" ", "_").replace("<", "_LT_").replace(">", "_GT_")
        for feature in features
    ]
    feature_columns = ", ".join([f"{feature} REAL" for feature in sanitized_features])
    query = f"""
    CREATE TABLE IF NOT EXISTS cleaned_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        {feature_columns},
        target REAL
    );
    """
    try:
        conn.execute(query)
        logger.info("Table 'cleaned_data' created successfully.")
    except sqlite3.Error as e:
        logger.error(f"Error creating table 'cleaned_data': {e}")
        raise


def insert_cleaned_data(
    conn: Connection, features: List[str], data: List[Tuple]
) -> None:
    """
    Insert preprocessed data into the cleaned_data table.

    Args:
        conn (Connection): SQLite connection object.
        features (List[str]): List of feature column names.
        data (List[Tuple]): List of data rows to insert, including target values.

    Raises:
        sqlite3.Error: If data insertion fails.
    """
    try:
        # Sanitize column names
        sanitized_features = [
            feature.replace(" ", "_").replace("<", "_LT_").replace(">", "_GT_")
            for feature in features
        ]
        columns = ", ".join(sanitized_features + ["target"])
        placeholders = ", ".join(["?"] * (len(features) + 1))  # +1 for the target
        query = f"INSERT INTO cleaned_data ({columns}) VALUES ({placeholders})"
        conn.executemany(query, data)
        conn.commit()
        logger.info(
            f"Inserted {len(data)} rows into 'cleaned_data' table successfully."
        )
    except sqlite3.Error as e:
        logger.error(f"Error inserting cleaned data: {e}")
        raise


def create_predictions_table(conn: Connection) -> None:
    """
    Create a table for storing predictions.

    Args:
        conn (Connection): SQLite connection object.

    Raises:
        sqlite3.Error: If table creation fails.
    """
    try:
        query = """
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            actual REAL,
            predicted REAL
        );
        """
        conn.execute(query)
        logger.info("Table 'predictions' created successfully.")
    except sqlite3.Error as e:
        logger.error(f"Error creating table 'predictions': {e}")
        raise


def insert_predictions(conn: Connection, data: List[Tuple[float, float]]) -> None:
    """
    Insert prediction results into the predictions table.

    Args:
        conn (Connection): SQLite connection object.
        data (List[Tuple[float, float]]): List of tuples with actual and predicted values.

    Raises:
        sqlite3.Error: If data insertion fails.
    """
    try:
        query = "INSERT INTO predictions (actual, predicted) VALUES (?, ?)"
        conn.executemany(query, data)
        conn.commit()
        logger.info(f"Inserted {len(data)} rows into 'predictions' table successfully.")
    except sqlite3.Error as e:
        logger.error(f"Error inserting predictions: {e}")
        raise


def get_cleaned_data(conn: Connection, table: str) -> pd.DataFrame:
    """
    Fetches all rows from a specified SQLite table and returns them as a pandas DataFrame.

    Parameters:
        conn (sqlite3.Connection): SQLite database connection object.
        table (str): Name of the table to query.

    Returns:
        pd.DataFrame: DataFrame containing the query results.
    """
    try:
        query = f"SELECT * FROM {table}"
        df = pd.read_sql_query(query, conn)
        print(f"Data fetched successfully from the '{table}' table.")
        return df
    except sqlite3.Error as e:
        print(f"Error fetching data from '{table}' table: {e}")
        raise


def insert_df_to_sqlite(conn: Connection, df: pd.DataFrame, table_name: str):
    """
    Inserts a pandas DataFrame into an SQLite table.

    Parameters:
        conn (sqlite3.Connection): SQLite database connection object.
        df (pd.DataFrame): DataFrame to insert into the SQLite database.
        table_name (str): Name of the table to insert the data into.

    Raises:
        ValueError: If the DataFrame is empty.
    """
    if df.empty:
        raise ValueError("The DataFrame is empty and cannot be inserted into the database.")

    # Infer SQL table schema from the DataFrame and insert data
    try:
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Data inserted successfully into the '{table_name}' table.")
    except Exception as e:
        print(f"An error occurred while inserting data into the '{table_name}' table: {e}")