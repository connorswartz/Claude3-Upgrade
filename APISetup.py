import os
import requests
import json
import argparse
import re
import subprocess
import time
import sys

# Set your API key
api_key = "API KEY"  # Replace with your actual API key

# Set the API endpoint URL
url = "https://api.anthropic.com/v1/messages"

# Set the model and temperature
model = "claude-3-opus-20240229"
temperature = 0.3
max_tokens = 4000

# Create an argument parser
parser = argparse.ArgumentParser(description="Generate code using Claude 3 API")
parser.add_argument("project_directory", help="Path to the project directory")
parser.add_argument("--files", nargs="+", help="Files to be edited by the API")
parser.add_argument("--directory", help="Directory containing files to be edited by the API")

# Parse the command-line arguments
args = parser.parse_args()

# Set the project directory
project_directory = args.project_directory

# Create the project directory if it doesn't exist
os.makedirs(project_directory, exist_ok=True)

def generate_code(instruction, new_directory_path, file_contents=None, error_message=None):
    # Prepare the request payload
    payload = {
        "messages": [
            {
                "role": "user",
                "content": f"Instruction: {instruction}\n\nProject Directory: {new_directory_path}\n\nPlease generate the necessary files and code to create the program described in the instruction. Create files with appropriate names and extensions for each part of the project (e.g., frontend, backend, database). Organize the files in a suitable directory structure within the '{new_directory_path}' directory. For each file, provide the file name followed by a colon and the code enclosed in triple backticks (```), specifying the language after the opening backticks. Make sure to include the file name and code block on separate lines."
            }
        ],
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    if file_contents:
        payload["messages"].append({
            "role": "assistant",
            "content": "Here are the contents of the files you requested:"
        })
        for file_path, content in file_contents.items():
            payload["messages"].append({
                "role": "user",
                "content": f"File: {file_path}\n\n```\n{content}\n```"
            })
        payload["messages"].append({
            "role": "assistant",
            "content": "Acknowledged. Please provide any necessary updates or modifications to the files based on the instruction."
        })
        payload["messages"].append({
            "role": "user",
            "content": instruction
        })

    if error_message:
        payload["messages"].append({
            "role": "assistant",
            "content": "I understand that an error occurred while creating the files. I will try to provide a solution."
        })
        payload["messages"].append({
            "role": "user",
            "content": f"Error Message: {error_message}\n\nPlease provide a solution to resolve the error."
        })

    # Set the request headers
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01"
    }

    # Send the request to the API
    print("Waiting for API response...", end="", flush=True)
    response = requests.post(url, json=payload, headers=headers)
    print("\rAPI response received. ")

    # Check the response status code
    if response.status_code == 200:
        # Parse the response JSON
        result = response.json()

        # Extract the generated text from the response
        generated_text = result["content"][0]["text"]

        # Extract file names and their corresponding code snippets using regex
        file_pattern = r"File: (.*?)\n```(?:.*?)\n(.*?)\n```"
        files = re.findall(file_pattern, generated_text, re.DOTALL)

        if files:
            # Update the existing files with the new code snippets
            updated_files = []
            for file_path, code in files:
                file_path = file_path.strip()
                if os.path.isfile(file_path):
                    with open(file_path, "w") as file:
                        file.write(code.strip())
                    print(f"Updated file: {file_path}")
                    updated_files.append(file_path)
                else:
                    print(f"File not found: {file_path}")
            return updated_files
        else:
            print("The API response did not contain the expected code changes.")
            print("Saving the API response in a text file for reference.")
            # Create a text file with the generated information
            file_path = os.path.join(new_directory_path, "api_response.txt")
            with open(file_path, "w") as file:
                file.write(generated_text.strip())
            print(f"Created file with API response: {file_path}")
            return None
    else:
        print(f"Request failed with status code: {response.status_code}")
        print("Error details:", response.text)
        return None

def check_files(expected_files):
    for file_path in expected_files:
        if not os.path.exists(file_path):
            return False
    return True

def open_terminal(directory):
    subprocess.Popen(f'open -a Terminal "{directory}"', shell=True)

def read_file_contents(file_paths):
    file_contents = {}
    for file_path in file_paths:
        with open(file_path, "r") as file:
            content = file.read()
            file_contents[file_path] = content
    return file_contents

def convert_files_to_text(file_paths):
    file_contents = {}
    for file_path in file_paths:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                file_contents[file_path] = content
        except UnicodeDecodeError:
            print(f"Skipping file '{file_path}' due to decoding error.")
    return file_contents

def get_files_in_directory(directory):
    file_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)
    return file_paths

def loading_animation():
    chars = "/—\\|"
    while True:
        for char in chars:
            sys.stdout.write("\r" + char)
            sys.stdout.flush()
            time.sleep(0.1)

# Prompt the user for instructions
print("Enter the instruction for generating or editing the code:")
instruction = input()

# Check if files or directory are provided as arguments
if args.files:
    file_paths = [os.path.abspath(file_path) for file_path in args.files]
    file_contents = convert_files_to_text(file_paths)
    created_files = generate_code(instruction, project_directory, file_contents=file_contents)
    if created_files:
        print("Files edited successfully.")
    else:
        print("No files were edited. Please check the API response.")
elif args.directory:
    directory_path = os.path.abspath(args.directory)
    # Create the directory if it doesn't exist
    os.makedirs(directory_path, exist_ok=True)
    file_paths = get_files_in_directory(directory_path)
    file_contents = convert_files_to_text(file_paths)
    created_files = generate_code(instruction, directory_path, file_contents=file_contents)
    if created_files:
        print("Necessary files updated successfully.")
    else:
        print("No files were updated. Please check the API response.")
else:
    while True:
        # Prompt the user for the new directory name
        while True:
            new_directory_name = input("Enter the name for the new directory: ")
            new_directory_path = os.path.join(project_directory, new_directory_name)
            if os.path.exists(new_directory_path):
                print(f"Directory '{new_directory_name}' already exists. Please choose a different name.")
            else:
                break

        # Create the new directory inside the project directory
        os.makedirs(new_directory_path, exist_ok=True)

        # Change the current directory to the new directory
        os.chdir(new_directory_path)

        try:
            created_files = generate_code(instruction, new_directory_path)
            if created_files:
                if check_files(created_files):
                    print("All files created successfully.")
                    # Open a new terminal window in the newly created directory
                    open_terminal(new_directory_path)
                else:
                    error_message = "Some files were not created correctly."
                    print(error_message)
                    while not check_files(created_files):
                        print("Sending error message back to the API for resolution...")
                        file_contents = read_file_contents(created_files)
                        created_files = generate_code(instruction, new_directory_path, file_contents=file_contents, error_message=error_message)
                        if not created_files:
                            break
                    if created_files:
                        print("All files created successfully after resolution.")
                        # Open a new terminal window in the newly created directory
                        open_terminal(new_directory_path)
                    else:
                        print("No files were created. Please check the API response.")
            else:
                print("No files were created. Please check the API response.")

            while True:
                # Wait for user input
                user_input = input("Next Prompt (or type 'STOP' to exit): ")
                if user_input.lower() == "stop":
                    print("Stopping the script...")
                    break

                # Continue the conversation and make edits to the initially created project
                instruction = user_input
                file_contents = read_file_contents(created_files)
                created_files = generate_code(instruction, new_directory_path, file_contents=file_contents)
                if created_files:
                    print("Files updated successfully.")
                else:
                    print("No files were updated. Please check the API response.")

        except Exception as e:
            print("An error occurred:")
            print(str(e))
            break