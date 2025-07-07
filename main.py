# Auto-install required packages
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import pandas as pd
except ImportError:
    install("pandas")
    import pandas as pd

try:
    from faker import Faker
except ImportError:
    install("faker")
    from faker import Faker

# Standard libs
import random
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()
Faker.seed(42)
random.seed(42)

# Settings
num_entries = 2000
email_domains = ["gmail.com", "yahoo.com", "hotmail.com", "mail.com"]
start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 4, 18)

# Country list with ISO codes
countries_with_iso = {
    "United States": "US", "Canada": "CA", "Mexico": "MX", "Brazil": "BR", "Argentina": "AR",
    "United Kingdom": "GB", "France": "FR", "Germany": "DE", "Italy": "IT", "Spain": "ES", "Portugal": "PT",
    "Netherlands": "NL", "Sweden": "SE", "Norway": "NO", "Denmark": "DK",
    "Australia": "AU", "New Zealand": "NZ"
}

# Boat specs: (make, model, LOA in feet)
boat_specs = [
    ("Beneteau", "Oceanis 30.1", "31.3"), ("Jeanneau", "Sun Odyssey 440", "43.8"),
    ("Catalina", "Catalina 36", "36.3"), ("Hunter", "Hunter 356", "34.5"),
    ("Bavaria", "Cruiser 34", "32.8"), ("Hanse", "418", "40.7"),
    ("Island Packet", "IP 380", "38.7"), ("Hallberg-Rassy", "HR 412", "41.0"),
    ("Dufour", "390", "39.1"), ("Sabre", "426", "42.6"),
    ("Albin", "Nova 33", "32.6"), ("Tartan", "4300", "43.0"),
    ("C&C", "30", "29.5"), ("Morgan", "382", "38.2"),
    ("Pearson", "365", "36.5"), ("O'Day", "302", "29.9"),
    ("Contessa", "32", "32.2"), ("Ericson", "38", "37.8"),
    ("Westsail", "32", "32.0"), ("Freedom", "35", "35.4"),
    ("Cape Dory", "36", "36.0"), ("Niagara", "35", "35.1")
]

# Boat name components
adjectives = ["Blue", "Golden", "Crimson", "Quiet", "Misty", "Lone", "La", "El", "Velho", "Nova", "Serene"]
nouns = ["Wind", "Dream", "Voyager", "Sirena", "Spirit", "Whisper", "Odyssey", "Vento", "Esperanza", "Breeze"]
mythical = ["Zephyr", "Nautilus", "Poseidon", "Athena", "Calypso", "Orion", "Aphrodite"]
nature = ["Sea Breeze", "Ocean Mist", "Morning Star", "Sunset Sail", "Storm Breaker", "Deep Blue"]
suffixes = ["II", "III", "IV", "of the Sea", "del Mar", "dos Mares", "of Avalon"]

# Utilities
def clean_text(text):
    return ''.join(c for c in text if c.isalnum()).lower()

def generate_boat_name():
    for _ in range(1000):
        pattern = random.choice([
            lambda: f"{random.choice(adjectives)} {random.choice(nouns)}",
            lambda: f"{random.choice(mythical)}",
            lambda: f"{random.choice(nature)}",
            lambda: f"{random.choice(adjectives)} {random.choice(mythical)}",
            lambda: f"{random.choice(nouns)} {random.choice(suffixes)}",
            lambda: f"{random.choice(adjectives)} {random.choice(nouns)} {random.randint(1, 999)}",
            lambda: f"{random.choice(mythical)} {random.randint(100, 999)}"
        ])
        name = pattern().strip()
        if name not in used_boat_names:
            used_boat_names.add(name)
            return name
    fallback = f"Boat_{len(used_boat_names) + 1}"
    used_boat_names.add(fallback)
    return fallback

def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

# Containers
used_names = set()
used_emails = set()
used_boat_names = set()
data = []

# Generate data
for _ in range(num_entries):
    # Unique name
    while True:
        first = fake.first_name()
        last = fake.last_name()
        key = (clean_text(first), clean_text(last))
        if key not in used_names:
            used_names.add(key)
            break

    full_name = f"{first} {last}"

    # Unique email
    while True:
        email = f"{key[0]}.{key[1]}{random.randint(1, 999)}@{random.choice(email_domains)}"
        if email not in used_emails:
            used_emails.add(email)
            break

    # Boat info
    boat_name = generate_boat_name()
    make, model, loa = random.choice(boat_specs)

    # Country + ISO code
    country = random.choice(list(countries_with_iso.keys()))
    country_code = countries_with_iso[country]

    # Join date
    join_date = random_date(start_date, end_date).strftime('%Y-%m-%d')

    # Append to dataset
    data.append({
        "first_name": first,
        "last_name": last,
        "full_name": full_name,
        "boat_name": boat_name,
        "make": make,
        "model": model,
        "loa_ft": loa,
        "country": country,
        "country_code": country_code,
        "email": email,
        "date_joined": join_date
    })

# Export to CSV
df = pd.DataFrame(data)
csv_file = "dummy_boat_users_2000.csv"
df.to_csv(csv_file, index=False)

print(f"\n✅ Done! CSV file created: {csv_file}")
