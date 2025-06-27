import os
import pandas as pd

def load_data(source):
    if hasattr(source, "read"):  # file uploader
        if source.name.endswith(".csv"):
            return pd.read_csv(source)
        elif source.name.endswith((".xls", ".xlsx")):
            return pd.read_excel(source)
    elif isinstance(source, str):  # file path or URL
        source = os.path.expanduser(source.strip())  # expands ~ and strips whitespace
        if not source.startswith("/"):
            source = "/" + source  # ensure absolute path
        if source.endswith(".csv"):
            return pd.read_csv(source)
        elif source.endswith((".xls", ".xlsx")):
            return pd.read_excel(source)
    raise ValueError("Unsupported file or path format.")

