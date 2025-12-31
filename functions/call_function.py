from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file

available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file],
)
'''
schema_call_function = types.FunctionDeclaration(
    name="call_function",
    description="Function call function to call functions",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["function_call"],
        properties={
            "function_call": types.Schema(
                type=types.Type.OBJECT,
                description="Function call containing the function name and arguments",
                properties={
                    "name" : types.Schema(
                        type=types.Type.STRING,
                        description="Name of the function being called"
                    ),
                    "arg" : types.Schema(
                        type=types.Type.OBJECT,
                        description="Arguments of the function being called"
                    ),
                },
            ),
        },
    ),
)
'''
function_map = {
    "get_file_content" : get_file_content,
    "get_files_info" : get_files_info,
    "write_file" : write_file,
    "run_python_file" : run_python_file
}

def function_print(function_call, verbose):
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

def setup_arguments(function_call):
    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = "./calculator"
    return args


def call_function(function_call, verbose=False):
    function_print(function_call, verbose)
    function_name = function_call.name or ""
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    args = setup_arguments(function_call)
    function_result = function_map[function_name](**args)  
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )