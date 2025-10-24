import csv
from typing import Optional

def load_dataset(filepath: str, headers: Optional[list[str]] = None) -> list[dict]:
    """Generic CSV dataset loader. 
    
    Args:
        filepath (str): Full path to the CSV file
        headers (list[str], optional): List of column headers. If None, uses first row as headers.

    Returns:
        list[dict]: List of dictionaries representing rows
    """
    rows: list[dict] = []

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        if headers is None:
            # Use CSV headers from first row
            reader = csv.DictReader(f)
            for row in reader:
                # Clean up the row
                cleaned_row = {}
                for k, v in row.items():
                    cleaned_row[k] = v.strip() if isinstance(v, str) else v
                rows.append(cleaned_row)
        else:
            # Use provided headers for .dat files or headerless CSV
            reader = csv.reader(f)
            for raw in reader:
                if not raw:
                    continue
                # Pad row if it has fewer columns than headers
                if len(raw) < len(headers):
                    raw += ["" for _ in range(len(headers) - len(raw))]
                # Create row dictionary
                row = {h: (raw[i].strip('"') if i < len(raw) else "") for i, h in enumerate(headers)}
                rows.append(row)
    
    return rows