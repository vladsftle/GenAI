from faker import Faker
import random
import re

def parse_constraint(constraint, field):
    """
    Parse constraints and return a callable that generates data meeting the constraints.
    """
    faker = Faker()

    if not constraint:
        # Default data generation logic if no constraints are provided
   #     return lambda: faker.word()
        return default_generators(field)

    # Custom logic for specific fields based on constraints
    
    if field == "Address" and "Country:" in constraint:
    # Generate addresses specific to the given country
        country = constraint.split(":")[1].strip().lower()

    # Map user input to Faker locales
        locale_map = {
            "France": "fr_FR",
            "fr": "fr_FR",
            "Germany": "de_DE",
            "de": "de_DE",
            "United States": "en_US",
            "us": "en_US",
            "Spain": "es_ES",
            "es": "es_ES",
            "Italy": "it_IT",
            "it": "it_IT",
            "Japan": "ja_JP",
            "jp": "ja_JP",
            "Canada": "en_CA",
            "ca": "en_CA",
            "United Kingdom": "en_GB",
            "gb": "en_GB",
            "Romania": "ro_RO",
            "ro": "ro_RO",
            # Add more mappings as needed
        }
    
    # Get the corresponding locale or default to en_US
        locale = locale_map.get(country, "en_US")
    
        Faker.seed(0)
        faker = Faker(locale)
        return lambda: faker.address().replace("\n", ", ")


    if field == "Phone" and "Country:" in constraint:
    # Extract country from the constraint
        country = constraint.split(":")[1].strip().lower()

        # Map user input to Faker locales
        locale_map = {
            "France": "fr_FR",
            "fr": "fr_FR",
            "Germany": "de_DE",
            "de": "de_DE",
            "United States": "en_US",
            "us": "en_US",
            "Spain": "es_ES",
            "es": "es_ES",
            "Italy": "it_IT",
            "it": "it_IT",
            "Japan": "ja_JP",
            "jp": "ja_JP",
            "Canada": "en_CA",
            "ca": "en_CA",
            "United Kingdom": "en_GB",
            "gb": "en_GB",
            "Romania": "ro_RO",
            "ro": "ro_RO",
            # Add more mappings as needed
        }

    # Get the corresponding locale or default to en_US
        locale = locale_map.get(country, "en_US")

        # Initialize Faker with the resolved locale
        try:
            Faker.seed(0)
            faker = Faker(locale)
            return lambda: faker.phone_number()
        except Exception as e:
            # Handle any errors during locale initialization
            print(f"Error initializing Faker with locale {locale}: {e}")
            return lambda: "Invalid locale"


    if field == "Random Strings" and "length:" in constraint:
        # Generate random strings with the specified length
        match = re.search(r"Length:\s*(\d+)", constraint)
        if match:
            length = int(match.group(1))
            return lambda: faker.pystr(min_chars=length, max_chars=length)

    if field == "Gender":
        
        # Generate gender based on the constraint (e.g., "male")
        gender = constraint.strip().lower()
        return lambda: gender.capitalize()

    if field == "Education":
        # Generate education level based on the constraint (e.g., "Higher education")
        education_levels = [level.strip() for level in constraint.split(",")]
        return lambda: random.choice(education_levels)

    if field == "Email":
        # Ensure valid email format with domain-specific constraints (e.g., "example.com")
        domain = constraint.strip()
        return lambda: f"{faker.user_name()}@{domain}"

    if field == "Age":
        # Handle empty constraints explicitly
        if not constraint:
            # No constraint provided; generate a random age between 18 and 80
            return lambda: faker.random_int(min=18, max=80)

        # Strip any extra whitespace for further validation
        constraint = constraint.strip()

        if constraint.startswith("<") and len(constraint) > 1:
            # Handle "<" (Less than)
            max_age = int(constraint[1:].strip())
            return lambda: faker.random_int(min=0, max=max_age)

        elif constraint.startswith(">") and len(constraint) > 1:
            # Handle ">" (Greater than)
            min_age = int(constraint[1:].strip())
            return lambda: faker.random_int(min=min_age, max=100)

        elif constraint.startswith("<=") and len(constraint) > 2:
            # Handle "<=" (Less than or equal to)
            max_age = int(constraint[2:].strip())
            return lambda: faker.random_int(min=0, max=max_age)

        elif constraint.startswith(">=") and len(constraint) > 2:
            # Handle ">=" (Greater than or equal to)
            min_age = int(constraint[2:].strip())
            return lambda: faker.random_int(min=min_age, max=100)

        elif "-" in constraint:
            # Handle age interval (e.g., "20-30")
            age_range = constraint.split("-")
            if len(age_range) == 2:
                try:
                    min_age = int(age_range[0].strip())
                    max_age = int(age_range[1].strip())
                    if min_age > max_age:
                        # In case the interval is reversed, swap the values
                        min_age, max_age = max_age, min_age
                    return lambda: faker.random_int(min=min_age, max=max_age)
                except ValueError:
                    return lambda: "Invalid interval format"

        # If no valid constraints, generate a random age between 18 and 80
        return lambda: faker.random_int(min=18, max=80)


    if field == "Pets" and "dog" in constraint.lower():
        # List of common dog breeds
        dog_breeds = [
            "Labrador Retriever", "German Shepherd", "Golden Retriever", "Bulldog", 
            "Beagle", "Poodle", "Rottweiler", "Dachshund", "Boxer", "Shih Tzu", 
            "Chihuahua", "Siberian Husky", "Doberman Pinscher", "Great Dane", 
            "Australian Shepherd", "Yorkshire Terrier", "Cocker Spaniel", "Pomeranian"
        ]
        
        # Return a random dog breed if "dog" or "dog breeds" is mentioned
        return lambda: random.choice(dog_breeds)
        
    if field == "hobbies" and "sports" in constraint.lower():
        hobbies = ["Football", "Basketball", "Cricket", "Tennis", "Running", "Cycling", "Swimming", "Gymnastics"]
        return lambda: random.choice(hobbies)
  
        if field == "Hobbies" and "traveling" in constraint.lower():
            hobbies = ["Hiking", "Road trips", "Backpacking", "Cruises", "City tours", "Camping"]
        return lambda: random.choice(hobbies)
    return default_generators(field)  # Fallback to default generator if constraint is invalid
    
