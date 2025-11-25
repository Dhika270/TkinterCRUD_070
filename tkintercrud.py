import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ====================================
#  DATABASE
# ====================================

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

# ====================================
#  FUNGSI PREDIKSI
# ====================================

def prediksi(bio, fis, ing):
    if bio > fis and bio > ing:
        return "Kedokteran"
    elif fis > bio and fis > ing:
        return "Teknik"
    else:
        return "Bahasa"

# ====================================
#  CREATE (SUBMIT)
# ====================================

def submit():
    try:
        nama = entry_nama.get()
        bio = int(entry_bio.get())
        fis = int(entry_fis.get())
        ing = int(entry_ing.get())

        hasil = prediksi(bio, fis, ing)

        cur.execute("""
            INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
            VALUES (?, ?, ?, ?, ?)
        """, (nama, bio, fis, ing, hasil))
        conn.commit()

        messagebox.showinfo("Sukses", "Data berhasil disimpan!")
        tampilkan_data()
        reset_input()

    except ValueError:
        messagebox.showerror("Error", "Nilai harus berupa angka!")

# ====================================
#  READ (TAMPILKAN DATA)
# ====================================

def tampilkan_data():
    tabel.delete(*tabel.get_children())
    cur.execute("SELECT * FROM nilai_siswa")
    rows = cur.fetchall()
    for row in rows:
        tabel.insert("", tk.END, values=row)

# ====================================
#  UPDATE
# ====================================

def update_data():
    try:
        selected = tabel.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih data yang ingin diupdate!")
            return

        item = tabel.item(selected)
        id_val = item['values'][0]

        nama = entry_nama.get()
        bio = int(entry_bio.get())
        fis = int(entry_fis.get())
        ing = int(entry_ing.get())
        hasil = prediksi(bio, fis, ing)

        cur.execute("""
            UPDATE nilai_siswa
            SET nama_siswa=?, biologi=?, fisika=?, inggris=?, prediksi_fakultas=?
            WHERE id=?
        """, (nama, bio, fis, ing, hasil, id_val))
        conn.commit()

        messagebox.showinfo("Sukses", "Data berhasil diupdate!")
        tampilkan_data()
        reset_input()

    except ValueError:
        messagebox.showerror("Error", "Nilai harus angka!")

# ====================================
#  DELETE
# ====================================

def delete_data():
    selected = tabel.selection()
    if not selected:
        messagebox.showwarning("Peringatan", "Pilih data yang ingin dihapus!")
        return

    item = tabel.item(selected)
    id_val = item['values'][0]

    cur.execute("DELETE FROM nilai_siswa WHERE id=?", (id_val,))
    conn.commit()

    messagebox.showinfo("Sukses", "Data berhasil dihapus!")
    tampilkan_data()
    reset_input()

# ====================================
#  KETIKA DATA DIKLIK DARI TABEL
# ====================================

def pilih_data(event):
    selected = tabel.selection()
    if selected:
        item = tabel.item(selected)
        _, nama, bio, fis, ing, _ = item["values"]

        entry_nama.delete(0, tk.END)
        entry_bio.delete(0, tk.END)
        entry_fis.delete(0, tk.END)
        entry_ing.delete(0, tk.END)

        entry_nama.insert(0, nama)
        entry_bio.insert(0, bio)
        entry_fis.insert(0, fis)
        entry_ing.insert(0, ing)

# ====================================
#  RESET INPUT
# ====================================

def reset_input():
    entry_nama.delete(0, tk.END)
    entry_bio.delete(0, tk.END)
    entry_fis.delete(0, tk.END)
    entry_ing.delete(0, tk.END)

# ====================================
#  GUI
# ====================================

root = tk.Tk()
root.title("Aplikasi Prediksi Prodi Pilihan (CRUD)")
root.geometry("650x500")

title = tk.Label(root, text="Aplikasi Prediksi Prodi Pilihan", font=("Arial", 16, "bold"))
title.pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=10)

# INPUT
tk.Label(frame, text="Nama Siswa").grid(row=0, column=0)
entry_nama = tk.Entry(frame, width=20)
entry_nama.grid(row=0, column=1)

tk.Label(frame, text="Nilai Biologi").grid(row=1, column=0)
entry_bio = tk.Entry(frame, width=10)
entry_bio.grid(row=1, column=1)

tk.Label(frame, text="Nilai Fisika").grid(row=2, column=0)
entry_fis = tk.Entry(frame, width=10)
entry_fis.grid(row=2, column=1)

tk.Label(frame, text="Nilai Inggris").grid(row=3, column=0)
entry_ing = tk.Entry(frame, width=10)
entry_ing.grid(row=3, column=1)

# BUTTON CRUD
tk.Button(root, text="Submit Nilai", bg="lightblue", command=submit).pack(pady=5)
tk.Button(root, text="Update Data", bg="orange", command=update_data).pack(pady=5)
tk.Button(root, text="Delete Data", bg="red", fg="white", command=delete_data).pack(pady=5)

# TABEL
header = ["ID", "Nama", "Biologi", "Fisika", "Inggris", "Prediksi"]
tabel = ttk.Treeview(root, columns=header, show="headings")
tabel.pack(fill=tk.BOTH, expand=True)

for col in header:
    tabel.heading(col, text=col)
    tabel.column(col, width=100)

tabel.bind("<ButtonRelease-1>", pilih_data)

tampilkan_data()
root.mainloop()
