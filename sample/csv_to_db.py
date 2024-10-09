import os
import sqlite3
import pandas as pd
import re

def camel_case(s):
    # Convert to lowercase, then replace spaces and underscores, capitalize the next letter, and join them
    return ''.join(word.capitalize() for word in re.split(r'[\s_]+', s.lower()))

# Create or connect to the SQLite database
def create_db(db_name):
    return sqlite3.connect(db_name)

# Create a table and insert data from the CSV file
def csv_to_sqlite(csv_file, conn):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Convert DataFrame column names to CamelCase
    df.columns = [camel_case(col) for col in df.columns]

    # Use the CSV filename (without extension) as the table name
    table_name = os.path.splitext(os.path.basename(csv_file))[0]

    # Write the DataFrame to an SQLite table
    df.to_sql(table_name, conn, if_exists='replace', index=False)

def main():
    # Database file name
    db_file = 'output_database.db'
    
    # Create database connection
    conn = create_db(db_file)

    # Get all CSV files in the current working directory
    csv_files = [f for f in os.listdir() if f.endswith('.csv')]

    # Process each CSV file
    for csv_file in csv_files:
        csv_to_sqlite(csv_file, conn)

    # Close the database connection
    conn.close()

if __name__ == '__main__':
    main()
