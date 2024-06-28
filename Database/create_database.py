"""
Module for creating tables in the attendance system database.
"""

import sqlite3

# Connect to the database
conn = sqlite3.connect('Database/attendance_system.db')
c = conn.cursor()

# Create the users table
c.execute('''
          CREATE TABLE users
          (user_id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT,
          email TEXT,
          department TEXT)
          ''')

# Create the face_data table
c.execute('''
          CREATE TABLE face_data
          (face_id INTEGER PRIMARY KEY AUTOINCREMENT,
          user_id INTEGER,
          face_embedding BLOB,
          FOREIGN KEY(user_id) REFERENCES users(user_id))
          ''')

# Create the attendance table
c.execute('''
          CREATE TABLE attendance
          (attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
          user_id INTEGER,
          timestamp DATETIME,
          FOREIGN KEY(user_id) REFERENCES users(user_id))
          ''')

# Commit changes and close the connection
conn.commit()
conn.close()