"""
Module for adding new users with face data to the SQLite attendance system database dana signature file.
"""

import sqlite3
from PIL import Image
import numpy as np
import os
import pickle
import cv2
from numpy import asarray, expand_dims
from keras_facenet import FaceNet

# Load FaceNet model and Haar Cascade for face detection
HaarCascade = cv2.CascadeClassifier(cv2.samples.findFile(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'))
MyFaceNet = FaceNet()

# Load existing face database
with open("signatureNotebook/data.pkl", "rb") as myfile:
    database = pickle.load(myfile)

def add_new_user(name, email, department, face_image_path):
    """
    Adds a new user to the users table and their face embedding to the face_data table.

    Args:
        name (str): Name of the user.
        email (str): Email of the user.
        department (str): Department of the user.
        face_image_path (str): Path to the face image of the user.
    
    Raises:
        ValueError: If the face image cannot be loaded.
    """
    conn = sqlite3.connect('Database/attendance_system.db')
    c = conn.cursor()

    # Add new user to the users table
    c.execute("INSERT INTO users (name, email, department) VALUES (?, ?, ?)", (name, email, department))
    user_id = c.lastrowid

    # Process face image
    path = face_image_path
    gbr1 = cv2.imread(path)
    if gbr1 is None:
        raise ValueError(f"Failed to load image at {path}")
    
    wajah = HaarCascade.detectMultiScale(gbr1, 1.1, 4)
    
    if len(wajah) > 0:
        x1, y1, width, height = wajah[0]
    else:
        x1, y1, width, height = 1, 1, 10, 10
    
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height
    
    gbr = cv2.cvtColor(gbr1, cv2.COLOR_BGR2RGB)
    gbr = Image.fromarray(gbr)
    gbr_array = asarray(gbr)
    
    face = gbr_array[y1:y2, x1:x2]
    face = Image.fromarray(face)
    face = face.resize((160, 160))
    face = asarray(face)
    
    face = expand_dims(face, axis=0)
    signature = MyFaceNet.embeddings(face)
    
    database[name] = signature
    
    # Save signature to file
    with open("signatureNotebook/data.pkl", "wb") as myfile:
        pickle.dump(database, myfile)

    # Save face embedding to face_data table
    c.execute("INSERT INTO face_data (user_id, face_embedding) VALUES (?, ?)", (user_id, signature.tobytes()))

    conn.commit()
    conn.close()
