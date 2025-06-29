#!/usr/bin/env bash

# Mimir Installer Script

set -e

echo "🚀 Installing Mimir..."

# 1. Check Rust installation
if ! command -v cargo &> /dev/null; then
  echo "Rust is not installed. Installing Rust using rustup..."
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
  source "$HOME/.cargo/env"
else
  echo "Rust is already installed ✅"
fi

# 2. Install Ollama if not installed
if ! command -v ollama &> /dev/null; then
  echo "Ollama is not installed. Please follow instructions at https://ollama.com to install it."
  exit 1
else
  echo "Ollama is already installed ✅"
fi

# 3. Build the project
echo "Building Mimir..."
cargo build --release

# 4. Create ~/.local/bin if it doesn't exist
mkdir -p ~/.local/bin

# 5. Copy the built binary
cp target/release/mimir ~/.local/bin/

echo "✅ Mimir installed successfully!"
echo ""
echo "Add ~/.local/bin to your PATH if it's not there:"
echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
echo ""
echo "Run Mimir with:"
echo "  mimir"
echo ""
echo "🚀 Done!"