# Example of default generators when no constraints are provided
def default_generators(field):
    if field == "Gender":
        genders = ["Male", "Female", "Non-binary", "Other"]
        return lambda: random.choice(genders)
    elif field == "Hobbies":
        hobbies = ["Reading", "Painting", "Gardening", "Cooking", "Photography", "Fishing", "Traveling", "Crafting", "Biking", "Music"]
        return lambda: random.choice(hobbies)
    elif field == "Education":
        education = ["High School", "Higher Education", "None", "PhD", "Masterate"]
        return lambda: random.choice(education)
    elif field == "Pets":
        # Default pet types
        pets = ["Cat", "Dog", "Parrot", "Hamster", "Goldfish", "Rabbit", "Guinea Pig", 
            "Turtle", "Ferret", "Chinchilla", "Budgie", "Iguana", "Canary", 
            "Hedgehog", "Gecko"]
        return lambda: random.choice(pets)
    elif field == "Email":
        return lambda: Faker().email()  # Generate a random email address
    elif field == "Phone":
        return lambda: Faker().phone_number()  # Generate a random phone number
    elif field == "Address":
        return lambda: Faker().address().replace("\n", ", ")  # Generate a random address
    elif field == "Random Strings":
        return lambda: Faker().pystr(min_chars=10, max_chars=15)
    else:
        # For other fields, return a random string or similar
        return lambda: "No valid data"

def generate_data(selected_fields, constraints, num_entries):
    """
    Generate test data based on selected fields and constraints.
    """
    data = []

    # Create a generator function for each field based on its constraint
    generators = {
        field: parse_constraint(constraints.get(field, None), field)
        for field in selected_fields
    }

    # Generate data entries
    for _ in range(num_entries):
        entry = {}
        for field, generator in generators.items():
            entry[field] = generator()  # Generate data using the generator function
        data.append(entry)

    return data
