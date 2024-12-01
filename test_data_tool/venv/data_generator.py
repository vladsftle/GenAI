from faker import Faker
import random
import re

def parse_constraint(constraint, field):
    """
    Parse constraints and return a callable that generates data meeting the constraints.
    """
    faker = Faker()

    # Handle empty or None constraints
    if not constraint:
        return default_generators(field)

    constraint = constraint.strip()  # Clean up leading/trailing whitespace

    # Custom logic for specific fields based on constraints
    if field == "Hobbies":
        if "sports" in constraint.lower():  # Match case-insensitive substring "sports"
            sports = ["Football", "Basketball", "Cricket", "Tennis", "Running", "Cycling", "Swimming", "Gymnastics"]
            return lambda: random.choice(sports)
        
        elif "traveling" in constraint.lower():  # Match case-insensitive substring "traveling"
            traveling = ["Hiking", "Road trips", "Backpacking", "Cruises", "City tours", "Camping"]
            return lambda: random.choice(traveling)

    elif field == "Age":
        if constraint.startswith("<") and len(constraint) > 1:
            max_age = int(constraint[1:].strip())
            return lambda: faker.random_int(min=0, max=max_age)
        elif constraint.startswith(">") and len(constraint) > 1:
            min_age = int(constraint[1:].strip())
            return lambda: faker.random_int(min=min_age, max=100)
        elif "-" in constraint:
            min_age, max_age = map(int, constraint.split("-"))
            return lambda: faker.random_int(min=min_age, max=max_age)
        elif constraint.isdigit():
            age = int(constraint)
            return lambda: age

    elif field == "Gender":
        return lambda: constraint.capitalize()

    elif field == "Address" and "Country:" in constraint:
        # Generate addresses specific to the given country
        country = constraint.split(":")[1].strip().lower()

        # Map user input to Faker locales
        locale_map = {
            "france": "fr_FR",
            "germany": "de_DE",
            "united states": "en_US",
            "spain": "es_ES",
            "italy": "it_IT",
            "japan": "ja_JP",
            "canada": "en_CA",
            "united kingdom": "en_GB",
            "romania": "ro_RO",
        }

        locale = locale_map.get(country, "en_US")
        faker = Faker(locale)
        return lambda: faker.address().replace("\n", ", ")

    elif field == "Phone" and "Country:" in constraint:
        # Generate phone numbers specific to the given country
        country = constraint.split(":")[1].strip().lower()
        locale_map = {
            "france": "fr_FR",
            "germany": "de_DE",
            "united states": "en_US",
            "spain": "es_ES",
            "italy": "it_IT",
            "japan": "ja_JP",
            "canada": "en_CA",
            "united kingdom": "en_GB",
            "romania": "ro_RO",
        }
        locale = locale_map.get(country, "en_US")
        faker = Faker(locale)
        return lambda: faker.phone_number()

    elif field == "Email":
        domain = constraint.strip()
        return lambda: f"{faker.user_name()}@{domain}"

    elif field == "Education":
        education_levels = [level.strip() for level in constraint.split(",")]
        return lambda: random.choice(education_levels)

    elif field == "Pets":
        if "dogs" in constraint.lower():  # Match case-insensitive substring "dogs"
            dog_breeds = [
                "Labrador Retriever", "German Shepherd", "Golden Retriever", "Bulldog", 
                "Beagle", "Poodle", "Rottweiler", "Dachshund", "Boxer", "Shih Tzu"
            ]
            return lambda: random.choice(dog_breeds)
        
        elif "cats" in constraint.lower():  # Match case-insensitive substring "cats"
            cat_breeds = [
                "Calico", "Siamese", "British Shorthair", "Main Coon", 
                "Persian Cat", "Ragdoll", "Sphinx", "Scottish Fold",
            ]
            return lambda: random.choice(cat_breeds)

    elif field == "Random Strings" and "Length:" in constraint:
        match = re.search(r"Length:\s*(\d+)", constraint)
        if match:
            length = int(match.group(1))
            return lambda: faker.pystr(min_chars=length, max_chars=length)

    # Fallback to default generator
    return default_generators(field)

# Default generators for fields
def default_generators(field):
    faker = Faker()
    if field == "Hobbies":
        hobbies = ["Reading", "Painting", "Gardening", "Cooking", "Photography", "Fishing"]
        return lambda: random.choice(hobbies)
    elif field == "Age":
        return lambda: faker.random_int(min=18, max=80)  # Default range
    elif field == "Gender":
        return lambda: random.choice(["Male", "Female", "Non-binary"])
    elif field == "Address":
        return lambda: Faker().address().replace("\n", ", ")
    elif field == "Phone":
        return lambda: Faker().phone_number()
    elif field == "Email":
        return lambda: Faker().email()
    elif field == "Education":
        return lambda: random.choice(["High School", "Bachelor", "Master", "PhD"])
    elif field == "Pets":
        return lambda: random.choice(["Cat", "Dog", "Parrot", "Hamster", "Fish", "Reptile", "Rabbit", "Guinea pig"])
    elif field == "Random Strings":
        return lambda: Faker().pystr(min_chars=10, max_chars=15)
    else:
        return lambda: "No valid data"

def generate_data(selected_fields, constraints, num_entries):
    """
    Generate test data based on selected fields and constraints.
    """
    data = []
    generators = {
        field: parse_constraint(constraints.get(field, ""), field)
        for field in selected_fields
    }

    for _ in range(num_entries):
        entry = {field: generator() for field, generator in generators.items()}
        data.append(entry)

    return data
