def test_full_pipeline():
    from main import run_pipeline

    # Run the pipeline
    run_pipeline()

    # Validate outputs (e.g., check predictions.db or predictions.csv)
    import os
    assert os.path.exists("predictions.csv"), "Predictions file not generated"
    assert os.path.exists("housing_data.db"), "Database file not generated"