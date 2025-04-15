from faker import Faker
from fuzzywuzzy import fuzz

def match_faker_function(field_name: str) -> str:
    faker = Faker()
    
    faker_functions = [
        attr for attr in dir(faker)
        if not attr.startswith("_")
        and attr not in {"seed", "seed_instance"}
        and callable(getattr(faker, attr, None))
    ]
    
    best_match = max(faker_functions, key=lambda func: fuzz.ratio(field_name.lower(), func.lower()))
    return best_match

if __name__ == "__main__":
    faker = Faker()
    field_name = "name"
    matched_function = match_faker_function(field_name)
    print(f"Matched Faker function for '{field_name}': {matched_function}")
    print(getattr(faker, matched_function)())
