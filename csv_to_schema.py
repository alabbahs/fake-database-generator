import os
import pandas as pd
import json
from split_tables import split_tables
from fuzzy_matching import match_faker_function
from faker import Faker

INPUT_FOLDER = "data/split_tables"
OUTPUT_FILE = "output_schema.json"

def process_csv(file_path):
    faker = Faker()
    df = pd.read_csv(file_path)

    table_name = df["table_name"].iloc[0]

    fields = []
    for _, row in df.iterrows():
        fake_data = match_faker_function(row["column_name"])  
        field = {
            "name": row["column_name"],
            "type": row["full_data_type"],
            "fake_data": str(fake_data)
        }
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
