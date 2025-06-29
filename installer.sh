#!/bin/bash

# 🧠 Mimir Installation Script
# Installs Ollama, TinyLlama, and Mimir Terminal AI Assistant

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Emojis for better UX
CHECK="✅"
CROSS="❌"
ARROW="➤"
ROCKET="🚀"
BRAIN="🧠"
GEAR="⚙️"
DOWNLOAD="📥"

print_header() {
    echo -e "${PURPLE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    🧠 MIMIR INSTALLER                        ║"
    echo "║              Terminal AI Assistant Setup                     ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_step() {
    echo -e "${CYAN}${ARROW} $1${NC}"
}

print_success() {
    echo -e "${GREEN}${CHECK} $1${NC}"
}

print_error() {
    echo -e "${RED}${CROSS} $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        print_error "This script should not be run as root"
        exit 1
    fi
}

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
        if command -v apt-get &> /dev/null; then
            DISTRO="debian"
        elif command -v yum &> /dev/null; then
            DISTRO="rhel"
        elif command -v pacman &> /dev/null; then
            DISTRO="arch"
        else
            DISTRO="unknown"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
        DISTRO="macos"
    else
        print_error "Unsupported operating system: $OSTYPE"
        exit 1
    fi
}

# Check system requirements
check_requirements() {
    print_step "Checking system requirements..."
    
    if [[ "$OS" == "linux" ]]; then
        MEMORY_KB=$(grep MemTotal /proc/meminfo | awk '{print $2}')
        MEMORY_GB=$((MEMORY_KB / 1024 / 1024))
    elif [[ "$OS" == "macos" ]]; then
        MEMORY_BYTES=$(sysctl -n hw.memsize)
        MEMORY_GB=$((MEMORY_BYTES / 1024 / 1024 / 1024))
    fi
    
    if [[ $MEMORY_GB -lt 2 ]]; then
        print_warning "Low memory detected (${MEMORY_GB}GB). Mimir needs at least 2GB RAM."
        echo "Continue anyway? (y/N)"
        read -r response
        if [[ ! "$response" =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is required but not installed"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    if ! python3 -c 'import sys; exit(0 if sys.version_info >= (3, 7) else 1)'; then
        print_error "Python 3.7+ required. Found: $PYTHON_VERSION"
        exit 1
    fi
    
    print_success "System requirements met (${MEMORY_GB}GB RAM, Python $PYTHON_VERSION)"
}

# Install system dependencies
install_dependencies() {
    print_step "Installing system dependencies..."
    
    case $DISTRO in
        "debian")
            sudo apt-get update -qq
            sudo apt-get install -y curl wget python3-pip
            ;;
        "rhel")
            sudo yum install -y curl wget python3-pip
            ;;
        "arch")
            sudo pacman -S --noconfirm curl wget python-pip
            ;;
        "macos")
            if ! command -v brew &> /dev/null; then
                print_error "Homebrew is required on macOS. Please install it first: https://brew.sh"
                exit 1
            fi
            brew install curl wget python3
            ;;
        *)
            print_warning "Unknown distribution. Please ensure curl, wget, and python3-pip are installed."
            ;;
    esac
    
    print_success "Dependencies installed"
}

# Install Ollama
install_ollama() {
    print_step "Installing Ollama..."
    
    if command -v ollama &> /dev/null; then
        print_success "Ollama already installed"
        return 0
    fi
    
    curl -fsSL https://ollama.ai/install.sh | sh
    
    if [[ "$OS" == "linux" ]]; then
        if command -v systemctl &> /dev/null; then
            sudo systemctl enable ollama
            sudo systemctl start ollama
        else
            nohup ollama serve > /dev/null 2>&1 &
        fi
    elif [[ "$OS" == "macos" ]]; then
        nohup ollama serve > /dev/null 2>&1 &
    fi
    
    print_step "Waiting for Ollama to start..."
    sleep 5
    
    if ! curl -s http://localhost:11434/api/tags > /dev/null; then
        print_error "Failed to start Ollama service"
        exit 1
    fi
    
    print_success "Ollama installed and running"
}

