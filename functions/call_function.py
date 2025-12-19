from google.genai import types
import functions.get_files_info as get_files_info 
import functions.get_file_content as get_file_content
import functions.write_file as write_file
import functions.run_python_file as run_python_file


functions = {
    "get_files_info"   : get_files_info.get_files_info, 
    "get_file_content" : get_file_content.get_file_content,
    "write_file"       : write_file.write_file,
    "run_python_file"  : run_python_file.run_python_file,
}

available_functions = types.Tool(
    function_declarations=[
        get_files_info.schema_get_files_info, 
        get_file_content.schema_get_file_content,
        write_file.schema_write_file,
        run_python_file.schema_run_python_file,
    ],
)