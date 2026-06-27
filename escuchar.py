import sounddevice as sd
import numpy as np
import threading
import json
import os
import sys
import tkinter as tk
from faster_whisper import WhisperModel

sys.stdout.reconfigure(encoding='utf-8')

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
# WHISPER MODEL
# -----------------------
model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

fs = 16000
duracion = 4
solape = 1

# -----------------------
# STATE
# -----------------------
running = False
current_phrase = ""
current_count = 0
guardar = False

buffer_total = np.array([], dtype=np.float32)

# -----------------------
# AUDIO ENGINE
# -----------------------
def escuchar():
    global buffer_total, current_count, running

    while running:

        audio = sd.rec(
            int(duracion * fs),
            samplerate=fs,
            channels=1,
            dtype=np.float32
        )

        sd.wait()
        audio = audio.flatten()

        buffer_total = np.concatenate((buffer_total[-solape*fs:], audio))

        segments, _ = model.transcribe(buffer_total)

        texto = " ".join(s.text.lower() for s in segments)

        print("Detectado:", texto)

        if current_phrase and current_phrase.lower() in texto:
            current_count += texto.count(current_phrase.lower())

            if guardar:
                data[current_phrase] = current_count
                save_db()

            actualizar_ui()

# -----------------------
# UI ACTIONS
# -----------------------
def start():
    global running, current_phrase, current_count, guardar

    current_phrase = entry.get().strip().lower()

    if not current_phrase:
        return

    guardar = var_guardar.get()

    if current_phrase in data:
        current_count = data[current_phrase]
    else:
        current_count = 0

    running = True

    threading.Thread(target=escuchar, daemon=True).start()

def stop():
    global running
    running = False

def actualizar_ui():
    label_count.config(text=f"Contador: {current_count}")
    refresh_list()

def refresh_list():
    listbox.delete(0, tk.END)
    for k, v in data.items():
        listbox.insert(tk.END, f"{k} → {v}")

# -----------------------
# UI
# -----------------------
root = tk.Tk()
root.title("Detector de Frases PRO")
root.geometry("420x500")

tk.Label(root, text="🎤 Frase a detectar").pack()

entry = tk.Entry(root, width=40)
entry.pack(pady=5)

var_guardar = tk.BooleanVar()
tk.Checkbutton(root, text="Guardar historial", variable=var_guardar).pack()

tk.Button(root, text="START", command=start).pack(pady=5)
tk.Button(root, text="STOP", command=stop).pack()

label_count = tk.Label(root, text="Contador: 0", font=("Arial", 18))
label_count.pack(pady=10)

tk.Label(root, text="Frases guardadas").pack()

listbox = tk.Listbox(root, width=50)
listbox.pack(pady=10)

refresh_list()

root.mainloop()