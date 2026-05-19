# AI-tutor-in-terminal

````md
# 🦆 Rubber Duck AI

A local AI tutor + rubber duck debugger that runs directly inside your VS Code terminal using Ollama and Python. No API keys. Runs offline after setup.

It can:
- Explain coding concepts
- Help debug code
- Guide you using Socratic questioning
- Remember previous chats even after closing the terminal

---

# 📦 Prerequisites

Before starting, make sure you have:

- Python installed
- VS Code installed
- Git installed
- Basic knowledge of how to clone a GitHub repo

---

# 🚀 Setup Guide

## Step 1 — Install Ollama

Download and install Ollama from:

https://ollama.com/download

After installing, restart your terminal.

---

## Step 2 — Clone the Repository

Clone the repo and open the project folder in VS Code.

To clone: (command)

```bash
git clone YOUR_REPO_LINK
cd rubber-duck-ai
```

---

## Step 3 — Check if Ollama is Installed

Open a new terminal inside the project folder and run:

```bash
ollama --version
```

If installed correctly, it should display the Ollama version.

---

## Step 4 — Download an AI Model

### Recommended

```bash
ollama pull llama3.2
```

Requires around 8GB RAM.

---

### If your PC is slower

```bash
ollama pull llama2
```

---

### Lightweight Option

```bash
ollama pull phi3
```

This step may take a while depending on your internet speed. Be patient.

---

## Step 5 — Create a Virtual Environment

```bash
python -m venv venv
```

---

## Step 6 — Activate the Virtual Environment

### PowerShell

```bash
.\venv\Scripts\Activate.ps1
```

---

### If that doesn't work

```bash
venv\Scripts\activate.bat
```

---

## Step 7 — Install Ollama Python Package

```bash
pip install ollama
```

---

## Step 8 — Install Project Requirements

```bash
pip install -r requirements.txt
```

---

## Step 9 — Set Your Model Name

Open:

```text
main.py
```

Replace:

```python
CHAT_MODEL = "llama3.2"
```

with the model you downloaded.

Example:

If you ran:

```bash
ollama pull llama2
```

Then change it to:

```python
CHAT_MODEL = "llama2"
```

---

## Step 10 — Run the App

```bash
python main.py
```

---

# 💬 Commands

You can load a code file directly into the AI using:

you can just drag the file from the left panel of vs code into the terminal!

```text
/read <filename.py>
```

Example:

```text
/read test.py
```

The AI will read your exact code and help you debug or understand it without assuming extra variables or code outside the file.

After loading the file, you can ask things like:

```text
Why is this function returning None?

Why is my loop infinite?



# 🧠 Features

* Local AI assistant
* Rubber duck debugging
* Streaming AI responses
* Persistent chat memory
* Lightweight terminal interface
* Beginner-friendly setup

---

# ⚠️ Notes

* `chat_history.json` stores previous conversations locally.
* If memory becomes too long, the app will warn you.
* No paid APIs required.
* Everything runs locally on your machine.

---

# 🦆 Example Prompts

```text
Explain recursion simply

Why is my loop not stopping?

Teach me linked lists

How does binary search work?

Help me debug this Python error
```

---

#  Built With

* Ollama
* Python
* VS Code

```
```
