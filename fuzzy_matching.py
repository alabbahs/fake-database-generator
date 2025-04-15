from faker import Faker
from fuzzywuzzy import fuzz
import pandas as pd

def is_safe_function(func_name):
    return not (
        func_name.startswith("_") or
        func_name in {"seed", "seed_instance", "time_series"}  # Exclude known problematic generators
    )

def match_faker_function(field_name: str) -> str:
    faker = Faker()
    faker_functions = [
        attr for attr in dir(faker)
        if is_safe_function(attr) and callable(getattr(faker, attr, None))
    ]
    
    best_match = max(faker_functions, key=lambda func: fuzz.ratio(field_name.lower(), func.lower()))
    
    try:
        return getattr(faker, best_match)()
    except Exception as e:
        return f"<Error generating fake data: {e}>"

if __name__ == "__main__":
    df = pd.read_csv("data/split_tables/white_past_year.csv")
    for field in df["column_name"]:
        field_name = str(field)
        faker_output = match_faker_function(field_name)
        print(f"Best match for field '{field_name}': {faker_output}")
