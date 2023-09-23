import sqlite3
import streamlit as st
import pandas as pd

# Buat koneksi ke database SQLite
conn = sqlite3.connect('cluster_data.db')  # Ganti dengan nama database Anda
cursor = conn.cursor()

# Path lengkap ke file CSV
csv_file_path = 'D:\SEO Analysis\pages\cluster_data.csv'

# Membaca data dari file CSV
df = pd.read_csv(csv_file_path)  # Membaca data dari file CSV

# Buat tabel jika belum ada
cursor.execute('''
    CREATE TABLE IF NOT EXISTS data (
        URL TEXT,
        Cluster1 TEXT,
        Cluster2 TEXT
    )
''')

# Masukkan data ke dalam tabel SQLite
for index, row in df.iterrows():
    url = row['URL']
    cluster1 = row['Cluster1']
    cluster2 = row['Cluster2']
    cursor.execute("INSERT INTO data (URL, Cluster1, Cluster2) VALUES (?, ?, ?)", (url, cluster1, cluster2))

# Commit perubahan ke dalam database
conn.commit()

# Tampilkan data yang telah dimasukkan
cursor.execute("SELECT * FROM data")
data = cursor.fetchall()

# Menampilkan data dalam tabel Streamlit
st.title("Data Cluster")
st.write(data)

# Tutup koneksi ke database
conn.close()
