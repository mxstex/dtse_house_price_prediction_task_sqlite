def test_invalid_file_format():
    from csv_processor.preprocessor import preprocess_housing_data
    import tempfile

    # Create a temporary non-CSV file
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt') as temp_file:
        temp_file.write("Invalid data")
        temp_path = temp_file.name

    try:
        # Attempt to preprocess an invalid file
        preprocess_housing_data(temp_path)
        assert False, "Preprocessing should fail for invalid file format or insufficient columns"
    except ValueError as e:
        # Validate the expected error message
        assert "Invalid file format" in str(e) or "insufficient columns" in str(e), f"Unexpected error message: {e}"
    finally:
        import os
        os.remove(temp_path)

