import os
import subprocess
from google.genai import types


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file relative to the working directory with optional command-line arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Python file path relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Command-line arguments passed to the Python file.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
    ),
)


def run_python_file(working_directory, file_path, args=None):
    result = f"Result for {file_path} file execution:" + os.linesep
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        
        if not valid_target_file:
            return result + f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory' + os.linesep
        if not os.path.isfile(target_file):
            return result + f'Error: "{file_path}" does not exist or is not a regular file' + os.linesep
        if file_path[-3:] != ".py":
            return result + f'Error: "{file_path}" is not a Python file' + os.linesep
        
        command = ["python3", target_file]
        if args is not None: 
            command.extend(args)
        process = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)        

        if process.returncode != 0:
            return result + f"Error: Process exited with code {process.returncode}." + os.linesep
        if not process.stdout and not process.stderr:
            return result + "No output produced" + os.linesep
        if process.stdout:
            result += f"STDOUT: {process.stdout}" + os.linesep        
        if process.stderr:
            result += f"STDERR: {process.stderr}" + os.linesep
        return result

    except Exception as e:
        return result + f"    Error: executing Python file: {e}" + os.linesep