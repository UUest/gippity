# Gippity - AI Coding Agent

Gippity is a Python-based AI coding agent that leverages Google's Gemini AI to provide an interactive coding assistant with file system capabilities. It allows you to interact with your code using natural language prompts while the AI can read, write, and execute files within a secure working directory.

## Features

- **File System Integration**: Read, write, and list files within a specified working directory
- **Code Execution**: Run Python scripts and see their output
- **Natural Language Interface**: Interact with your codebase using plain English
- **Security-First Design**: All operations are constrained to a working directory for safety
- **Function Calling**: Uses Google Gemini's function calling capabilities for structured interactions

## Prerequisites

- Python 3.7 or higher
- Google Gemini API key

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd gippity
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your Google Gemini API key:
   - Create a `.env` file in the project root
   - Add your API key: `GEMINI_API_KEY=your_api_key_here`

## Usage

Run Gippity with a natural language prompt:

```bash
python main.py "Your prompt here"
```

### Command Line Options

- `--model`: Specify the Gemini model to use (default: `gemini-2.0-flash-001`)
- `--verbose`: Enable verbose output to see detailed function calls and responses

### Examples

```bash
# Basic usage
python main.py "List all files in the current directory"

# With specific model
python main.py "Create a simple calculator script" --model gemini-pro

# With verbose output
python main.py "Read the main.py file and explain what it does" --verbose
```

## Available Functions

The AI agent has access to the following functions:

### `get_files_info`
Lists files and directories with their sizes, constrained to the working directory.

### `get_file_content`
Reads the content of a specified file (limited to 10,000 characters for safety).

### `write_file`
Creates or overwrites files with specified content.

### `run_python_file`
Executes Python scripts and returns their output.

## Working Directory

By default, all file operations are performed within the `./calculator` directory. This security constraint ensures that the AI agent cannot access files outside of the designated workspace.

## Project Structure

```
gippity/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── functions/             # Function implementations
│   ├── get_files_info.py  # Directory listing functionality
│   ├── get_file_content.py # File reading functionality
│   ├── write_file.py      # File writing functionality
│   └── run_python_file.py # Python execution functionality
├── calculator/            # Default working directory
└── tests.py              # Test files
```

## Configuration

Create a `.env` file in the project root with the following variables:

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

## Safety and Security

- All file operations are restricted to the working directory
- File content reading is limited to 10,000 characters
- The system includes error handling for permission issues and invalid paths
- Function calls are limited to prevent infinite loops (max 20 iterations)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Troubleshooting

### Common Issues

1. **API Key Error**: Ensure your `GEMINI_API_KEY` is set correctly in the `.env` file
2. **Permission Denied**: Check that the working directory has proper read/write permissions
3. **Module Not Found**: Ensure all dependencies are installed with `pip install -r requirements.txt`

### Getting Help

If you encounter issues or have questions:
1. Check the verbose output using the `--verbose` flag
2. Review the error messages for specific guidance
3. Ensure your working directory and file paths are correct

## Acknowledgments

- Built with [Google Gemini AI](https://ai.google.dev/)
- Uses the `google-genai` Python SDK
- Environment management with `python-dotenv`
