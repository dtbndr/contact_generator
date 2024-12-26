# Contact Data Generator

A Python utility for generating and managing synthetic contact data. The project includes tools for creating realistic contact records and splitting large CSV files into manageable chunks.

## Prerequisites

- Python 3.8+
- Virtual environment (venv)
- pip package manager

## Setup

1. Clone the repository and navigate to the project directory
2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Generate Contacts

Generate synthetic contact data with companies and employee information:

```bash
python generate_contacts.py
```

This creates `pygen_contacts.csv` with randomized contact records including:
- Personal information (name, email, phone)
- Company details
- LinkedIn profiles
- Industry keywords
- SEO descriptions

### Split CSV Files

Split large CSV files into smaller chunks:

```bash
python split_csv.py
```

This will:
- Read `pygen_contacts.csv`
- Split it into multiple files of 5000 rows each
- Save the split files in a `split_files` directory

## Customization

### Contact Generation
Modify `generate_contacts()` parameters:
- `num_records`: Total number of contacts (default: 100)
- `duplicate_percentage`: Percentage of duplicate records (default: 0.01)
- `min_company_size`: Minimum employees per company (default: 5)
- `max_company_size`: Maximum employees per company (default: 10)

### CSV Splitting
Adjust `split_csv()` parameters:
- `input_file`: Source CSV file
- `output_prefix`: Prefix for split files
- `rows_per_file`: Number of rows per split file (default: 5000)
