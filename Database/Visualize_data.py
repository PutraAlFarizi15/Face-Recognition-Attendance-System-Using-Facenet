import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.decomposition import PCA

# Visualisasi distribusi data pengguna
conn = sqlite3.connect('Database/attendance_system.db')
c = conn.cursor()

# Ambil data dari tabel users
c.execute("SELECT * FROM users")
users = c.fetchall()

# Ambil data dari tabel attendance
c.execute("SELECT * FROM attendance")
attendance = c.fetchall()

conn.close()

# Debugging: Cek apakah data users diambil dengan benar
print("Users data:", users)

# Jika users kosong, cetak pesan error dan exit
if not users:
    print("Tidak ada data pengguna ditemukan.")
    exit()

# Distribusi jumlah pengguna
user_ids = [user[0] for user in users]
username = [user[1] for user in users]

plt.figure(figsize=(10, 6))
#sns.countplot(user_ids)
sns.countplot(username)
plt.title('Distribusi Jumlah Pengguna')
plt.xlabel('Count')
plt.ylabel('Username')
plt.show()

# Visualisasi kinerja model
def plot_embeddings(embeddings, labels):
    pca = PCA(n_components=2)
    reduced_embeddings = pca.fit_transform(embeddings)

    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(reduced_embeddings[:, 0], reduced_embeddings[:, 1], c=labels, cmap='viridis')
    plt.legend(handles=scatter.legend_elements()[0], labels=set(labels))
    plt.title('Visualisasi Embeddings Wajah')
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')
    plt.show()

# Mengumpulkan data embedding dan label dari database
embeddings = []
labels = []

conn = sqlite3.connect('Database/attendance_system.db')
c = conn.cursor()
c.execute("SELECT user_id, face_embedding FROM face_data")
data = c.fetchall()

conn.close()

# Debugging: Cek apakah data face_data diambil dengan benar
print("Face data:", data)

# Jika data face_data kosong, cetak pesan error dan exit
if not data:
    print("Tidak ada data wajah ditemukan.")
    exit()

for row in data:
    user_id, face_embedding = row
    embeddings.append(np.frombuffer(face_embedding, dtype=np.float32))
    labels.append(user_id)

plot_embeddings(embeddings, labels)
