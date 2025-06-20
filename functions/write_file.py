import os
import errno

def write_file(working_directory, file_path, content):
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
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(rf):
            try:
                os.makedirs(os.path.dirname(rf), exist_ok=True)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    return f'Error: Failed to create directory "{os.path.dirname(rf)}": {str(e)}'
                else:
                    return f'Warning: Directory "{os.path.dirname(rf)}" already exists'

        try:
            with open(rf, 'w') as f:
                f.write(content)
                return f'Successfully wrote to "{rf}" ({len(content)} characters written)'
        except PermissionError as e:
            return f'Error: Permission denied to write to file "{file_path}": {str(e)}'
        except Exception as e:
            return f'Error: Failed to write to file "{file_path}": {str(e)}'
        except:
            return f'Error: Failed to write to file "{file_path}"'
