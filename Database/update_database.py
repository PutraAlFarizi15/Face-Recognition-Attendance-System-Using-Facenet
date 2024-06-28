"""
Module for adding initial users and face data to the SQLite attendance system database.
"""

import sqlite3
import pickle

def add_user(name, email, department):
    """
    Adds a user to the users table.
    
    Args:
        name (str): The name of the user.
        email (str): The email of the user.
        department (str): The department of the user.
    
    Returns:
        int: The user_id of the newly added user.
    """
    conn = sqlite3.connect('Database/attendance_system.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email, department) VALUES (?, ?, ?)", (name, email, department))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id

def add_face_data(user_id, face_embedding):
    """
    Adds face data to the face_data table.
    
    Args:
        user_id (int): The ID of the user.
        face_embedding (blob): The face embedding data.
    
    Returns:
        int: The face_id of the newly added face data.
    """
    conn = sqlite3.connect('Database/attendance_system.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO face_data (user_id, face_embedding) VALUES (?, ?)", (user_id, face_embedding))
    conn.commit()
    face_id = cursor.lastrowid
    conn.close()
    return face_id

users_to_add = [
    ['Aaron Eckhart', 'Aaron@E', 'IT'],
    ['Aaron Guiel', 'Aaron@G', 'Finance'],
    ['Aaron Patterson', 'Aaron@P', 'Marketing'],
    ['Dasha Taran', 'dasha.taran@example.com', 'IT'],
    ['Unknown', 'Unknown', 'Unknown']
]

for user in users_to_add:
    user_id = add_user(user[0], user[1], user[2])
    print(f"User {user_id} added: {user[0]}")

# Adding data to face_data
with open("signatureNotebook/data.pkl", "rb") as myfile:
    database = pickle.load(myfile)

names = []
embeddings = []
for key, value in database.items():
    names.append(key)
    embeddings.append(value)

user_id = 1
for embedding in embeddings:
    face_id = add_face_data(user_id, embedding)
    user_id += 1
    print(f"Face {face_id} added for user {user_id - 1}")
