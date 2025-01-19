import sqlite3
from sqlite3 import Connection
from typing import Optional
from config import logger

def create_connection(db_file: str) -> Optional[Connection]:
    """
    Create a database connection to the SQLite database.

    Args:
        db_file (str): Path to the SQLite database file.

    Returns:
        Optional[Connection]: SQLite connection object if successful, None otherwise.
    """
    logger.info(f"Attempting to connect to database at {db_file}")
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        logger.info("Connection to SQLite DB successful")
    except sqlite3.Error as e:
        logger.error(f"Error connecting to database: {e}")
    return conn

def close_connection(conn: Optional[Connection]) -> None:
    """
    Close the database connection.

    Args:
        conn (Optional[Connection]): SQLite connection object to be closed.
    """
    if conn:
        try:
            conn.close()
            logger.info("Connection to SQLite DB closed")
        except sqlite3.Error as e:
            logger.error(f"Error closing database connection: {e}")
