import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import config
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

def client_generate_content():
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=config,
        )
    if response.usage_metadata == None:
        raise RuntimeError("Usage metadata empty")
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    return response

def response_function_call(function_calls):
    if function_calls:
        function_responses = []
        
        for function_call in function_calls:
            function_call_result = call_function(function_call, args.verbose)
            if function_call_result.parts[0].function_response == None:
                raise Exception("Function response is none")
            if function_call_result.parts[0].function_response.response == None:
                raise Exception("Function response.reponse is none")
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            function_responses.append(function_call_result.parts[0])
        
        messages.append(types.Content(role="user", parts=function_responses))

def canidate_response(candidates):
    if len(candidates):
        for candidate in candidates:
            messages.append(candidate.content)

def main():
    if api_key == None:
        raise RuntimeError("API Key empty")

    for i in range(20):
        response = client_generate_content()
        canidate_response(response.candidates)
        if not response.function_calls:
            if response.text:
                print(response.text)
                return
        response_function_call(response.function_calls)

    print("Maximum iterations reached without a final response")
    return 1



if __name__ == "__main__":
    main()
