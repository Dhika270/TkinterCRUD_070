import tkinter as tk
import sqlite3
from tkinter import messagebox

# -------------------------
#  DATABASE
# -------------------------

conn = sqlite3.connect("nilai_siswa.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS nilai_siswa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_siswa TEXT,
    biologi INTEGER,
    fisika INTEGER,
    inggris INTEGER,
    prediksi_fakultas TEXT
)
""")
conn.commit()

# -------------------------
#  FUNGSI PREDIKSI
# -------------------------

def prediksi(bio, fis, ing):
    terbesar = max(bio, fis, ing)

    if terbesar == bio:
        return "Kedokteran"
    elif terbesar == fis:
        return "Teknik"
    else:
        return "Bahasa"

# -------------------------
#  GUI TKINTER
# -------------------------

root = tk.Tk()
root.title("Aplikasi Prediksi Prodi Pilihan")
root.geometry("350x350")

judul = tk.Label(root, text="Aplikasi Prediksi Prodi Pilihan", font=("Arial", 14, "bold"))
judul.pack(pady=10)

frm = tk.Frame(root)
frm.pack(pady=10)

# INPUT NAMA
tk.Label(frm, text="Nama Siswa").grid(row=0, column=0, sticky="w")
entry_nama = tk.Entry(frm, width=20)
entry_nama.grid(row=0, column=1)

# INPUT NILAI BIOLOGI
tk.Label(frm, text="Nilai Biologi").grid(row=1, column=0, sticky="w")
entry_bio = tk.Entry(frm, width=10)
entry_bio.grid(row=1, column=1)

# INPUT NILAI FISIKA
tk.Label(frm, text="Nilai Fisika").grid(row=2, column=0, sticky="w")
entry_fis = tk.Entry(frm, width=10)
entry_fis.grid(row=2, column=1)

# INPUT NILAI INGGRIS
tk.Label(frm, text="Nilai Inggris").grid(row=3, column=0, sticky="w")
entry_ing = tk.Entry(frm, width=10)
entry_ing.grid(row=3, column=1)

# -------------------------
#  SIMPAN + PREDIKSI
# -------------------------

def submit():
    try:
        nama = entry_nama.get()
        bio = int(entry_bio.get())
        fis = int(entry_fis.get())
        ing = int(entry_ing.get())

        hasil_prediksi = prediksi(bio, fis, ing)

        # SIMPAN DATABASE
        cur.execute("""
            INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
            VALUES (?, ?, ?, ?, ?)
        """, (nama, bio, fis, ing, hasil_prediksi))

        conn.commit()

        hasil_label.config(text=f"Hasil Prediksi: {hasil_prediksi}")
        messagebox.showinfo("Sukses", "Data berhasil disimpan!")

    except ValueError:
        messagebox.showerror("Error", "Masukkan nilai dengan angka!")

# BUTTON
btn_submit = tk.Button(root, text="Submit Nilai", command=submit, bg="lightblue")
btn_submit.pack(pady=10)

hasil_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
hasil_label.pack(pady=10)

root.mainloop()