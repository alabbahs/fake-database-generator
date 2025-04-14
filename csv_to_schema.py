import os
import pandas as pd
import json
from split_tables import split_tables

INPUT_FOLDER = "data/split_tables"
OUTPUT_FILE = "output_schema.json"

def process_csv(file_path):
    df = pd.read_csv(file_path)

    table_name = df["TableName"].iloc[0]

    fields = []
    for _, row in df.iterrows():
        field = {"name": row["Column"], "type": type(row["max"]).__name__}
        fields.append(field)

    return {
        "table_name": table_name,
        "fields": fields
    }

def main():
    all_tables = []

    for filename in os.listdir(INPUT_FOLDER):
        if filename.endswith(".csv"):
            csv_path = os.path.join(INPUT_FOLDER, filename)
            try:
                table_json = process_csv(csv_path)
                all_tables.append(table_json)
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    with open(OUTPUT_FILE, "w") as f:
        json.dump(all_tables, f, indent=4)

    print(f"✅ Schema written to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
