import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    print("Hello from ai-agent!")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None: raise RuntimeError("apie_key not found.")
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    response = client.models.generate_content(model='gemini-2.5-flash', contents=args.user_prompt)
    if response.usage_metadata is None:
        raise RuntimeError("No usage_metadata in response, assuming response is invalid", response)

    print_response(args.user_prompt, response, args.verbose)


def print_response(prompt, response, verbose=False):
    if verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count }")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count }")
    print("Response:")
    print(response.text)




if __name__ == "__main__":
    main()
