import os
import subprocess
from google import genai
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute Python file with optional arguments at specified file path relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to python file to execute, relative to the working directory",
            ),
            "arg": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional arguments to send when running file, defaults to None if not send",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_path = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not valid_target_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if target_file[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_file]
        if args != None:
            command.extend(args)
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        output_string = ""
        if result.returncode:
            output_string = (F"Process exited with code {result.returncode}")
        if result.stdout:
            output_string += (f"STDOUT:{result.stdout}")
        else:
            output_string += ("STDOUT: No output produced")
        if result.stderr:
            output_string += (f"STDERR:{result.stderr}")
        else:
            output_string += ("STDERR: No output produced")

        return output_string

    except Exception as e:
        return f"Error: {e}"