#!/usr/bin/env python3
import argparse
import os
import re
import subprocess
import requests
import json
from datetime import datetime

# === Default Config ===
# TinyLlama is the default model - lightweight and fast for terminal use
DEFAULT_MODEL = "tinyllama:latest"

DEFAULT_CONFIG = {
    "model": DEFAULT_MODEL,  # Always defaults to TinyLlama unless user changes config
    "ollama_url": "http://localhost:11434",
    "temperature": 0.1,
    "max_response_length": 50,
    "stream_responses": False,
    "log_file": "mimir_history.log",
    "bash_history": "~/.bash_history",
    "timeout_seconds": 30,
    "max_history_search": 20,
    "use_default_model": True,  # If True, ignores config model and uses DEFAULT_MODEL
    "profiles": {
        "lightweight": {
            "model": "tinyllama:latest",
            "temperature": 0.1,
            "max_response_length": 30
        },
        "balanced": {
            "model": "llama3.2:1b",
            "temperature": 0.2,
            "max_response_length": 50
        },
        "powerful": {
            "model": "llama3.2:3b",
            "temperature": 0.1,
            "max_response_length": 100
        }
    },
    "favorite_models": [
        "tinyllama:latest",
        "llama3.2:1b",
        "llama3.2:3b",
        "codellama:latest",
        "mistral:latest"
    ]
}

CONFIG_FILE = 'mimir_config.json'

# === Config Management ===
def load_config():
    """Load configuration from file or create default with TinyLlama fallback"""
    config = DEFAULT_CONFIG.copy()
    
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                user_config = json.load(f)
                # Merge with defaults to handle missing keys
                config.update(user_config)
                # Ensure profiles exist
                if 'profiles' not in config:
                    config['profiles'] = DEFAULT_CONFIG['profiles']
        except Exception as e:
            print(f"⚠️  Error loading config: {e}")
            print("Using default TinyLlama configuration...")
    else:
        # Create default config file
        create_default_config()
    
    # Always use TinyLlama as default unless user explicitly changed it
    if config.get('use_default_model', True):
        config['model'] = DEFAULT_MODEL
        print(f"🦙 Using default model: {DEFAULT_MODEL}")
    else:
        print(f"🤖 Using configured model: {config['model']}")
    
    return config

def save_config(config):
    """Save current configuration to file"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        print(f"⚠️  Could not save config: {e}")
        return False

def create_default_config():
    """Create default configuration file"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
        print(f"📝 Created default config file: {CONFIG_FILE}")
    except Exception as e:
        print(f"⚠️  Could not create config file: {e}")

def get_available_models(config):
    """Fetch available models from Ollama"""
    try:
        response = requests.get(f"{config['ollama_url']}/api/tags", timeout=5)
        response.raise_for_status()
        models = response.json()['models']
        return [model['name'] for model in models]
    except Exception as e:
        print(f"⚠️  Could not fetch available models: {e}")
        return []

def switch_profile(profile_name, config):
    """Switch to a different model profile"""
    if profile_name in config['profiles']:
        profile = config['profiles'][profile_name]
        for key, value in profile.items():
            config[key] = value
        print(f"🔄 Switched to '{profile_name}' profile")
        print(f"   Model: {config['model']}")
        print(f"   Temperature: {config['temperature']}")
        return config
    else:
        print(f"❌ Profile '{profile_name}' not found")
        print(f"Available profiles: {list(config['profiles'].keys())}")
        return config

def set_model(model_name, config):
    """Set the current model and disable default model behavior"""
    available_models = get_available_models(config)
    
    if available_models and model_name not in available_models:
        print(f"⚠️  Model '{model_name}' not found in available models")
        print("Available models:")
        for model in available_models:
            print(f"   - {model}")
        return config
    
    # When user explicitly sets a model, disable default behavior
    config['model'] = model_name
    config['use_default_model'] = False
    print(f"🤖 Set model to: {model_name}")
    print("🔧 Disabled default TinyLlama behavior - will use your chosen model")
    
    # Save the change to config
    if save_config(config):
        print("💾 Configuration saved")
    
    return config

