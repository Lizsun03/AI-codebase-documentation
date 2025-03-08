# AI Python Automated Codebase Analyzer and Documentation Generator

This project provides an automated solution for analyzing a Python codebase and generating structured README documentation based on the file content. The solution extracts key information such as function names, docstrings, and class definitions from Python scripts, then summarizes and formats this information into a user-friendly README.

## Features

- Analyze all Python files in a directory.
- Extract function names and docstrings.
- Extract class names and docstrings.
- Generate concise README descriptions for each script.
- Combine all individual script descriptions into a single README file.
  
## Tech Stack

- **Python**: The main programming language for this solution.
- **LangChain**: Used for processing and generating summaries using external language models.
- **OpenAI API / Anthropic API / HuggingFace Models**: Used to generate code summaries and recommendations.
- **AST (Abstract Syntax Tree)**: Built-in Python library used for parsing and analyzing Python scripts.

## Installation

Follow these steps to get the project up and running locally:

### 1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Add your API keys:

If you are using Anthropic, set the ANTHROPIC_API variable in your main.py to your own API key.

### 5. Run the application:
```bash
python main.py
```

The program will process the Python files in the codebase folder, generate summaries and docstrings for each file, and update the README.md file with the results

## Author
Elizabeth Sun - https://github.com/Lizsun03


