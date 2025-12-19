import os
from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="writes content to the specified file path relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required = ["file_path", "content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file_path relative to the working directory to write content to.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="content to write to file specified by file_path relative to working directory.",
            ),
        },
    ),
)


def write_file(working_directory, file_path, content):
    result = f"Result for {file_path} file write:" + os.linesep
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if not valid_target_file:
            return result + f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory' + os.linesep
        if os.path.isdir(target_file):
            return result + f'Error: Cannot write to "{file_path}" as it is a directory' + os.linesep

        target_dir = os.path.dirname(target_file)
        os.makedirs(target_dir, exist_ok=True)

        with open(target_file, "w") as f:
            f.write(content)

        return result + f'Successfully wrote to "{file_path}" ({len(content)} characters written)' + os.linesep

    except Exception as e:
        return result + f"Error: {e}" + os.linesep