def reset_to_default_model(config):
    """Reset to always use TinyLlama as default"""
    config['model'] = DEFAULT_MODEL
    config['use_default_model'] = True
    print(f"🦙 Reset to default model: {DEFAULT_MODEL}")
    print("🔧 Enabled default behavior - will always use TinyLlama unless overridden")
    
    # Save the change to config
    if save_config(config):
        print("💾 Configuration saved")
    
    return config

def interactive_model_selection(config):
    """Interactive model selection menu"""
    available_models = get_available_models(config)
    
    if not available_models:
        print("❌ No models available. Please check your Ollama installation.")
        return config
    
    print(f"\n🦙 Current behavior: {'Using TinyLlama default' if config.get('use_default_model', True) else 'Using configured model'}")
    print(f"🤖 Current model: {config['model']}")
    print("\n🤖 Available Models:")
    
    # Add option to reset to default
    print("   0. 🦙 Reset to TinyLlama default")
    
    for i, model in enumerate(available_models, 1):
        current = " (current)" if model == config['model'] else ""
        print(f"   {i}. {model}{current}")
    
    try:
        choice = input(f"\nSelect model (0-{len(available_models)}) or press Enter to keep current: ").strip()
        
        if choice == "":
            print(f"🤖 Keeping current setup")
            return config
        
        choice_idx = int(choice)
        
        if choice_idx == 0:
            return reset_to_default_model(config)
        elif 1 <= choice_idx <= len(available_models):
            selected_model = available_models[choice_idx - 1]
            return set_model(selected_model, config)
        else:
            print("❌ Invalid selection")
            return config
            
    except (ValueError, KeyboardInterrupt):
        print("\n❌ Invalid input or cancelled")
        return config

def add_favorite_model(model_name, config):
    """Add a model to favorites"""
    if 'favorite_models' not in config:
        config['favorite_models'] = []
    
    if model_name not in config['favorite_models']:
        config['favorite_models'].append(model_name)
        print(f"⭐ Added '{model_name}' to favorites")
        save_config(config)
    else:
        print(f"⭐ '{model_name}' is already in favorites")
    
    return config

def show_favorites(config):
    """Show favorite models"""
    favorites = config.get('favorite_models', [])
    if not favorites:
        print("⭐ No favorite models set")
        return
    
    print("⭐ Favorite Models:")
    available_models = get_available_models(config)
    
    for i, model in enumerate(favorites, 1):
        status = "✅" if model in available_models else "❌"
        current = " (current)" if model == config['model'] else ""
        print(f"   {i}. {status} {model}{current}")

# === Utility Functions ===
def read_log_matches(query, config):
    log_file = config['log_file']
    if not os.path.exists(log_file): 
        return []
    with open(log_file, 'r') as f:
        matches = [line.strip() for line in f if query.lower() in line.lower()]
        return matches[:config['max_history_search']]

def read_bash_history(query, config):
    bash_history = os.path.expanduser(config['bash_history'])
    if not os.path.exists(bash_history): 
        return []
    with open(bash_history, 'r') as f:
        matches = [line.strip() for line in f if query.lower() in line.lower()]
        return matches[:config['max_history_search']]

def read_man_page_summary(term):
    try:
        result = subprocess.run(['man', term], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=3)
        output = result.stdout.decode()
        # Extract NAME section
        match = re.search(r'(?<=\nNAME\n)(.*?)(?=\n[A-Z])', output, re.S)
        return match.group(1).strip() if match else "No man page summary found."
    except Exception:
        return "No man page found."

def log_interaction(prompt, reply, config):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_file = config['log_file']
    with open(log_file, 'a') as f:
        f.write(f"[{timestamp}] USER: {prompt}\n")
        f.write(f"[{timestamp}] BOT: {reply}\n")
        f.write(f"[{timestamp}] MODEL: {config['model']}\n\n")

def ask_model(prompt, config):
    messages = [
        {
            "role": "system",
            "content": (
                "Reply with ONLY the shell command. Nothing else.\n"
                "Examples:\n"
                "User: show running processes\n"
                "You: ps aux\n\n"
                "User: check disk space\n"  
                "You: df -h\n\n"
                "User: find large files\n"
                "You: find / -size +100M 2>/dev/null\n\n"
                "NO explanations. NO text. ONLY the command."
            )
        },
        {"role": "user", "content": prompt}
    ]
    
    payload = {
        "model": config['model'],
        "messages": messages,
        "stream": config['stream_responses'],
        "options": {
            "temperature": config['temperature']
        }
    }
    
    try:
        response = requests.post(
            f"{config['ollama_url']}/api/chat", 
            json=payload,
            timeout=config['timeout_seconds']
        )
        response.raise_for_status()
        return response.json()['message']['content']
    except requests.exceptions.RequestException as e:
        return f"Error connecting to Ollama: {e}"

