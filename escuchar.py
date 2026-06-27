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
    "small",
    device="cpu",
    compute_type="int8"
)

fs = 16000
duracion = 4
solape = 1

running = False
buffer = np.array([], dtype=np.float32)

# -----------------------
# AUDIO LOG
# -----------------------
log_lines = []

def add_log(text):
    log_lines.append(text)
    if len(log_lines) > 50:
        log_lines.pop(0)

    log_box.configure(state="normal")
    log_box.delete("0.0", "end")
    log_box.insert("0.0", "\n".join(log_lines))
    log_box.configure(state="disabled")

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

        add_log(f"🗣 {texto}")

        for frase in list(data.keys()):

            score = fuzz.partial_ratio(frase, texto)

            if frase in texto or score > 85:
                data[frase] += 1
                save_db()
                refresh_list()
                add_log(f"🔥 MATCH: '{frase}' → {data[frase]}")

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

def remove_phrase(phrase):
    if phrase in data:
        del data[phrase]
        save_db()
        refresh_list()

# -----------------------
# UI RENDER LIST (CON BOTÓN DELETE)
# -----------------------
def refresh_list():

    for widget in list_frame.winfo_children():
        widget.destroy()

    for k, v in data.items():

        row = ctk.CTkFrame(list_frame)
        row.pack(fill="x", pady=2)

        label = ctk.CTkLabel(row, text=f"{k} → {v}", anchor="w")
        label.pack(side="left", padx=10)

        btn = ctk.CTkButton(
            row,
            text="🗑",
            width=40,
            command=lambda k=k: remove_phrase(k)
        )
        btn.pack(side="right", padx=5)

# -----------------------
# UI
# -----------------------
root = ctk.CTk()
root.title("Speech Detector")
root.geometry("650x750")

entry = ctk.CTkEntry(root, width=400, placeholder_text="Escribe frase...")
entry.pack(pady=10)

ctk.CTkButton(root, text="➕ Añadir frase", command=add_phrase).pack()

ctk.CTkButton(root, text="▶ START", command=start).pack(pady=5)
ctk.CTkButton(root, text="⏹ STOP", command=stop).pack()

status_label = ctk.CTkLabel(root, text="🔴 PARADO")
status_label.pack(pady=10)

# -----------------------
# LISTA FRAME
# -----------------------
list_frame = ctk.CTkScrollableFrame(root, width=600, height=250)
list_frame.pack(pady=10)

# -----------------------
# LOG FRAME
# -----------------------
ctk.CTkLabel(root, text="📜 LOG").pack()

log_box = ctk.CTkTextbox(root, width=600, height=200)
log_box.pack()
log_box.configure(state="disabled")

refresh_list()

root.mainloop()