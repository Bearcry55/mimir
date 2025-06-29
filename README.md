# 🧠 Mimir

**Mimir** is a simple, local, offline AI helper for Linux terminal users.  
It uses [Ollama](https://ollama.com/) with a **lightweight TinyLlama model** by default.

Mimir can:
- Answer Linux terminal questions
- Read your system logs for context (`--logs`)
- Read your recent shell command history for context (`--history`)

---

## ⚡ Features

✅ Fully local — runs with your local Ollama server  
✅ Tiny LLM (TinyLlama) for fast offline answers  
✅ Clear, concise help for Linux beginners  
✅ Optional flags for extra context (logs, history)  
✅ Easy to install with one script

---

## 🗂️ Project Structure

.
├── Cargo.toml
├── src/
│ └── main.rs
├── installer.sh
└── README.md 

---

## 🛠️ Install

**1️⃣ Clone the repo**

```bash
git clone https://github.com/YOUR_USERNAME/mimir.git
cd mimir
chmod +x installer.sh
./installer.sh
```
This will:

    Check if you have Ollama installed and running

    Install mimir dependencies

    Build the binary

By default, Mimir uses the TinyLlama model.
To switch models, change the model name in main.rs:

"model": "tinyllama"

Replace "tinyllama" with any Ollama-supported model you have installed.

# 🧩 Usage

Run Mimir with or without flags:

cargo run -- --logs --history

Or, after installing:

mimir --logs --history

# How it works:

    --logs → Mimir scans /var/log/syslog for context

    --history → Mimir includes ~/.bash_history

    If you skip a flag, that source is skipped — no interactive prompts

    Then, Mimir asks for your question or extra info

    Mimir answers clearly and concisely
    Example:

mimir --logs --history

# or minimal:

mimir

# ✅ Flags
Flag	What it does
--logs	Read system logs for context
--history	Include recent shell commands
(none)	Just your question, no extra context
# 📦 Notes

    Make sure Ollama is installed and running (ollama serve)

    TinyLlama model must be pulled: ollama pull tinyllama

    You can switch to any other local model by editing main.rs

# 💡 Example Questions

    How do I check disk space?

    How do I create a new user in Linux?

    Why is my server using 100% CPU?

# 👤 Author

Made by Deep Narayan Banerjee (@bearcry55)
🫶 License

MIT — feel free to modify and share!


