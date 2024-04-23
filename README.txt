This Python script utilizes the Anthropic Claude-3 API to generate code based on user instructions. It provides a convenient way to create and edit code projects using natural language instructions.

## Prerequisites

Before using this script, make sure you have the following:

- Python 3.x installed on your system
- An API key for the Anthropic Claude-3 API
- Required Python packages: `requests`, `argparse`, `re`, `subprocess`

## Installation

1. Clone the repository or download the script file.
2. Install the required Python packages by running the following command:
   pip install requests argparse

## Usage

The script can be run from the command line with various options and arguments. Here are the available commands and their usage:
### Generate Code for a New Project
To generate code for a new project, use the following command:

python script.py <project_directory>

- `<project_directory>`: The path to the directory where the new project will be created.

The script will prompt you to enter an instruction describing the desired code project. It will then send the instruction to the Anthropic Claude-3 API, which will generate the necessary code files and directory structure based on the instruction.

Example:
python script.py /path/to/project/directory

### Edit Existing Code Files

To edit existing code files using the API, use the following command:

python script.py <project_directory> --files <file1> <file2> ...

- `<project_directory>`: The path to the directory where the project is located.
- `--files`: Flag indicating that specific files should be edited.
- `<file1> <file2> ...`: The paths to the code files to be edited.

The script will prompt you to enter an instruction describing the desired changes to the code files. It will then send the instruction and the contents of the specified files to the API for editing.

Example:
python script.py /path/to/project/directory --files /path/to/file1.py /path/to/file2.py

### Edit Code Files in a Directory

To edit code files in a directory using the API, use the following command:

python script.py <project_directory> --directory <directory_path>

- `<project_directory>`: The path to the directory where the project is located.
- `--directory`: Flag indicating that multiple files in a directory should be edited.
- `<directory_path>`: The path to the directory containing the code files to be edited.

The script will prompt you to enter an instruction describing the desired changes to the code files. It will then send the instruction and the contents of all code files in the specified directory to the API for editing.

Example:
python script.py /path/to/project/directory --directory /path/to/code/directory

## Workflow

1. Run the script with the appropriate command and arguments.
2. Enter the instruction when prompted, describing the desired code project or changes to existing code files.
3. The script will send the instruction and any necessary file contents to the Anthropic Claude-3 API.
4. The API will generate or edit the code files based on the provided instruction.
5. The script will create or update the code files in the specified project directory.
6. If the API response does not contain the expected code and file structure, the script will save the API response in a text file named `api_response.txt` for reference.
7. The script will provide feedback on the success or failure of the code generation or editing process.

## Troubleshooting

- If the script fails to create or edit the code files as expected, check the `api_response.txt` file for the raw API response to investigate any issues.
- Ensure that you have a valid API key and that the API endpoint URL is correct.
- Make sure you have the necessary permissions to create and modify files in the specified project directory.
- If you encounter any errors or exceptions, refer to the error messages displayed in the console for more information.

## Disclaimer

This script relies on the Anthropic Claude-3 API for code generation and editing. The quality and accuracy of the generated code depend on the performance and capabilities of the API. Always review and test the generated code before using it in production environments.
