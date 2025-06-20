import os
import errno

def get_file_content(working_directory, file_path):
    if not os.path.exists(working_directory):
        return f'Error: Working directory "{working_directory}" does not exist'

    if not os.path.isdir(working_directory):
        return f'Error: Working directory "{working_directory}" is not a directory'

    wd = os.path.abspath(working_directory)

    if file_path is not None:
        if file_path.strip() == "":
            return f'Error: File parameter cannot be empty'

        try:
            rf = os.path.abspath(os.path.join(wd, file_path))
        except (TypeError, ValueError) as e:
            return f'Error: Invalid file parameter "{file_path}": {str(e)}'

        if not rf.startswith(wd):
            return f'Error: Cannot open "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(rf):
            return f'Error: File "{file_path}" does not exist in working directory'

        if not os.path.isfile(rf):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        MAX_CHARS = 10000
        try:
            with open(rf, "r") as f:
                file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) == MAX_CHARS:
                return file_content_string + f'[...File "{rf}" truncated at 10000 characters]'
            else:
                return file_content_string
        except PermissionError:
            return f'Error: Permission denied when accessing file "{file_path}"'
        except OSError as e:
            return f'Error: Cannot access file "{file_path}": {str(e)}'
