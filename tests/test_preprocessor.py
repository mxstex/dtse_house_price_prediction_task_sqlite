def test_preprocessor():
    from csv_processor.preprocessor import preprocess_housing_data

    # Sample input data with the target column
    test_csv = """longitude,latitude,housing_median_age,total_rooms,total_bedrooms,population,households,median_income,ocean_proximity,median_house_value
    -122.64,38.01,36.0,1336.0,258.0,678.0,249.0,5.5789,NEAR OCEAN,320201
    """

    # Write to a temporary file for testing
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.csv') as temp_file:
        temp_file.write(test_csv)
        temp_path = temp_file.name

    try:
        # Run the preprocessing function
        features, target = preprocess_housing_data(temp_path)

        # Validate the output
        assert features.shape == (1, len(features.columns)), "Features shape mismatch"
        assert target.shape == (1,), "Target shape mismatch"
        assert target.iloc[0] > 0, "Target value should be positive"
    finally:
        # Clean up the temporary file
        import os
        os.remove(temp_path)


def test_preprocessor_missing_target():
    from csv_processor.preprocessor import preprocess_housing_data
    import tempfile

    test_csv = """longitude,latitude,housing_median_age,total_rooms,total_bedrooms,population,households,median_income,ocean_proximity
    -122.64,38.01,36.0,1336.0,258.0,678.0,249.0,5.5789,NEAR OCEAN
    """
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.csv') as temp_file:
        temp_file.write(test_csv)
        temp_path = temp_file.name

    try:
        try:
            preprocess_housing_data(temp_path)
            assert False, "Preprocessing should fail without target column"
        except ValueError as e:
            assert "Target column 'median_house_value' not found" in str(e)
    finally:
        import os
        os.remove(temp_path)
