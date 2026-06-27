import customtkinter as ctk
import sounddevice as sd
import numpy as np
import threading
import json
import os
import sys
from rapidfuzz import fuzz
from faster_whisper import WhisperModel

sys.stdout.reconfigure(encoding='utf-8')

# -----------------------
# UI CONFIG
# -----------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# -----------------------
# STORAGE
# -----------------------
DB_FILE = "frases.json"

if os.path.exists(DB_FILE):
    data = json.load(open(DB_FILE, "r", encoding="utf-8"))
else:
    data = {}

def save_db():
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# -----------------------
# MODEL
# -----------------------
model = WhisperModel(
    "small",   # mejor precisión
    device="cpu",
    compute_type="int8"
)

fs = 16000
duracion = 4
solape = 1

running = False

buffer = np.array([], dtype=np.float32)

# -----------------------
# AUDIO LOOP
# -----------------------
def escuchar():
    global buffer

    while running:

        audio = sd.rec(int(duracion * fs),
                       samplerate=fs,
                       channels=1,
                       dtype=np.float32)

        sd.wait()
        audio = audio.flatten()

        buffer = np.concatenate((buffer[-solape*fs:], audio))

        segments, _ = model.transcribe(buffer)

        texto = " ".join(s.text.lower() for s in segments)

        status_label.configure(text="🎧 Escuchando...")

        for frase in list(data.keys()):

            # fuzzy match para palabras mal reconocidas
            score = fuzz.partial_ratio(frase, texto)

            if frase in texto or score > 85:
                data[frase] += 1
                save_db()
                refresh_list()

# -----------------------
# UI LOGIC
# -----------------------
def start():
    global running
    running = True
    threading.Thread(target=escuchar, daemon=True).start()
    status_label.configure(text="🟢 ACTIVO")

def stop():
    global running
    running = False
    status_label.configure(text="🔴 PARADO")

def add_phrase():
    frase = entry.get().strip().lower()
    if frase and frase not in data:
        data[frase] = 0
        save_db()
        refresh_list()

def remove_phrase():
    frase = entry.get().strip().lower()
    if frase in data:
        del data[frase]
        save_db()
        refresh_list()

def select_phrase(event):
    selection = listbox.get(listbox.curselection())
    frase = selection.split(" → ")[0]
    entry.delete(0, "end")
    entry.insert(0, frase)

def refresh_list():
    listbox.delete(0, "end")
    for k, v in data.items():
        listbox.insert("end", f"{k} → {v}")

# -----------------------
# UI
# -----------------------
root = ctk.CTk()
root.title("🎤 Speech Detector PRO")
root.geometry("520x600")

entry = ctk.CTkEntry(root, width=400, placeholder_text="Escribe frase...")
entry.pack(pady=10)

btn_frame = ctk.CTkFrame(root)
btn_frame.pack()

ctk.CTkButton(btn_frame, text="➕ Añadir", command=add_phrase).grid(row=0, column=0, padx=5)
ctk.CTkButton(btn_frame, text="➖ Quitar", command=remove_phrase).grid(row=0, column=1, padx=5)

ctk.CTkButton(root, text="▶ START", command=start).pack(pady=5)
ctk.CTkButton(root, text="⏹ STOP", command=stop).pack(pady=5)

status_label = ctk.CTkLabel(root, text="🔴 PARADO")
status_label.pack(pady=10)

listbox = ctk.CTkTextbox(root, width=450, height=300)
listbox.pack(pady=10)

def refresh_list():
    listbox.delete("0.0", "end")
    for k, v in data.items():
        listbox.insert("end", f"{k} → {v}\n")

listbox.bind("<Button-1>", select_phrase)

refresh_list()

root.mainloop()