# House Price Prediction Pipeline

This project demonstrates a robust data pipeline for processing housing data, generating predictions using a pre-trained model, and storing results in a database. The solution is implemented in Python and integrates essential software engineering best practices like logging, testing, and modular design.

---

## **Overview**

The pipeline performs the following steps:
1. **Preprocessing Input Data**:
   - Loads raw housing data (`housing.csv`).
   - Cleans and transforms data to align with the model's requirements.
   - Handles missing values and encodes categorical variables.

2. **Database Integration**:
   - Stores cleaned data in an SQLite database (`housing_data.db`).
   - Creates tables for cleaned data and predictions.

3. **Prediction Generation**:
   - Uses a pre-trained model (`model.joblib`) to generate house price predictions.
   - Saves predictions to the database and a CSV file (`predictions.csv`).

4. **Logging**:
   - Tracks operations and errors using Python’s `logging` module.

5. **Testing**:
   - Includes comprehensive unit tests for key modules and functionalities.

---

## **Setup Instructions**

### **1. Install Dependencies**

Ensure you have Python 3.9 installed. Install the required dependencies using `pip`:
```bash
pip install -r requirements.txt
```

### **2. Prepare the Environment**

Ensure the following files are available in the project directory:
- `data/housing.csv`: Input data file.
- `models/model.joblib`: Pre-trained model file.

### **3. Run the Pipeline**

Execute the pipeline using:
```bash
python main.py
```

This will:
- Process the input data.
- Store the cleaned data in `housing_data.db`.
- Generate predictions and save them in `predictions.csv` and `housing_data.db`.

---

## **Project Structure**

```
House_price_prediction_lite/
|-- config.py                # Configuration and logging setup
|-- main.py                  # Main script for pipeline execution
|-- csv_processor/           # Data preprocessing module
|-- db_handler/              # Database interaction module
|-- models/                  # Model handling module
|-- tests/                   # Unit tests for modules
|-- requirements.txt         # Dependency file
|-- README.md                # Documentation
|-- housing_data.db          # SQLite database file
|-- predictions.csv          # Generated predictions
```

---

## **GitHub Actions**

### **CI/CD Integration**

This project uses **GitHub Actions** for continuous integration. The workflow:
1. Runs all tests upon each `push` or `pull_request`.
2. Tracks code quality and ensures the pipeline remains robust.

**Sample Workflow File (`.github/workflows/test.yml`):**
```yaml
name: Test Pipeline

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt

    - name: Run tests
      run: |
        pytest --tb=short --disable-warnings

    - name: Upload coverage report
      uses: actions/upload-artifact@v3
      with:
        name: coverage-report
        path: htmlcov
```

---

## **Testing**

### **Run Tests**
Execute all tests using:
```bash
pytest
```

### **Key Tests**
- **Data Preprocessing**:
  - Validates transformation logic for input data.
- **Database Operations**:
  - Ensures tables are created and data is inserted correctly.
- **Model Predictions**:
  - Checks predictions match expected outputs.
- **Pipeline Execution**:
  - Verifies the entire workflow from preprocessing to prediction.

---

## **Next Steps**

- Implement an API layer using FastAPI for real-time data processing and predictions. Using MongoDB as storage for processed raw data and PostgreSQL for predicted data. 
- Address any warnings (e.g., `FutureWarning` in `sklearn`) for long-term compatibility.

---

## **Author**
This project was completed as part of a technical interview for a Data Engineer (ETL) position. If you have any questions, please feel free to contact me.

