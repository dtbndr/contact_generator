import random
import csv
from faker import Faker
import string
import math

def generate_contacts(num_records=3200, duplicate_percentage=0.05):
    fake = Faker()
    
    # Calculate the number of duplicates to create (not exceeding 5%)
    max_duplicates = math.floor(num_records * duplicate_percentage)
    num_duplicates = random.randint(1, max_duplicates)
    
    print(f"Generating {num_records} records with approximately {num_duplicates} duplicates...")
    
    # List of common company suffixes
    company_suffixes = ['Inc.', 'LLC', 'Corp.', 'Ltd.', 'Group', 'Solutions', 'Technologies']
    
    # List to store all records
    records = []
    emails_to_records = {}  # Dictionary to store email -> record mapping
    
    def generate_email(first_name, last_name):
        """Generate an email based on first and last name with random additions"""
        base_email = f"{first_name.lower()}.{last_name.lower()}"
        domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'company.com', 'business.net']
        random_num = ''.join(random.choices(string.digits, k=random.randint(2, 4)))
        return f"{base_email}{random_num}@{random.choice(domains)}"
    
    def generate_phone():
        """Generate a formatted phone number"""
        area_code = random.randint(100, 999)
        prefix = random.randint(100, 999)
        line = random.randint(1000, 9999)
        return f"({area_code}) {prefix}-{line}"
    
    def generate_company():
        """Generate a company name"""
        company_types = ['Solutions', 'Technologies', 'Industries', 'Consulting', 'Services']
        name_parts = [fake.word().capitalize(), fake.word().capitalize()]
        suffix = random.choice(company_suffixes)
        return f"{' '.join(name_parts)} {suffix}"
    
    def create_record():
        """Create a single record"""
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = generate_email(first_name, last_name)
        
        return {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone_number': generate_phone(),
            'company': generate_company()
        }
    
    # Generate initial records
    initial_records = num_records - num_duplicates
    for _ in range(initial_records):
        record = create_record()
        records.append(record)
        emails_to_records[record['email']] = record
    
    # Generate duplicates
    emails_to_duplicate = random.sample(list(emails_to_records.keys()), num_duplicates)
    for email in emails_to_duplicate:
        # Create a variation of the original record
        original = emails_to_records[email]
        duplicate = original.copy()
        
        # Randomly modify some fields while keeping the email the same
        if random.random() < 0.5:
            duplicate['phone_number'] = generate_phone()
        if random.random() < 0.5:
            duplicate['company'] = generate_company()
            
        records.append(duplicate)
    
    # Shuffle records to distribute duplicates randomly
    random.shuffle(records)
    
    # Write to CSV
    with open('pygen_contacts.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['first_name', 'last_name', 'email', 'phone_number', 'company'])
        writer.writeheader()
        writer.writerows(records)
    
    # Count actual duplicates for verification
    email_counts = {}
    for record in records:
        email_counts[record['email']] = email_counts.get(record['email'], 0) + 1
    
    duplicate_emails = {email: count for email, count in email_counts.items() if count > 1}
    
    print(f"\nGenerated {len(records)} total records")
    print(f"Number of unique emails: {len(email_counts)}")
    print(f"Number of duplicate entries: {len(records) - len(email_counts)}")
    print("\nDuplicate email examples:")
    for email, count in list(duplicate_emails.items())[:3]:
        print(f"Email: {email}, Occurrences: {count}")
    
    return records

# Generate the contacts
contacts = generate_contacts()

# Preview first few records
print("\nFirst 5 records:")
for contact in contacts[:5]:
    print(contact)
