import os
from posix import sysconf_names
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
import argparse

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
    response = client.models.generate_content(model=args.model, contents=messages)
    token_usage = response.usage_metadata
    print(response.text)
    if args.verbose:
        print(f"User prompt: {args.prompt}")
        if token_usage:
            print(f"Prompt tokens: {token_usage.prompt_token_count}")
            print(f"Response tokens: {token_usage.candidates_token_count}")



if __name__ == "__main__":
    main()
