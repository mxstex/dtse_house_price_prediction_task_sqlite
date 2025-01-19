def test_database_operations():
    from db_handler.db_connector import create_connection, close_connection
    from db_handler.db_query import create_cleaned_data_table, insert_cleaned_data

    # Setup: Create a temporary database
    db_path = "test_housing_data.db"
    conn = create_connection(db_path)

    # Example feature list
    features = ["col1", "col2", "col3", "col4", "col5", "col6", "col7", "col8"]

    try:
        # Test table creation
        create_cleaned_data_table(conn, features)

        # Debug: Check table schema
        cur = conn.cursor()
        cur.execute("PRAGMA table_info(cleaned_data)")
        print("Table Schema:", cur.fetchall())

        # Test data insertion (Include target value)
        sample_data = [("Test", 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 100.0)]  # Added target value
        insert_cleaned_data(conn, features, sample_data)

        # Debug: Query inserted data
        cur.execute("SELECT * FROM cleaned_data")
        print("Inserted Rows:", cur.fetchall())

        # Validate insertion
        cur.execute("SELECT COUNT(*) FROM cleaned_data")
        count = cur.fetchone()[0]
        assert count == 1, "Data insertion failed"

    finally:
        # Cleanup
        close_connection(conn)
        import os
        os.remove(db_path)

def test_database_connection_failure():
    from db_handler.db_connector import create_connection

    invalid_path = "/invalid/path/test.db"
    conn = create_connection(invalid_path)
    assert conn is None, "Connection should fail with invalid path"


def test_insert_empty_data():
    from db_handler.db_query import create_cleaned_data_table, insert_cleaned_data
    from db_handler.db_connector import create_connection, close_connection

    db_path = "test_empty_data.db"
    conn = create_connection(db_path)
    features = ["col1", "col2", "col3"]

    try:
        create_cleaned_data_table(conn, features)
        insert_cleaned_data(conn, features, [])  # Empty data
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM cleaned_data")
        assert cur.fetchone()[0] == 0, "No rows should be inserted for empty data"
    finally:
        close_connection(conn)
        import os
        os.remove(db_path)
