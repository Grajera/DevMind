import sys
import requests
import time
import threading
import itertools
import os
import json

# === CONFIG ===

# Change to match your local model name from `ollama list`
MODEL_NAME = 'custom-model'

# Default Ollama local API endpoint
OLLAMA_URL = 'http://localhost:11434/api/generate'


# === UX Spinner ===
def spinner(text="Thinking..."):
    """Terminal spinner to show activity during long generation."""
    for c in itertools.cycle(["|", "/", "-", "\\"]):
        if not spinner.running:
            break
        sys.stdout.write(f"\r{text} {c}")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write("\r" + " " * 50 + "\r")
spinner.running = True


# === Core API Calls ===
def ask_ollama(prompt):
    """Send prompt to Ollama's local REST API with error handling."""
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                'model': MODEL_NAME,
                'prompt': f"""You are DevMind, a brilliant programming assistant. You specialize in algorithms and writing test code in C++ (Boost Test) and C#. Be clear, optimal, and thorough.\n\n{prompt}""",
                'stream': False
            }
        )
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': f"Ollama API error: {e}"}


def ask_ollama_stream(prompt):
    """Send prompt to Ollama and stream output as it arrives."""
    try:
        with requests.post(
            OLLAMA_URL,
            json={
                'model': MODEL_NAME,
                'prompt': f"""You are DevMind, a brilliant programming assistant. You specialize in algorithms and writing test code in C++ (Boost Test) and C#. Be clear, optimal, and thorough.\n\n{prompt}""",
                'stream': True
            },
            timeout=300,
            stream=True
        ) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    chunk = line.decode('utf-8')
                    if chunk.startswith("data: "):
                        chunk = chunk[6:]
                    try:
                        data = json.loads(chunk)
                        if 'response' in data:
                            print(data['response'], end='', flush=True)
                    except Exception as e:
                        print(f"\n[stream error: {e}]")
    except requests.exceptions.RequestException as e:
        print(f"\nStreaming request failed: {e}")


# === Banner ===
def print_banner():
    """Show DevMind ASCII branding."""
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

    # Debug and output flags
    debug = "--debug" in sys.argv
    stream_mode = "--stream" in sys.argv

    if "-o" in sys.argv:
        out_index = sys.argv.index("-o")
        if out_index + 1 >= len(sys.argv):
            print("Error: Missing output filename after -o")
            sys.exit(1)
        output_file = sys.argv[out_index + 1]
    else:
        output_file = None

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python devmind.py \"<prompt>\"")
        print("  python devmind.py -f <filename>")
        print("  python devmind.py \"<prompt>\" -f <filename>")
        print("Optional flags: --debug  |  --stream  |  -o <output.txt>")
        sys.exit(1)

    if "-f" in sys.argv:
        file_index = sys.argv.index("-f")
        if file_index + 1 >= len(sys.argv):
            print("Error: Missing filename after -f")
            sys.exit(1)
        filepath = sys.argv[file_index + 1]
        if not os.path.exists(filepath):
            print(f"Error: File not found: {filepath}")
            sys.exit(1)

        with open(filepath, 'r') as f:
            file_contents = f.read()

        if file_index > 1:
            custom_prompt = ' '.join(sys.argv[1:file_index])
            prompt = f"{custom_prompt}\n\n{file_contents}"
        else:
            prompt = file_contents
        print(f"Loaded file: {filepath}")
    else:
        prompt = ' '.join(arg for arg in sys.argv[1:] if arg not in ["--debug", "--stream", "-o"])

    print(f"\nFull Prompt:\n{'-'*60}\n{prompt}\n{'-'*60}\n")

    start_time = time.time()

    if stream_mode:
        print("\nStreaming Response:\n")
        ask_ollama_stream(prompt)
        elapsed_time = time.time() - start_time

        word_count = len(prompt.split())
        token_est = int(word_count * 1.5)
        print("\n\nStats:")
        print(f"• Prompt length: {len(prompt)} characters")
        print(f"• Word count: {word_count}")
        print(f"• Estimated tokens: {token_est}")
        print(f"• Time taken: {elapsed_time:.2f} seconds")
    else:
        spinner.running = True
        t = threading.Thread(target=spinner)
        t.start()

        data = ask_ollama(prompt)
        elapsed_time = time.time() - start_time
        spinner.running = False
        t.join()

        print("\nResponse:\n")
        if 'response' in data:
            response = data['response']
            print(response)
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(response)
                print(f"\nResponse saved to {output_file}")
        else:
            print("Error:", data.get('error', 'Unknown'))

        if debug:
            print("\nFull JSON:\n", data)

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
