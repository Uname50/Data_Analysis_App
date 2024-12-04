import pandas as pd
from pathlib import Path

def process_uploaded_file(file_path: Path) -> dict:
    
    """
    Process an uploaded file to clean and transform data
    """

    # Determine the file type and turn it into a Pandas DataFrame
    if file_path.suffix == ".csv":
        df = pd.read_csv(file_path)
    elif file_path.suffix == ".json":
        df = pd.read_json(file_path)
    else:
        raise ValueError("Unsupported file type, only CSV or JSON files are allowed")
    
    # Fill missing values with 0
    df.fillna(0, inplace=True)

    # Test operation: combine to create sales by category
    if "category" in df.columns and "sales" in df.columns:
        sales_by_category = df.groupby("category")["sales"].sum().reset_index()
        return {"sales_by_category": sales_by_category.to_dict(orient="records")}
    else:
        return{"message": "Required columns are not found in the DF"}