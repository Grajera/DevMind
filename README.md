# DevMind – Offline AI Assistant for C++ Unit Test Generation

**DevMind** is a lightweight offline tool that uses a locally hosted LLaMA 3.3 70B language model to generate C++ unit tests with Boost.Test. It runs entirely offline using [Ollama](https://ollama.com/) and a simple Python CLI.

---

## Objective

Automatically generate structured, documentation-quality unit tests from natural language prompts and `.cpp` files. Designed for secure, offline, or air-gapped environments.

---

## Features

- **Fully Offline** – No internet or cloud required  
- **Python CLI** – Cross-platform and easy to use  
- **LLM-Powered** – Uses LLaMA 3.3 70B (quantized `.gguf`)  
- **Generates Boost.Test suites** with edge cases and inline docs  
- **Token/Time Stats** printed after generation  
- **Easy Scripting** – Modular design for automation  

---

## Example Usage

```powershell
python devmind.py "write a boost test for this file" -f main.cpp
