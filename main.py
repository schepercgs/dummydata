# 🚀 Dummy Boat Users Generator (2000 entries)
# ✔ Auto-installs dependencies
# ✔ Saves CSV file as 'dummy_boat_users_2000.csv'

import subprocess
import sys

# Auto-install required packages
try:
    import pandas as pd
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])
    import pandas as pd

try:
    from faker import Faker
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "faker"])
    from faker import Faker

import random
from datetime import datetime, timedelta

# Initialize
fake = Faker()
Faker.seed(42)
random.seed(42)

# Parameters
num_entries = 2000
email_domains = ["gmail.com", "yahoo.com", "hotmail.com", "mail.com"]
start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 4, 18)

countries = [
    "United States", "Canada", "Mexico", "Brazil", "United Kingdom",
    "France", "Germany", "Italy", "Spain", "Netherlands",
    "Australia", "New Zealand"
]

boat_specs = [
    ("Beneteau", "Oceanis 30.1", "31.3"), ("Jeanneau", "Sun Odyssey 440", "43.8"),
    ("Catalina", "Catalina 36", "36.3"), ("Hunter", "Hunter 356", "34.5"),
    ("Bavaria", "Bavaria Cruiser 34", "32.8"), ("Hanse", "Hanse 418", "40.7"),
    ("Island Packet", "IP 380", "38.7"), ("Hallberg-Rassy", "HR 412", "41.0"),
    ("Dufour", "Dufour 390", "39.1"), ("Sabre", "Sabre 426", "42.6"),
    ("Albin", "Nova 33", "32.6"), ("Tartan", "Tartan 4300", "43.0"),
    ("C&C", "C&C 30", "29.5"), ("Morgan", "Morgan 382", "38.2"),
    ("Pearson", "Pearson 365", "36.5"), ("O'Day", "O'Day 302", "29.9"),
    ("Contessa", "Contessa 32", "32.2"), ("Ericson", "Ericson 38", "37.8"),
    ("Westsail", "Westsail 32", "32.0"), ("Freedom", "Freedom 35", "35.4"),
    ("Cape Dory", "Cape Dory 36", "36.0"), ("Niagara", "Niagara 35", "35.1")
]

# Helpers
def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

def clean_text(text):
    return ''.join(c for c in text if c.isalnum()).lower()

# Data containers
used_names = set()
used_emails = set()
used_boat_names = set()
boat_names = [fake.unique.word().capitalize() + str(random.randint(1, 999)) for _ in range(3000)]

# Generation loop
data = []

for _ in range(num_entries):
    # Unique name
    while True:
        first = fake.first_name()
        last = fake.last_name()
        name_key = (clean_text(first), clean_text(last))
        if name_key not in used_names:
            used_names.add(name_key)
            break

    # Unique email
    while True:
        email = f"{name_key[0]}.{name_key[1]}{random.randint(1, 999)}@{random.choice(email_domains)}"
        if email not in used_emails:
            used_emails.add(email)
            break

    # Unique boat name
    while True:
        boat_name = boat_names.pop()
        if boat_name not in used_boat_names:
            used_boat_names.add(boat_name)
            break

    make, model, loa = random.choice(boat_specs)
    country = random.choice(countries)
    join_date = random_date(start_date, end_date).strftime('%Y-%m-%d')

    data.append({
        "first_name": first,
        "last_name": last,
        "boat_name": boat_name,
        "make": make,
        "model": model,
        "loa_ft": loa,
        "country": country,
        "email": email,
        "date_joined": join_date
    })

# Export CSV
df = pd.DataFrame(data)
csv_filename = "dummy_boat_users_2000.csv"
df.to_csv(csv_filename, index=False)
print(f"✅ CSV generated: {csv_filename}")
