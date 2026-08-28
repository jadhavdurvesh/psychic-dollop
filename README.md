# Multi-Agent Coding System

## Introduction
Welcome to the **Multi-Agent Coding System**, a framework that orchestrates multiple specialized agents to collaboratively solve coding tasks. By leveraging the strengths of each agent—ranging from code generation and debugging to documentation and testing—the system provides a seamless, end‑to‑end development experience.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Philosophy](#philosophy)
- [Authors](#authors)

## Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/multi-agent-coding-system.git
cd multi-agent-coding-system

# Install required dependencies
pip install -r requirements.txt
```

> **Note:** The project requires Python 3.9 or newer.

## Usage
Run the main entry point to start the orchestrator:

```bash
python -m src.main
```

You can also invoke individual agents directly for debugging or custom workflows:

```bash
python -m agents.codegen <input_prompt>
python -m agents.debugger <source_file>
```

Configuration options are stored in `config.yaml`. Adjust the model parameters, logging level, and agent routing as needed.

## Examples
### Simple Function Generation
```bash
python -m agents.codegen "Write a Python function that returns the nth Fibonacci number."
```
The system will generate the function, run a quick sanity test, and output the final code.

### Automated Refactoring
```bash
python -m agents.refactor my_script.py
```
The refactor agent analyzes `my_script.py`, applies style improvements, and writes the updated file back to disk.

## Philosophy
The core philosophy of this project is **collaborative intelligence**—treating each specialized agent as a team member that contributes its expertise toward a shared goal. By decomposing complex problems into smaller, manageable tasks, the system achieves higher reliability, better code quality, and faster iteration cycles. This modular design also encourages extensibility: new agents can be added without disrupting existing workflows.

## Authors
Durvesh M. Jadhav