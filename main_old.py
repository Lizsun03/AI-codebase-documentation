import os
import openai
from langchain_core.prompts import PromptTemplate
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSequence
from langchain_openai import ChatOpenAI


# Get all python files in a directory
def get_python_files(directory):
    python_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize LLM
openai.api_key = OPENAI_API_KEY
llm = ChatOpenAI(model="gpt-4", temperature=0)

def generate_docstring(code: str) -> str:
    prompt = f"Add docstrings below any method or function declarations if there are any present for the following Python code:\n\n{code}. Please do not remove any existing code. If you do not find any functions, just return the code."
    response = llm.invoke(prompt)
    return response.content

def generate_comment(code: str) -> str:
    prompt = f"Add in-line comments for the following Python code:\n\n{code}. Please do not remove any existing code."
    response = llm.invoke(prompt)
    return response.content

def generate_readme(directory: str) -> str:
    # Get all python files in a directory
    python_files = get_python_files(directory)
    prompt_text = "\n".join([f"- {file}" for file in python_files])

    prompt_template = "Generate a README for the following files:\n\n{files}"
    prompt = prompt_template.format(files=prompt_text)

    response = llm.invoke(prompt)
    readme_content = response.content

    readme_path = os.path.join(directory, "README.md")
    with open(readme_path, "w") as f:
        f.write(readme_content)

    return readme_content


def process_codebase(directory):
    """Processes an entire codebase, adding docstrings, inline comments, and READMEs."""
    python_files = get_python_files(directory)
    print(f"Processing {len(python_files)} python files...")
    for file in python_files:
        with open(file, "r") as f:
            code = f.read()

        # Generate docstrings and comments
        commented_code = generate_comment(code)
        docstring_code = generate_docstring(commented_code)

        # Overwrite file with new documentation
        with open(file, "w") as f:
            f.write(commented_code)

    # Generate README for each folder
    for root, dirs, files in os.walk(directory):
        readme_content = generate_readme(root)
    print("Codebase processing complete. README.md generated.")


if __name__ == "__main__":
    codebase_path = os.path.join(os.getcwd(), "codebase")
    process_codebase(codebase_path)