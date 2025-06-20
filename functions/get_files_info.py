import os
import errno


def get_files_info(working_directory, directory=None):
    if not os.path.exists(working_directory):
        return f'Error: Working directory "{working_directory}" does not exist'

    if not os.path.isdir(working_directory):
        return f'Error: Working directory "{working_directory}" is not a directory'

    wd = os.path.abspath(working_directory)

    if directory is not None:
        if directory.strip() == "":
            return f'Error: Directory parameter cannot be empty'

        try:
            rd = os.path.abspath(os.path.join(wd, directory))
        except (TypeError, ValueError) as e:
            return f'Error: Invalid directory parameter "{directory}": {str(e)}'

        if not rd.startswith(wd):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.exists(rd):
            return f'Error: Directory "{directory}" does not exist in working directory'

        if not os.path.isdir(rd):
            return f'Error: "{directory}" is not a directory'

        try:
            dirlist = os.listdir(rd)
        except PermissionError:
            return f'Error: Permission denied when accessing directory "{directory}"'
        except OSError as e:
            return f'Error: Cannot access directory "{directory}": {str(e)}'

        resultslist = []
        for dir in dirlist:
            full_path = os.path.join(rd, dir)
            try:
                if os.path.isdir(full_path):
                    size = os.path.getsize(full_path)
                    resultslist.append(f'- {dir}: file_size={size}, is_dir=True')
                elif os.path.isfile(full_path):
                    size = os.path.getsize(full_path)
                    resultslist.append(f'- {dir}: file_size={size}, is_dir=False')
                else:
                    resultslist.append(f'- {dir}: unknown type')
            except (OSError, PermissionError) as e:
                resultslist.append(f'- {dir}: error accessing - {str(e)}')

        if resultslist:
            return "\n".join(resultslist)
        else:
            return f'Error: Directory parameter is required'