# === Main CLI Tool ===
def main():
    parser = argparse.ArgumentParser(description="🧠 Mimir - Terminal Troubleshooting Assistant")
    parser.add_argument('query', nargs='?', help='Your prompt in quotes')
    parser.add_argument('--logs', action='store_true', help='Search previous Mimir logs')
    parser.add_argument('--history', action='store_true', help='Search your Bash history')
    parser.add_argument('--man', action='store_true', help='Search local man pages')
    parser.add_argument('--profile', type=str, help='Switch to model profile (lightweight/balanced/powerful)')
    parser.add_argument('--config', action='store_true', help='Show current configuration')
    parser.add_argument('--models', action='store_true', help='List available Ollama models')
    parser.add_argument('--model', type=str, help='Set the LLM model to use')
    parser.add_argument('--select-model', action='store_true', help='Interactive model selection')
    parser.add_argument('--favorites', action='store_true', help='Show favorite models')
    parser.add_argument('--add-favorite', type=str, help='Add a model to favorites')
    parser.add_argument('--temp', type=float, help='Set temperature (0.0-1.0)')
    parser.add_argument('--reset-default', action='store_true', help='Reset to always use TinyLlama as default')
    
    args = parser.parse_args()
    config = load_config()
    
    # Handle special commands
    if args.config:
        print("🔧 Current Configuration:")
        default_status = "🦙 TinyLlama (default)" if config.get('use_default_model', True) else "🤖 User configured"
        print(f"   Model: {config['model']} ({default_status})")
        print(f"   Temperature: {config['temperature']}")
        print(f"   Ollama URL: {config['ollama_url']}")
        print(f"   Max Response Length: {config['max_response_length']}")
        print(f"   Available Profiles: {list(config['profiles'].keys())}")
        print(f"   Log File: {config['log_file']}")
        print(f"   Use Default Model: {config.get('use_default_model', True)}")
        return
    
    if args.models:
        try:
            response = requests.get(f"{config['ollama_url']}/api/tags")
            models = response.json()['models']
            print("🤖 Available Ollama Models:")
            for model in models:
                current = " (current)" if model['name'] == config['model'] else ""
                print(f"   - {model['name']}{current}")
        except Exception as e:
            print(f"❌ Could not fetch models: {e}")
        return
    
    if args.profile:
        config = switch_profile(args.profile, config)
        return
    
    if args.model:
        config = set_model(args.model, config)
        return
    
    if args.select_model:
        config = interactive_model_selection(config)
        return
    
    if args.favorites:
        show_favorites(config)
        return
    
    if args.add_favorite:
        config = add_favorite_model(args.add_favorite, config)
        return
    
    if args.reset_default:
        config = reset_to_default_model(config)
        return
    
    if args.temp is not None:
        if 0.0 <= args.temp <= 1.0:
            config['temperature'] = args.temp
            print(f"🌡️  Set temperature to: {args.temp}")
            save_config(config)
        else:
            print("❌ Temperature must be between 0.0 and 1.0")
        return
    
    if not args.query:
        parser.print_help()
        return
    
    prompt = args.query.strip()
    print(f"\n🧾 Prompt: {prompt}")
    print(f"🤖 Using: {config['model']} (temp: {config['temperature']})")
    
    if args.logs:
        print("\n🔍 Logs:")
        for line in read_log_matches(prompt, config):
            print("  ", line)
    
    if args.history:
        print("\n📜 Bash History:")
        for line in read_bash_history(prompt, config):
            print("  ", line)
    
    if args.man:
        term = prompt.strip().split()[0]
        print(f"\n📘 Man Page Summary for '{term}':")
        print("  ", read_man_page_summary(term))
    
    if not (args.logs or args.history or args.man):
        reply = ask_model(prompt, config)
        print(f"\n🤖 Mimir Says:\n {reply}")
        log_interaction(prompt, reply, config)

if __name__ == "__main__":
    main()
