import pandas as pd
import os
import math


def split_csv(input_file, output_prefix="split_contacts", rows_per_file=5000):
    """
    Split a CSV file into multiple files with specified number of rows

    Parameters:
    input_file (str): Name of the input CSV file
    output_prefix (str): Prefix for output files
    rows_per_file (int): Approximate number of rows per output file
    """
    # Read the CSV file
    print(f"Reading {input_file}...")
    df = pd.read_csv(input_file)

    # Verify the expected columns are present
    expected_columns = ["first_name", "last_name", "email", "phone_number", "company"]
    missing_columns = [col for col in expected_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing expected columns: {missing_columns}")

    # Calculate total number of rows and files needed
    total_rows = len(df)
    num_files = math.ceil(total_rows / rows_per_file)

    print(f"Total rows: {total_rows}")
    print(f"Splitting into {num_files} files...")

    # Create output directory if it doesn't exist
    output_dir = "split_files"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Split the dataframe and save to separate files
    for i in range(num_files):
        start_idx = i * rows_per_file
        end_idx = min((i + 1) * rows_per_file, total_rows)

        # Create the split dataframe
        split_df = df[start_idx:end_idx]

        # Generate output filename
        output_file = os.path.join(output_dir, f"{output_prefix}_{i+1}.csv")

        # Save to CSV
        split_df.to_csv(output_file, index=False)
        print(f"Created {output_file} with {len(split_df)} rows")
        print(f"Sample from file {i+1}:")
        print(split_df.head(1))
        print()


if __name__ == "__main__":
    # Split the CSV file
    input_file = "pygen_contacts.csv"
    split_csv(input_file)

    print("\nSplit complete! Files are saved in the 'split_files' directory.")
