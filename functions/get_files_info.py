import os
from google.genai import types



schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def get_files_info(working_directory, directory="."):
    dirstr = "current" if directory == "." else f"'{directory}'"
    result = f"Result for {dirstr} directory:" + os.linesep
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        
        if not valid_target_dir:
            return result + f'Error: Cannot list "{directory}" as it is outside the permitted working directory' + os.linesep
        if not os.path.isdir(target_dir):
            return result + f'Error: "{directory}" is not a directory' + os.linesep

        lsdir = []
        for e in os.listdir(target_dir):
            e_path = os.path.join(target_dir, e)
            lsdir.append(f"  - {e}: file_size={os.path.getsize(e_path)} bytes, is_dir={os.path.isdir(e_path)}")
       
        return result + os.linesep.join(sorted(lsdir)) + os.linesep

    except Exception as e:
        return result + f"Error: {e}" + os.linesep