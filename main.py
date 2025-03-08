# Task 3) AI Codebase Digestion

# Description:
# Given an arbitrary python codebase, use a system of LLMs to create
# docstrings & in line comments for files, and README’s for folders.

# Hints / Things to keep in mind:
#  Does an AI need info outside of the immediate thing being digested (e.g. if
# analyzing file1.py do you need any code from file2.py?). How can you (or an
# AI) determine if external info is needed ?
#  When analyzing a file, do you need to look at the whole file? How can you
# (or an AI) determine which chunks to look at
# Are there any extra reasoning steps involved? Are any of the hints in Task 1
# applicable here ?

# Frameworks: Langchain
import os
import ast
import anthropic
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSequence
import openai
from langchain_core.prompts import PromptTemplate
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSequence
from langchain_openai import ChatOpenAI


# Load API key

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY
# If run out of credits, comment out this line and uncomment the next line
llm = ChatOpenAI(model="gpt-4", temperature=0)

# llm = ChatAnthropic(
#     model="claude-3-haiku-20240307",
#     anthropic_api_key=ANTHROPIC_API
# )

# File Analyzer Agent
def extract_code_info(file_path):
    """Extracts function names, docstrings, and class names from a Python file."""
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=file_path)

    functions = []
    classes = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append((node.name, ast.get_docstring(node)))
        elif isinstance(node, ast.ClassDef):
            classes.append((node.name, ast.get_docstring(node)))

    return {
        "file": file_path,
        "functions": functions,
        "classes": classes
    }

def analyze_codebase(directory):
    """Analyzes all Python files in a directory."""
    analysis = []
    for file in os.listdir(directory):
        if file.endswith(".py"):
            analysis.append(extract_code_info(os.path.join(directory, file)))
    return analysis

# Code Summarizer Agent
summary_prompt = PromptTemplate(
    input_variables=["file", "functions", "classes"],
    template="""
    You are analyzing a Python file: {file}. 

    Functions:
    {functions}

    Classes:
    {classes}

    Based on this information, generate a concise README description for this script.
    """
)

summary_chain = summary_prompt | llm  

def generate_summaries(analysis):
    summaries = {}
    for file_data in analysis:
        summaries[file_data["file"]] = summary_chain.invoke({
            "file": file_data["file"],
            "functions": "\n".join([f"{name}: {doc}" for name, doc in file_data["functions"]]),
            "classes": "\n".join([f"{name}: {doc}" for name, doc in file_data["classes"]])
        })
    return summaries

# README Updater Agent
readme_prompt = PromptTemplate(
    input_variables=["summaries"],
    template="""
    You are an AI assistant that generates a README for a Python repository.

    Here are the descriptions of each script:
    {summaries}

    Format this information into a structured and well-written README.
    """
)

readme_chain = readme_prompt | llm 

def generate_readme(summaries):
    summaries_text = "\n".join([f"### {file}:\n{desc}" for file, desc in summaries.items()])
    return readme_chain.invoke({"summaries": summaries_text})


if __name__ == "__main__":
    # Analyze Python files
    codebase_path = os.path.join(os.getcwd(), "codebase")
    code_analysis = analyze_codebase(codebase_path)

    # Generate script summaries
    summaries = generate_summaries(code_analysis)

    # Generate an improved README
    updated_readme = generate_readme(summaries)

    # Save the new README.md
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated_readme)

    print("README.md updated successfully!")


