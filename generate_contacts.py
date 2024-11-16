import random
import csv
from faker import Faker
import string
import math
from collections import defaultdict

def generate_contacts(num_records=3200, duplicate_percentage=0.05, min_company_size=5, max_company_size=10):
    fake = Faker()
    
    # Calculate the number of duplicates to create (not exceeding 5%)
    max_duplicates = math.floor(num_records * duplicate_percentage)
    num_duplicates = random.randint(1, max_duplicates)
    
    print(f"Generating {num_records} records with approximately {num_duplicates} duplicates...")
    
    # List of common company suffixes
    company_suffixes = ['Inc.', 'LLC', 'Corp.', 'Ltd.', 'Group', 'Solutions', 'Technologies']
    
    # Generate a pool of companies
    def generate_company():
        """Generate a company name"""
        company_types = ['Solutions', 'Technologies', 'Industries', 'Consulting', 'Services']
        name_parts = [fake.word().capitalize(), fake.word().capitalize()]
        suffix = random.choice(company_suffixes)
        return f"{' '.join(name_parts)} {suffix}"
    
    # Calculate number of companies needed
    avg_company_size = (min_company_size + max_company_size) / 2
    num_companies = math.ceil(num_records / avg_company_size)
    companies = [generate_company() for _ in range(num_companies)]
    
    # List to store all records
    records = []
    emails_to_records = {}  # Dictionary to store email -> record mapping
    company_to_records = defaultdict(list)  # Dictionary to track records per company
    
    def generate_email(first_name, last_name, company):
        """Generate an email based on first and last name with random additions"""
        # 40% chance to use company domain, 60% chance to use public email domain
        if random.random() < 0.4:
            # Create company domain from company name
            company_domain = company.split()[0].lower() + '.com'
        else:
            domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'business.net']
            company_domain = random.choice(domains)
        
        base_email = f"{first_name.lower()}.{last_name.lower()}"
        random_num = ''.join(random.choices(string.digits, k=random.randint(2, 4)))
        return f"{base_email}{random_num}@{company_domain}"
    
    def generate_phone():
        """Generate a formatted phone number"""
        area_code = random.randint(100, 999)
        prefix = random.randint(100, 999)
        line = random.randint(1000, 9999)
        return f"({area_code}) {prefix}-{line}"
    
    def create_record(company=None):
        """Create a single record"""
        first_name = fake.first_name()
        last_name = fake.last_name()
        company = company or random.choice(companies)
        email = generate_email(first_name, last_name, company)
        
        return {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone_number': generate_phone(),
            'company': company
        }
    
    # Generate initial records with company clusters
    remaining_records = num_records - num_duplicates
    
    while remaining_records > 0:
        # Select a company
        company = random.choice(companies)
        
        # Determine cluster size for this company
        if len(company_to_records[company]) >= max_company_size:
            continue
            
        cluster_size = min(
            random.randint(min_company_size, max_company_size) - len(company_to_records[company]),
            remaining_records
        )
        
        # Generate records for this company
        for _ in range(cluster_size):
            record = create_record(company)
            records.append(record)
            emails_to_records[record['email']] = record
            company_to_records[company].append(record)
            remaining_records -= 1
    
    # Generate duplicates
    emails_to_duplicate = random.sample(list(emails_to_records.keys()), num_duplicates)
    for email in emails_to_duplicate:
        # Create a variation of the original record
        original = emails_to_records[email]
        duplicate = original.copy()
        
        # Randomly modify phone number while keeping email and company the same
        duplicate['phone_number'] = generate_phone()
        records.append(duplicate)
    
    # Shuffle records to distribute duplicates randomly
    random.shuffle(records)
    
    # Write to CSV
    with open('pygen_contacts.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['first_name', 'last_name', 'email', 'phone_number', 'company'])
        writer.writeheader()
        writer.writerows(records)
    
    # Print statistics
    print(f"\nGenerated {len(records)} total records")
    print(f"Number of companies: {len(company_to_records)}")
    print("\nCompany distribution examples:")
    for company, company_records in list(company_to_records.items())[:5]:
        print(f"\nCompany: {company}")
        print(f"Number of employees: {len(company_records)}")
        print("Sample employees:")
        for record in company_records[:2]:
            print(f"- {record['first_name']} {record['last_name']} ({record['email']})")
    
    # Count email duplicates
    email_counts = {}
    for record in records:
        email_counts[record['email']] = email_counts.get(record['email'], 0) + 1
    
    duplicate_emails = {email: count for email, count in email_counts.items() if count > 1}
    print(f"\nNumber of duplicate email entries: {len(records) - len(email_counts)}")
    
    return records

# Generate the contacts
contacts = generate_contacts()
