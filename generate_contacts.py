import random
import csv
from faker import Faker
import string
import math
from collections import defaultdict


def generate_contacts(
    num_records=100, duplicate_percentage=0.01, min_company_size=5, max_company_size=10
):
    fake = Faker()

    industries = [
        "Technology",
        "Healthcare",
        "Finance",
        "Manufacturing",
        "Retail",
        "Education",
        "Construction",
        "Entertainment",
        "Automotive",
        "Energy",
        "Consulting",
        "Real Estate",
    ]

    designations = [
        "CEO",
        "CTO",
        "CFO",
        "Manager",
        "Director",
        "VP Sales",
        "Software Engineer",
        "Product Manager",
        "Marketing Manager",
        "HR Manager",
        "Business Analyst",
        "Sales Representative",
    ]

    keywords = [
        "innovation",
        "leadership",
        "technology",
        "sustainability",
        "digital",
        "growth",
        "analytics",
        "automation",
        "cloud",
        "ai",
        "blockchain",
        "startup",
        "enterprise",
        "saas",
        "consulting",
    ]

    def generate_linkedin_url(first_name, last_name):
        if random.random() > 0.3:
            random_suffix = "".join(
                random.choices(
                    string.ascii_lowercase + string.digits, k=random.randint(4, 8)
                )
            )
            return f"https://www.linkedin.com/in/{first_name.lower()}-{last_name.lower()}-{random_suffix}"
        return None

    def generate_company_info():
        name_parts = [fake.word().capitalize(), fake.word().capitalize()]
        suffix = random.choice(
            ["Inc.", "LLC", "Corp.", "Ltd.", "Group", "Solutions", "Technologies"]
        )
        company_name = f"{' '.join(name_parts)} {suffix}"

        include_fields = {
            field: random.random() > 0.3
            for field in [
                "city",
                "state",
                "country",
                "industry",
                "website",
                "linkedin",
                "company_email",
                "company_phone",
                "keywords",
                "seo",
            ]
        }

        company_domain = company_name.split()[0].lower() + ".com"

        return {
            "name": company_name,
            "city": fake.city() if include_fields["city"] else None,
            "state": fake.state() if include_fields["state"] else None,
            "country": fake.country() if include_fields["country"] else None,
            "industry": (
                random.choice(industries) if include_fields["industry"] else None
            ),
            "website": (
                f"https://www.{company_domain}" if include_fields["website"] else None
            ),
            "linkedin": (
                f"https://www.linkedin.com/company/{'-'.join(company_name.split()[:2]).lower()}"
                if include_fields["linkedin"]
                else None
            ),
            "email": (
                f"contact@{company_domain}" if include_fields["company_email"] else None
            ),
            "phone": fake.phone_number() if include_fields["company_phone"] else None,
            "keywords": (
                ", ".join(random.sample(keywords, random.randint(3, 6)))
                if include_fields["keywords"]
                else None
            ),
            "seo": fake.text(max_nb_chars=200) if include_fields["seo"] else None,
        }

    def generate_email(first_name, last_name, company_domain):
        base_email = f"{first_name.lower()}.{last_name.lower()}"
        random_num = "".join(random.choices(string.digits, k=random.randint(2, 4)))
        use_company_email = random.random() < 0.4
        domain = (
            company_domain
            if use_company_email
            else random.choice(["gmail.com", "yahoo.com", "outlook.com"])
        )
        return f"{base_email}{random_num}@{domain}"

    print(
        f"Generating {num_records} records with approximately {math.floor(num_records * duplicate_percentage)} duplicates..."
    )

    companies = {}
    records = []
    emails_to_records = {}
    company_to_records = defaultdict(list)

    num_companies = math.ceil(num_records / ((min_company_size + max_company_size) / 2))
    for _ in range(num_companies):
        company_info = generate_company_info()
        companies[company_info["name"]] = company_info

    remaining_records = num_records - math.floor(num_records * duplicate_percentage)
    while remaining_records > 0:
        company_name = random.choice(list(companies.keys()))
        company = companies[company_name]

        if len(company_to_records[company_name]) >= max_company_size:
            continue

        cluster_size = min(
            random.randint(min_company_size, max_company_size)
            - len(company_to_records[company_name]),
            remaining_records,
        )

        company_domain = company_name.split()[0].lower() + ".com"

        for _ in range(cluster_size):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = generate_email(first_name, last_name, company_domain)

            record = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone_number": fake.phone_number(),
                "linkedin_url": generate_linkedin_url(first_name, last_name),
                "company": company_name,
                "designation": (
                    random.choice(designations) if random.random() > 0.2 else None
                ),
                "company_city": company["city"],
                "company_state": company["state"],
                "company_country": company["country"],
                "company_industry": company["industry"],
                "company_website_url": company["website"],
                "company_linkedin_url": company["linkedin"],
                "company_email_address": company["email"],
                "company_phone_number": company["phone"],
                "keywords": company["keywords"],
                "seo_description": company["seo"],
            }

            records.append(record)
            emails_to_records[email] = record
            company_to_records[company_name].append(record)
            remaining_records -= 1

    num_duplicates = math.floor(num_records * duplicate_percentage)
    emails_to_duplicate = random.sample(list(emails_to_records.keys()), num_duplicates)
    for email in emails_to_duplicate:
        duplicate = emails_to_records[email].copy()
        duplicate["phone_number"] = fake.phone_number()
        records.append(duplicate)

    random.shuffle(records)

    fieldnames = [
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "linkedin_url",
        "company",
        "designation",
        "company_city",
        "company_state",
        "company_country",
        "company_industry",
        "company_website_url",
        "company_linkedin_url",
        "company_email_address",
        "company_phone_number",
        "keywords",
        "seo_description",
    ]

    with open("pygen_contacts.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"\nGenerated {len(records)} total records")
    print(f"Number of companies: {len(company_to_records)}")
    print("\nCompany distribution examples:")
    for company, company_records in list(company_to_records.items())[:5]:
        print(f"\nCompany: {company}")
        print(f"Number of employees: {len(company_records)}")
        print("Sample employees:")
        for record in company_records[:2]:
            print(f"- {record['first_name']} {record['last_name']} ({record['email']})")
            print(f"  LinkedIn: {record['linkedin_url']}")

    email_counts = {}
    for record in records:
        email_counts[record["email"]] = email_counts.get(record["email"], 0) + 1

    duplicate_emails = {
        email: count for email, count in email_counts.items() if count > 1
    }
    print(f"\nNumber of duplicate email entries: {len(records) - len(email_counts)}")

    return records


# Generate contacts
if __name__ == "__main__":
    contacts = generate_contacts()
