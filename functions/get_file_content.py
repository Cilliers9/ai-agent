import os
from config import GET_FILE_CHARACTER_LIMIT
from google import genai
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file at specified file path relative to the working directory, content is return as a string of maximum length 10000 characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to file to read content, relative to the working directory",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_path = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not valid_target_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" is not a file'
        string_result = ""
        with open(target_file, mode="r") as file:
            string_result = file.read(GET_FILE_CHARACTER_LIMIT)
            if file.read(1):
                string_result += f'[...File "{file_path}" truncated at {GET_FILE_CHARACTER_LIMIT} characters]'

        return string_result
    except Exception as e:
        return f"Error: {e}"