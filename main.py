import os
from posix import sysconf_names
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
import argparse
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

def call_function(function_call_part, verbose=False)->types.Content:
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    function_dict = {
        'get_files_info': get_files_info,
        'get_file_content': get_file_content,
        'write_file': write_file,
        'run_python_file': run_python_file,
    }
    args_dict = {}
    args_dict.update(function_call_part.args)
    args_dict.update({'working_directory': './calculator'})
    if function_call_part.name not in function_dict:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    result = function_dict[function_call_part.name](**args_dict)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": result},
            )
        ],
    )

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    parser = argparse.ArgumentParser(description="Gemini API")
    parser.add_argument("prompt", help="Prompt")
    parser.add_argument("--model", default="gemini-2.0-flash-001", help="Model name")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()
    if args.prompt is None:
            print("Usage: python main.py <prompt>")
            sys.exit(1)
    messages = [
        types.Content(role="user", parts=[types.Part(text=args.prompt)]),
    ]
    schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )
    schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Gets the content of a specified file, restricted to the working directory and will not return more than 10,000 chars",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file to get the content of, relative to the working directory. If not provided, will return an error."
                )
            }
        )
    )
    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Writes the content to a specified file, restricted to the working directory",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file to write the content to, relative to the working directory. If not provided, will return an error."
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The content to write to the file. If not provided, will return an error."
                )
            }
        )
    )
    schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Runs a Python script",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The Python script to run"
                )
            }
        )
    )
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file
        ]
    )
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    loopCount = 0
    response = None
    token_usage = None
    while loopCount < 20:
        response = client.models.generate_content(
            model=args.model,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            )
        )
        loopCount += 1
        if response.candidates:
            for candidate in response.candidates:
                if candidate.content:
                    messages.append(candidate.content)
        token_usage = response.usage_metadata
        if response.function_calls:
            for func in response.function_calls:
                func_response = call_function(func)
                if func_response:
                    messages.append(func_response)
                    if func_response.parts:
                        if func_response.parts[0].function_response:
                            if func_response.parts[0].function_response.response:
                                if args.verbose:
                                    print(f"-> {func_response.parts[0].function_response.response['result']}")
                            else:
                                raise ValueError(f"Function call failed: {func.name}")
        if response.candidates and not response.function_calls:
            break
    if response:
        print(response.text)
    if args.verbose:
        print(f"User prompt: {args.prompt}")
        if token_usage:
            print(f"Prompt tokens: {token_usage.prompt_token_count}")
            print(f"Response tokens: {token_usage.candidates_token_count}")



if __name__ == "__main__":
    main()
