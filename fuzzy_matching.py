from faker import Faker
from fuzzywuzzy import fuzz
import pandas as pd

def is_safe_function(func_name):
    return not (
        func_name.startswith("_") or
        func_name in {"seed", "seed_instance", "time_series"}
    )

def match_faker_function(field_name: str) -> str | None:
    faker = Faker()
    faker_functions = [
        attr for attr in dir(faker)
        if is_safe_function(attr) and callable(getattr(faker, attr, None))
    ]
    
    best_match = max(
        faker_functions,
        key=lambda func: fuzz.ratio(field_name.lower(), func.lower())
    )
    
    score = fuzz.ratio(field_name.lower(), best_match.lower())
    if score >= 80:
        try:
            return getattr(faker, best_match)()
        except Exception as e:
            return f"<Error: {e}>"
    else:
        return None

if __name__ == "__main__":
    df = pd.read_csv("data/split_tables/white_past_year.csv")
    for field in df["column_name"]:
        field_name = str(field)
        faker_output = match_faker_function(field_name)
        print(f"Field '{field_name}' → {faker_output}")
