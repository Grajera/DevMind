import sys
import requests
import time
import threading
import itertools
import os

# === CONFIG ===
# Change to match your local model name from `ollama list`
MODEL_NAME = 'custom-llama-m'

# Default Ollama local API endpoint
OLLAMA_URL = 'http://localhost:11434/api/generate'

# === UX Spinner ===
def spinner(text="Thinking..."):
    for c in itertools.cycle(["|", "/", "-", "\\"]):
        if not spinner.running:
            break
        sys.stdout.write(f"\r{text} {c}")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write("\r" + " " * 50 + "\r")
spinner.running = True

# === Core API Call ===
def ask_ollama(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            'model': MODEL_NAME,
            'prompt': f"""You are DevMind, a brilliant programming assistant. You specialize in algorithms and writing test code in C++ (Boost Test) and C#. Be clear, optimal, and thorough.\n\n{prompt}""",
            'stream': False
        }
    )
    return response.json()

# === Banner ===
def print_banner():
    print(r"""
    ____            __  ____           __            _____ ____  __         
   / __ \___ _   __/  |/  (_)___  ____/ /           / ___// __ \/ /         
  / / / / _ \ | / / /|_/ / / __ \/ __  /  ______    \__ \/ / / / /          
 / /_/ /  __/ |/ / /  / / / / / / /_/ /  /_____/   ___/ / /_/ / /___        
/_____/\___/|___/_/  /_/_/_/ /_/\__,_/            /____/_____/_____/        
    __  ____      __               __   ______             _                
   /  |/  (_)____/ /_  ____ ____  / /  / ____/________ _  (_)__  _________ _
  / /|_/ / / ___/ __ \/ __ `/ _ \/ /  / / __/ ___/ __ `/ / / _ \/ ___/ __ `/
 / /  / / / /__/ / / / /_/ /  __/ /  / /_/ / /  / /_/ / / /  __/ /  / /_/ / 
/_/  /_/_/\___/_/ /_/\__,_/\___/_/   \____/_/   \__,_/_/ /\___/_/   \__,_/  
                                                    /___/                   
DevMind - Offline AI Programmer Assistant by Michael Grajera
    """)

# === Entry Point ===
def main():
    print_banner()

    # No prompt or file provided
    if len(sys.argv) < 2:
        print("Usage:\n  python devmind.py \"<prompt>\"\n  python devmind.py -f <filename>\n  python devmind.py \"<prompt>\" -f <filename>")
        return
    
    # Load from file if -f is provided
    if "-f" in sys.argv:
        file_index = sys.argv.index("-f")
        if file_index + 1 >= len(sys.argv):
            print("Error: Missing filename after -f")
            return
        filepath = sys.argv[file_index + 1]
        if not os.path.exists(filepath):
            print(f"Error: File not found: {filepath}")
            return
        with open(filepath, 'r') as f:
            file_contents = f.read()

        if file_index > 1:
            # Prompt AND file
            custom_prompt = ' '.join(sys.argv[1:file_index]) 
            prompt = f"{custom_prompt}\n\n{file_contents}"
        else:
            # Only file
            prompt = file_contents
        print(f"Loaded file: {filepath}")
    else:
        # Just a raw prompt
        prompt = ' '.join(sys.argv[1:])

    print(f"\n FULL Prompt:\n{prompt}\n")

    # Start spinner thread
    spinner.running = True
    t = threading.Thread(target=spinner)
    t.start()

    start_time = time.time()
    data = ask_ollama(prompt)
    elapsed_time = time.time() - start_time
    spinner.running = False
    t.join()

    print("\nResponse:\n")
    if 'response' in data:
        response = data['response']
        print(response)
    else:
        print("Error:", data.get('error', 'Unknown'))

    # Stats
    word_count = len(prompt.split())
    token_est = int(word_count * 1.5)
    print("\nStats:")
    print(f"• Prompt length: {len(prompt)} characters")
    print(f"• Word count: {word_count}")
    print(f"• Estimated tokens: {token_est}")
    print(f"• Response length: {len(data.get('response', ''))} characters")
    print(f"• Time taken: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()
