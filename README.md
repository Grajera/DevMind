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

---

## Example Usage

```bash
python devmind.py "write a boost test for this file" -f main.cpp
