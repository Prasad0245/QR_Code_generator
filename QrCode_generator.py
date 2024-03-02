import tkinter as tk
from tkinter import ttk
import qrcode
import sqlite3
import os

def retrieve_data_from_database():
    conn = sqlite3.connect('QR_Database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT data FROM qr_data')
    data = cursor.fetchall()
    conn.close()
    return data

def generate_qr_code():
    data = entry_data.get()
    filename = entry_filename.get()
    file_format = format_var.get()

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=size_var.get(),
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    output_folder = "output_qr_codes"
    os.makedirs(output_folder, exist_ok=True)

    img.save(os.path.join(output_folder, f"{filename}.{file_format}"))

    # Hide input elements after generating
    label_data.grid_forget()
    entry_data.grid_forget()
    label_filename.grid_forget()
    entry_filename.grid_forget()
    format_menu.grid_forget()
    size_menu.grid_forget()
    button_generate.grid_forget()

    status_label.config(text=f"QR code saved in '{output_folder}' as {filename}.{file_format}", foreground="green")

# Create main window
root = tk.Tk()
root.title("QR Code Generator")
root.geometry("400x300")

# Set style
style = ttk.Style()
style.configure('TLabel', font=('Arial', 12))
style.configure('TButton', font=('Arial', 12))
style.configure('TEntry', font=('Arial', 12))

# Labels
label_data = ttk.Label(root, text="Data:")
label_data.grid(row=0, column=0, padx=5, pady=5, sticky="w")

label_filename = ttk.Label(root, text="Filename:")
label_filename.grid(row=1, column=0, padx=5, pady=5, sticky="w")

label_format = ttk.Label(root, text="File Format:")
label_format.grid(row=2, column=0, padx=5, pady=5, sticky="w")

label_size = ttk.Label(root, text="Size:")
label_size.grid(row=3, column=0, padx=5, pady=5, sticky="w")

# Entry fields
entry_data = ttk.Entry(root, font=('Arial', 12), width=20)
entry_data.grid(row=0, column=1, padx=5, pady=5)

entry_filename = ttk.Entry(root, font=('Arial', 12), width=20)
entry_filename.grid(row=1, column=1, padx=5, pady=5)

file_formats = ["png", "jpg"]
format_var = tk.StringVar(value=file_formats[0])
format_menu = ttk.Combobox(root, textvariable=format_var, values=file_formats, font=('Arial', 12), width=17)
format_menu.grid(row=2, column=1, padx=5, pady=5)

size_var = tk.IntVar(value=10)
size_menu = ttk.Spinbox(root, from_=1, to=20, textvariable=size_var, font=('Arial', 12), width=5)
size_menu.grid(row=3, column=1, padx=5, pady=5)

# Generate button
button_generate = ttk.Button(root, text="Generate QR Code", command=generate_qr_code)
button_generate.grid(row=4, columnspan=2, pady=10)

# Status label
status_label = ttk.Label(root, text="", font=('Arial', 12), foreground="red")
status_label.grid(row=5, columnspan=2)

root.mainloop()
