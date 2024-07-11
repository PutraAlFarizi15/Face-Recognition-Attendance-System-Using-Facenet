# Face Recognition Attendance System Using Facenet

## Deskripsi Proyek
Proyek ini bertujuan untuk membangun sistem absensi berbasis pengenalan wajah yang menggunakan teknologi FaceNet. Sistem ini dirancang untuk menggantikan metode absensi manual dengan cara yang lebih cepat, akurat, dan aman. Teknologi FaceNet memungkinkan sistem untuk mengenali dan memverifikasi identitas individu melalui analisis wajah mereka, yang kemudian digunakan untuk mencatat kehadiran.

## Table of Contents
- [Rancangan Database dan Data Pipeline](#rancangan-database-dan-data-pipeline)
- [Dataset dan Modelling](#dataset-dan-modelling)
- [Instalasi dan Cara Penggunaan](#instalasi-dan-cara-penggunaan)
- [Struktur Proyek](#struktur-proyek)
- [Referensi](#referensi)

## Rancangan Database dan Data Pipeline
![Struktur Database](Database/Database%20Structure.png)

Database ini terdiri dari tiga tabel utama: users, face_data, dan attendance.
1. Tabel users menyimpan informasi tentang pengguna sistem kehadiran, termasuk user_id, name, email, dan department.
2. Tabel face_data digunakan untuk menyimpan data wajah pengguna. Setiap entri dalam tabel ini terkait dengan pengguna tertentu melalui user_id. Kolom face_embedding menyimpan data representasi wajah dalam bentuk blob.
3. Tabel attendance digunakan untuk mencatat kehadiran pengguna. Ini mencatat user_id pengguna yang hadir pada waktu tertentu (timestamp).

Setiap tabel memiliki kunci utama yang unik (PRIMARY KEY) dan kunci asing (FOREIGN KEY) yang merujuk ke user_id di tabel users, memastikan konsistensi referensial antara tabel-tabel tersebut.

**Data Pipeline**

Saat menambahkan data, data tersebut akan diembedding oleh [keras-facenet](https://pypi.org/project/keras-facenet/) untuk mengetahui signature wajah,  yang akan disimpan di database dan file data.pkl

## Dataset dan Modelling
Data untuk pembuatan signature wajah awal saya buat sendiri disimpan dalam folder **employeeFoto** terdapat file Unknown yang berguna jika tidak ada wajah yang dideteksi.

Untuk modelling pengenalan wajah saya menggunakan haarcascade untuk deteksi muka pada foto dan [keras-facenet](https://pypi.org/project/keras-facenet/) untuk mengetahui signature wajah.

## Instalasi dan Cara Penggunaan

Agar model yang sudah dibuat dapat digunakan, proyek ini menggunakan library [Streamlit](https://streamlit.io/) dari `Python` sebagai alat untuk melakukan _deployment_. Untuk melakukan proses deployment, berikut adalah langkah-langkahnya.

1. Clone Repository ini dengan memasukkan syntax berikut ke `command prompt`:
```
git clone https://github.com/PutraAlFarizi15/Face-Recognition-Attendance-System-Using-Facenet.git
```
2. Setelah selesai melakukan `git clone` kemudian masuklah ke lokasi folder git
```
cd Face-Recognition-Attendance-System-Using-Facenet
```
3. Kemudian buatlah `virtual environment` didalam lokasi tadi
```
python -m venv venv
```
4. Aktifkan `virtual environment` dengan syntax berikut
```
venv\scripts\activate
```
5. Jika `virtual environment` sudah aktif, install library yang diperlukan sesuai dengan requirements.txt
```
pip install -r requirements.txt
```
6. Tunggu sampai proses instalasi selesai, kemudian jalankan server untuk database
```
python attendance_server.py
```
7. Setelah menjalankan server buka Command Prompt baru lalu jalankan aplikasi
```
streamlit run app.py
```
Jika semua langkah-langkah sudah dilakukan dengan benar, maka seharusnya akan muncul aplikasi dalam bentuk website yang dapat digunakan, untuk penggunaan secara lengkap dapat melihat video demo pada link berikut
[Demo Video](https://drive.google.com/file/d/1yd4bYKXqXxk3Y4dtZAXfxnlynJWIRmPk/view?usp=sharing) atau secara singkat dengan langkah-langkah berikut
1. Klik **menu** di kiri atas, lalu pilih **add new user**
2. Akan ada form terdiri dari 3 teks name, email, department dan upload gambar user. Isi setiap isian form, setiap selesai satu isian form harus menekan **enter**, tunggu running selesai baru bisa mengisi isian berikutnya, hal ini dilakukan untuk menghindari **Error**. Setelah mengisi form klik **add user** tunggu hingga muncul pemberitahuan **User added successfully!**
3. Klik **menu** kiri atas lalu pilih **attendance**, secara otomatis akan ke halaman absensi dengan pengenalan wajah
4. Klik **start** untuk memulai absensi, di video akan ditampilkan nama karyawan dan otomatis dikirimkan ke data absensi. klik **stop** untuk menghentikan perekaman
5. Untuk melihat isi database dapat menjalankan script di Command Prompt
```
python Database/view_database.py
```
1. untuk liat visualisasy data bisa menjalankan script di cmd 
```
python Database/visulize_data.py
```
selesai

Opsional: Langkah langkah jika Signature berupa file data.pkl dan Database Berupa attendance_system.db dihapus

**Membuat signature:**
1. pada folder makeSignature di file MakeSignatureHaar.ipynb dengan menjalankan file tersebut akan membuat signature yang disimpan di file data.pkl
2. Untuk menguji signature, jalankan file Face Recognition Haar.ipynb perlu diingat saat program berjalan akan menjalankan kamera, untuk menutup kamera kli escape

**Membuat database**
1. Membuat database sesuai dengan rancangan dengan menulis script  Command Prompt
```
python Database/create_database.py 
```
2. Memasukkan data awal ke database sesuai dengan data yang disimpan pada signature script di Command Prompt
```
python Database/update_database.py 
```
3. Lakukan hal sama mulai dari No 6 pada [Instalasi dan Cara Penggunaan](#instalasi-dan-cara-penggunaan)


## Struktur Proyek
- Attendance-System-With-Face-Recognition-Using-Facenet/
  - addData/
    - image1.jpg
    - image2.jpg
    - ...
  - Database/
    - add_user_data.py
    - create_database.py
    - update_database.py
    - view_database.py
    - visualize_data.py
  - fotoKaryawan/
    - image1.jpg
    - image2.jpg
    - ...
  - signatureNotebook/
    - data.pkl
    - Face Recognition Haar.ipynb
    - haarcascade_frontalface_default.xml
    - Make Signature Haar.ipynb
  - app.py
  - attendance_api.py
  - requirements.txt
  - README.md

## Referensi
github: https://github.com/nemuelpah/Face-Recognition-with-FaceNET
