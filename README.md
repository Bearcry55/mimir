# 🧠 Mimir - Terminal AI Assistant

> **Your intelligent terminal companion powered by local LLMs**

Mimir is a lightweight, fast terminal troubleshooting assistant that runs entirely locally using Ollama. Get instant shell commands for any task without leaving your terminal.



## ✨ Features

- 🚀 **Lightning Fast** - Uses TinyLlama by default for instant responses
- 🔒 **100% Local** - No API keys, no data sharing, complete privacy
- 🎯 **Command Focused** - Returns pure shell commands, no explanations
- 📚 **Smart History** - Searches your bash history and previous interactions
- 🔧 **Configurable** - Multiple model profiles and customizable settings
- ⭐ **Model Management** - Easy switching between different LLM models
- 📖 **Man Page Integration** - Quick access to manual pages

## 🚀 Quick Start

### One-Line Installation
```bash
curl -fsSL https://raw.githubusercontent.com/your-username/mimir/main/install.sh | bash
```

### Manual Installation
```bash
git clone https://github.com/your-username/mimir.git
cd mimir
chmod +x install.sh
./install.sh
```

## 💡 Usage Examples

```bash
# Get shell commands instantly
mimir "show running processes"
# Output: ps aux

mimir "find large files"
# Output: find / -size +100M 2>/dev/null

mimir "check disk space"
# Output: df -h

# Search your command history
mimir "docker" --history

# Search previous Mimir interactions
mimir "processes" --logs

# Get man page summaries
mimir "grep" --man
```

## 🎛️ Model Management

```bash
# List available models
mimir --models

# Switch models on the fly
mimir --model "llama3.2:3b"

# Interactive model selection
mimir --select-model

# Use model profiles
mimir --profile powerful

# Reset to TinyLlama default
mimir --reset-default
```

## ⚙️ Configuration

Mimir creates a `mimir_config.json` file for customization:

```json
{
  "model": "tinyllama:latest",
  "temperature": 0.1,
  "use_default_model": true,
  "profiles": {
    "lightweight": {"model": "tinyllama:latest", "temperature": 0.1},
    "balanced": {"model": "llama3.2:1b", "temperature": 0.2},
    "powerful": {"model": "llama3.2:3b", "temperature": 0.1}
  }
}
```

### Available Commands

| Command | Description |
|---------|-------------|
| `mimir "query"` | Get shell command for your query |
| `--models` | List all available Ollama models |
| `--model MODEL` | Set specific model to use |
| `--select-model` | Interactive model selection menu |
| `--profile PROFILE` | Switch to predefined profile |
| `--config` | Show current configuration |
| `--history` | Search bash history with query |
| `--logs` | Search previous Mimir interactions |
| `--man` | Show man page summary |
| `--favorites` | Show favorite models |
| `--reset-default` | Reset to TinyLlama default |
| `--temp FLOAT` | Set model temperature (0.0-1.0) |

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Terminal    │───▶│      Mimir      │───▶│     Ollama      │
│   (Your Query)  │    │   (Processor)   │    │   (Local LLM)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  Command Output │
                       │   (Pure Shell)  │
                       └─────────────────┘
```

## 🔧 Requirements

- **Python 3.7+**
- **Ollama** (automatically installed by installer)
- **Linux/macOS** (Windows support via WSL)
- **2GB+ RAM** (for TinyLlama)

## 📋 Installation Details

The installer script will:

1. ✅ Install Ollama if not present
2. ✅ Pull TinyLlama model (1.1GB)
3. ✅ Install Python dependencies
4. ✅ Make `mimir` globally available
5. ✅ Create default configuration

## 🎯 Why Mimir?

- **Privacy First**: Everything runs locally, no data leaves your machine
- **Terminal Native**: Designed for command-line workflows
- **Lightweight**: Uses efficient models for fast responses
- **No Subscriptions**: Free and open source forever
- **Offline Ready**: Works without internet after initial setup

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) for making local LLMs accessible
- [TinyLlama](https://github.com/jzhang38/TinyLlama) for the efficient base model
- The open source AI community

## 📞 Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/your-username/mimir/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/your-username/mimir/discussions)
- 📖 **Documentation**: [Wiki](https://github.com/your-username/mimir/wiki)

---

**Made with ❤️ for terminal enthusiasts**

*"In Norse mythology, Mimir was known for his knowledge and wisdom. Our Mimir brings that same wisdom to your terminal."*
