"""
Streamlit application for a face recognition attendance system.
"""

import streamlit as st
import sqlite3
from PIL import Image
import numpy as np
import os
import pickle
from numpy import asarray, expand_dims
import cv2
from keras_facenet import FaceNet
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import requests
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import seaborn as sns
from Database.add_user_data import add_new_user  # Import the function from add_user_data.py
#from add_new_user import add_new_user

st.set_option('deprecation.showPyplotGlobalUse', False)

# Load HaarCascade and FaceNet model
HaarCascade = cv2.CascadeClassifier(cv2.samples.findFile(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'))

# Try initializing the FaceNet model
MyFaceNet = FaceNet()

# Load face data Signature
with open("signatureNotebook/data.pkl", "rb") as myfile:
    database = pickle.load(myfile)

# Function to get user_id based on user name
def get_user_id(identity):
    """
    Fetches the user_id based on the user name.
    
    Args:
        identity (str): The name of the user.
    
    Returns:
        int: The user_id of the user, if found. Otherwise, None.
    """
    conn = sqlite3.connect('Database/attendance_system.db')
    c = conn.cursor()
    c.execute("SELECT user_id FROM users WHERE name=?", (identity,))
    user_id = c.fetchone()
    conn.close()
    return user_id[0] if user_id else None

# Define the video transformer class
class VideoTransformer(VideoTransformerBase):
    """
    A class to handle video frame transformation for face recognition and attendance marking.
    """
    def __init__(self):
        self.attendance_marked = False

    def transform(self, frame):
        """
        Transforms the video frame to detect faces, recognize identities, and mark attendance.
        
        Args:
            frame: The video frame from the webcam.
        
        Returns:
            The annotated video frame.
        """
        gbr1 = frame.to_ndarray(format="bgr24")
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
        face = face.resize((160,160))
        face = asarray(face)
        face = expand_dims(face, axis=0)
        
        signature = MyFaceNet.embeddings(face)
        
        min_dist = 100
        identity = ''
        
        for key, value in database.items():
            dist = np.linalg.norm(value - signature)
            if dist < min_dist:
                min_dist = dist
                identity = key
        
        if identity and not self.attendance_marked:
            user_id = get_user_id(identity)
            response = requests.post('http://localhost:5000/mark_attendance', json={'user_id': user_id})
            st.write(response.json())
            self.attendance_marked = True  # Mark attendance
        
        cv2.putText(gbr1, identity, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
        cv2.rectangle(gbr1, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # Reset the attendance flag if no face is detected to allow for new detections
        if len(wajah) == 0:
            self.attendance_marked = False
        
        return gbr1

# Streamlit app
st.title("Face Recognition Attendance System Using Facenet")

# Sidebar for navigation
menu = st.sidebar.selectbox("Menu", ["Attendance", "Add New User"])

if menu == "Attendance":
    # Start the webcam
    webrtc_streamer(key="example", video_transformer_factory=VideoTransformer)

elif menu == "Add New User":
    st.header("Add New User")
    name = st.text_input("Name")
    email = st.text_input("Email")
    department = st.text_input("Department")
    face_image = st.file_uploader("Upload Face Image", type=["jpg", "jpeg", "png"])
    
    if st.button("Add User"):
        if name and email and department and face_image:
            # Save the uploaded image to a temporary file
            face_image_path = os.path.join("addData", face_image.name)
            with open(face_image_path, "wb") as f:
                f.write(face_image.getbuffer())
            
            try:
                add_new_user(name, email, department, face_image_path)
                st.success("User added successfully!")
            except Exception as e:
                st.error(f"Failed to add user: {e}")
        else:
            st.error("Please fill all the fields and upload an image.")
