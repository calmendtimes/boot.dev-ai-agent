import os
import argparse
import prompts
import functions.call_function
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
    MAX_ITER = 20
    for i in range(MAX_ITER):
        try:
            final_response = generate_content(client, messages, args.verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break
            elif i == MAX_ITER-1:
                print(f"Maximum iterations ({MAX_ITERS}) reached.")
                sys.exit(1)
                
        except Exception as e:
            print(f"Error in generate_content: {e}")


    #print_response(args.user_prompt, response, args.verbose)


def generate_content(client, messages, verbose):
    config=types.GenerateContentConfig(
        tools=[functions.call_function.available_functions], 
        system_instruction=prompts.system_prompt)

    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
        config=config)
            
    if response.usage_metadata is None:
        raise RuntimeError("No usage_metadata in response, assuming response is invalid", response)
    
    if response.candidates:
        for c in response.candidates:
            if c.content:
                messages.append(c.content)

    if not response.function_calls:
        return response.text   

    function_call_results = []
    print("Function calls:")
    for f in response.function_calls:
        result = call_function(f, verbose)
        if  not result.parts \
            or not result.parts[0].function_response \
            or not result.parts[0].function_response.response :
            raise RuntimeError(f"Empty function response for {function_call.name}")
        
        if verbose:
            print(f"-> {result.parts[0].function_response.response}")
        
        function_call_results.append(result.parts[0])

    messages.append(types.Content(role="user", parts=function_call_results))


def print_response(prompt, response, verbose=False):
    if verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count }")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count }")
    print("Response:")
    print(response.text)


def call_function(function_call, verbose=False):
    args_str = f"({function_call.args})" if verbose else ""
    print(f"  Calling function: {function_call.name}{args_str}")
    working_directory = "./calculator"
    
    if function_call.name in functions.call_function.functions:
        function_result = functions.call_function.functions[function_call.name](working_directory, **function_call.args)

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call.name,
                    response={"result": function_result},
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[ 
                types.Part.from_function_response(
                    name=function_call.name, 
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    

    


if __name__ == "__main__":
    main()
