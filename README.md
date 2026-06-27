# 🎤 Word-Audio-Counter (a.k.a Simple Speech Detector)

A desktop Python application that detects specific spoken phrases in real time using microphone input, maintaining a counter for each detected phrase and storing historical data.

This project was developed with the assistance of Artificial Intelligence tools to accelerate design, implementation, and optimization.

---

# 🚀 Features

- 🎧 Real-time continuous microphone listening  
- 🧠 Multi-phrase detection simultaneously  
- 🔢 Individual counters for each phrase  
- 📜 Live audio transcription log  
- 🗑 Phrase management (add / remove)  
- 💾 Persistent storage using JSON files  
- ⚡ Optimized for low latency performance  

---

# 🧰 Requirements

## 🔹 Python
- Python 3.8 or higher  
- Download: https://www.python.org/downloads/

⚠️ IMPORTANT: during installation make sure to enable:
- ✔ “Add Python to PATH”

---

## 🔹 Required libraries

Install all dependencies using:

```bash
pip install -r requirements.txt
```

# 📦 requirements.txt  
  
```bash  
customtkinter  
sounddevice  
numpy  
faster-whisper  
rapidfuzz
```

# 📁 Installation Guide (Step by Step)

## 1\. Clone the repository


```
git clone https://github.com/your-username/speech-detector-pro.git  
cd speech-detector-pro
```

---

## 2\. Create a virtual environment (recommended)

```
python -m venv venv  
venv\Scripts\activate
```

---

## 3\. Install dependencies


```
pip install -r requirements.txt
```

---

## 4\. Run the application

```
python escuchar.py
```

---

# 🖥️ How to Use

-   Type a phrase in the input field
    
-   Click ➕ Add to register it for detection
    
-   Press **START** to begin listening
    
-   Speak normally: the app will detect phrases in real time
    
-   Each detected phrase increases its counter automatically
    
-   You can remove phrases using the 🗑 icon
    
---

# 📊 Logs System

The bottom section of the application displays:

-   Real-time recognized speech
    
-   Detected matches
    
-   Counter updates
    
---

# ⚙️ Technical Notes

-   Uses `faster-whisper` model in optimized **base** mode
    
-   Chunk-based audio processing for low latency
    
-   Fuzzy matching to improve recognition of similar phrases
    
-   Built with `customtkinter` for a modern UI
    
-   Multithreaded architecture to avoid UI freezing
    
-   JSON-based persistence system
    
---

# 🤖 Artificial Intelligence Usage

This project was built with assistance from AI tools for:

-   Software architecture design
    
-   Audio processing optimization
    
-   Speech recognition implementation
    
-   UI/UX improvements
    
-   Latency reduction techniques
    
-   Code generation and refactoring
  
---  
  
