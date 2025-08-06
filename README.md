# DevMind – Offline AI Assistant for C++ Unit Test Generation

**DevMind** is a lightweight offline tool that uses a locally hosted language model (via [Ollama](https://ollama.com/)) to generate C++ unit tests with Boost.Test. It runs fully offline using a simple Python CLI and works with **any code-capable model available in Ollama**, such as LLaMA 3, DeepSeek-Coder, or CodeGemma.

---

## Objective

Automatically generate structured, documentation-quality unit tests from natural language prompts and `.cpp` files. Designed for secure, offline, or air-gapped environments.

---

## Features

- **Fully Offline** – No internet or cloud required  
- **Model-Agnostic** – Works with any compatible Ollama model  
- **Python CLI** – Cross-platform and easy to use  
- **Boost.Test Output** – Generates test suites with edge cases and inline docs  
- **Stats Displayed** – See token estimates and response timing  
- **Automation-Friendly** – Modular design for scripting or pipelines  
- **Streaming Support** – See output live with `--stream`  
- **Debug Mode** – Show raw JSON response with `--debug`  
- **Output Saving** – Save output to a file with `-o output.txt`

---

## CLI Flags Reference

| Flag / Option          | Description                                                               |
|------------------------|---------------------------------------------------------------------------|
| `"<prompt>"`           | Natural language prompt (required)                                         |
| `-f <filename.cpp>`    | Appends the contents of a source file to the prompt                      |
| `--stream`             | Enables real-time streaming response from the model                      |
| `--debug`              | Prints the full raw JSON response (useful for inspection or debugging)   |
| `-o <output.txt>`      | Saves the model output to the specified file                             |

### Notes
- Flags may appear in any order.
- Quoted prompt is required unless you're only using `-f <file>`.
- You can combine flags: `--stream`, `--debug`, and `-o` all work together.

---

## Example Usage

### Basic Prompt Only
```bash
python devmind.py "Write a Boost test for a function that reverses a string"
```

### Prompt + Source File
```bash
python devmind.py "Write a Boost test for this file" -f main.cpp
```

### Streaming Response (faster feedback)
```bash
python devmind.py "Write a Boost test for this file" -f main.cpp --stream
```

### Save Output to File
```bash
python devmind.py "Write a Boost test for this file" -f main.cpp -o test_output.txt
```

### Debug Mode
```bash
python devmind.py "Explain this code" -f example.cpp --debug
```

### Combine Everything
```bash
python devmind.py "Test this algorithm in Boost" -f sort.cpp --stream -o sort_tests.txt --debug
```


---

## Sample Output

![loading-opt](https://github.com/user-attachments/assets/b6d57e01-9d29-4838-aa4f-06a8bcc7fb28)

At the end of each run, DevMind displays useful stats:
```
 Stats:
• Prompt length: 1,120 characters
• Word count: 150
• Estimated tokens: 225
• Response length: 5,300 characters
• Time taken: 45.12 seconds
```

---

## Model Tip

You can use DevMind with any local Ollama model that supports code generation (e.g., `llama3`, `deepseek-coder`, `codegemma`). Simply update the `MODEL_NAME` variable inside the script to match the model you want to use:
```python
MODEL_NAME = "deepseek-coder"
```

