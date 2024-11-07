import random
import csv
from faker import Faker
import string


def generate_contacts(num_records=3200):
    fake = Faker()

    # List of common company suffixes
    company_suffixes = [
        "Inc.",
        "LLC",
        "Corp.",
        "Ltd.",
        "Group",
        "Solutions",
        "Technologies",
    ]

    # Set to track used emails
    used_emails = set()

    # List to store all records
    records = []

    def generate_unique_email(name):
        """Generate a unique email based on name with random additions if needed"""
        base_email = name.lower().replace(" ", ".")
        domains = [
            "gmail.com",
            "yahoo.com",
            "outlook.com",
            "company.com",
            "business.net",
        ]

        while True:
            random_num = "".join(random.choices(string.digits, k=random.randint(2, 4)))
            email = f"{base_email}{random_num}@{random.choice(domains)}"
            if email not in used_emails:
                used_emails.add(email)
                return email

    def generate_phone():
        """Generate a formatted phone number"""
        area_code = random.randint(100, 999)
        prefix = random.randint(100, 999)
        line = random.randint(1000, 9999)
        return f"({area_code}) {prefix}-{line}"

    def generate_company():
        """Generate a company name"""
        company_types = [
            "Solutions",
            "Technologies",
            "Industries",
            "Consulting",
            "Services",
        ]
        name_parts = [fake.word().capitalize(), fake.word().capitalize()]
        suffix = random.choice(company_suffixes)
        return f"{' '.join(name_parts)} {suffix}"

    # Generate records
    for _ in range(num_records):
        name = fake.name()
        email = generate_unique_email(name)
        record = {
            "name": name,
            "email": email,
            "phone_number": generate_phone(),
            "company": generate_company(),
        }
        records.append(record)

    # Write to CSV
    with open("pygen_contacts.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file, fieldnames=["name", "email", "phone_number", "company"]
        )
        writer.writeheader()
        writer.writerows(records)

    return records


# Generate the contacts
contacts = generate_contacts()

# Preview first few records
print("\nFirst 5 records:")
for contact in contacts[:5]:
    print(contact)

print(f"\nTotal records generated: {len(contacts)}")