# Pull TinyLlama model
install_tinyllama() {
    print_step "Installing TinyLlama model (1.1GB download)..."
    
    if ollama list | grep -q "tinyllama:latest"; then
        print_success "TinyLlama already installed"
        return 0
    fi
    
    echo -e "${YELLOW}${DOWNLOAD} Downloading TinyLlama model... This may take a few minutes${NC}"
    
    if ! ollama pull tinyllama:latest; then
        print_error "Failed to download TinyLlama model"
        exit 1
    fi
    
    print_success "TinyLlama model installed"
}

# Install Python dependencies
install_python_deps() {
    print_step "Installing Python dependencies..."
    
    cat > /tmp/mimir_requirements.txt << 'EOF'
requests>=2.25.0
argparse
EOF
    
    if ! python3 -m pip install -r /tmp/mimir_requirements.txt --user; then
        print_error "Failed to install Python dependencies"
        exit 1
    fi
    
    rm -f /tmp/mimir_requirements.txt
    print_success "Python dependencies installed"
}

# Install Mimir
install_mimir() {
    print_step "Installing Mimir..."
    
    INSTALL_DIR="$HOME/.local/bin"
    mkdir -p "$INSTALL_DIR"
    
    if [[ -f "mimir.py" ]]; then
        cp mimir.py "$INSTALL_DIR/mimir"
    else
        curl -fsSL https://raw.githubusercontent.com/Bearcry55/mimir/main/mimir.py -o "$INSTALL_DIR/mimir"
    fi
    
    chmod +x "$INSTALL_DIR/mimir"
    
    SHELL_RC=""
    if [[ "$SHELL" == *"bash"* ]]; then
        SHELL_RC="$HOME/.bashrc"
    elif [[ "$SHELL" == *"zsh"* ]]; then
        SHELL_RC="$HOME/.zshrc"
    elif [[ "$SHELL" == *"fish"* ]]; then
        SHELL_RC="$HOME/.config/fish/config.fish"
    fi
    
    if [[ -n "$SHELL_RC" && -f "$SHELL_RC" ]]; then
        if ! grep -q "$INSTALL_DIR" "$SHELL_RC"; then
            echo "export PATH=\"\$PATH:$INSTALL_DIR\"" >> "$SHELL_RC"
            print_success "Added Mimir to PATH in $SHELL_RC"
        fi
    fi
    
    print_success "Mimir installed to $INSTALL_DIR/mimir"
}

test_installation() {
    print_step "Testing installation..."
    
    if ! curl -s http://localhost:11434/api/tags > /dev/null; then
        print_error "Ollama is not responding"
        return 1
    fi
    
    if ! ollama list | grep -q "tinyllama:latest"; then
        print_error "TinyLlama model not found"
        return 1
    fi
    
    if [[ -x "$HOME/.local/bin/mimir" ]]; then
        print_success "Installation test passed"
        return 0
    else
        print_error "Mimir executable not found"
        return 1
    fi
}

show_completion() {
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                   🎉 INSTALLATION COMPLETE! 🎉               ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    echo -e "${CYAN}🚀 Quick Start:${NC}"
    echo "   • Restart your terminal or run: source ~/.bashrc"
    echo "   • Try: mimir \"show running processes\""
    echo "   • Help: mimir --help"
    echo ""
    echo -e "${CYAN}📚 Examples:${NC}"
    echo "   mimir \"find large files\""
    echo "   mimir \"check disk space\""
    echo "   mimir \"show network connections\""
    echo ""
    echo -e "${CYAN}⚙️  Configuration:${NC}"
    echo "   • Config file: ~/mimir_config.json"
    echo "   • Show config: mimir --config"
    echo "   • Switch models: mimir --select-model"
    echo ""
    echo -e "${YELLOW}💡 Tip: Add $HOME/.local/bin to your PATH if commands don't work${NC}"
}

main() {
    print_header
    check_root
    detect_os
    check_requirements
    install_dependencies
    install_ollama
    install_tinyllama
    install_python_deps
    install_mimir
    
    if test_installation; then
        show_completion
    else
        print_error "Installation completed with errors. Please check the output above."
        exit 1
    fi
}

main "$@"
