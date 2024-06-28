"""
Module for accessing and displaying data from the SQLite attendance system database.
"""

import sqlite3
import pandas as pd

try:
    # Open connection to SQLite database
    conn = sqlite3.connect('Database/attendance_system.db')
    cursor = conn.cursor()
    print("Successfully connected to the database.")

    # Get list of tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    if tables:
        print("Tables in the database:")
        for table in tables:
            print(table[0])
    else:
        print("No tables found in the database.")

    # Display content of each table using pandas
    for table in tables:
        table_name = table[0]
        print(f"\nContent of table {table_name}:")

        # Use pandas to read the table
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        print(df)

except sqlite3.Error as e:
    print(f"Error accessing the database: {e}")

finally:
    if conn:
        # Close the connection to the database
        conn.close()
        print("Database connection closed.")
