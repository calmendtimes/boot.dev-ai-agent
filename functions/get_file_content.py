import os
import io
from google.genai import types

MAX_CHARS = 10000


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns file content for the specified file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required = ["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file path relative to the working directory",
            ),
        },
    ),
)


def get_file_content(working_directory, file_path):
    result = f"Result for {file_path} file read:" + os.linesep
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        
        if not valid_target_file:
            return result + f'Error: Cannot read "{file_path}" as it is outside the permitted working directory' + os.linesep
        if not os.path.isfile(target_file):
            return result + f'Error: File not found or is not a regular file: "{file_path}"' + os.linesep

        content = ""
        with open(target_file, "r") as f:
            content += f.read(MAX_CHARS) + os.linesep
            if f.read(1): 
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]' + os.linesep
        
        return result + content

    except Exception as e:
        return result + f"Error: {e}" + os.linesep



