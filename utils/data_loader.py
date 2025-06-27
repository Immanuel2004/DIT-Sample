import pandas as pd
import duckdb
import tempfile
import os

def load_dataset(source, row_limit=1000, is_path=False):
    """
    Load dataset from Streamlit upload or file path using DuckDB.

    Args:
        source: Streamlit file uploader object or file path string
        row_limit: Number of rows to sample
        is_path: If True, treat source as file path

    Returns:
        pd.DataFrame
    """
    if is_path:
        file_path = source
        file_name = file_path.lower()
    else:
        file_name = source.name.lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv" if file_name.endswith(".csv") else ".xlsx") as tmp_file:
            tmp_file.write(source.getbuffer())
            file_path = tmp_file.name

    try:
        if file_name.endswith(".csv"):
            query = f"""
            SELECT * FROM read_csv_auto(
                '{file_path}',
                SAMPLE_SIZE={row_limit},
                delim=',',
                AUTO_DETECT=TRUE,
                encoding='utf-8',
                ignore_errors=TRUE,
                normalize_names=TRUE
            )
            LIMIT {row_limit}
            """
        elif file_name.endswith(".xlsx") or file_name.endswith(".xls"):
            query = f"""
            SELECT * FROM read_excel('{file_path}', AUTO_DETECT_TYPES=TRUE)
            LIMIT {row_limit}
            """
        else:
            raise ValueError("Unsupported file format. Use .csv or .xlsx")

        df = duckdb.query(query).to_df()
        return df

    finally:
        if not is_path and os.path.exists(file_path):
            os.unlink(file_path)
