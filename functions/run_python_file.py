import os
import errno
import subprocess

def run_python_file(working_directory, file_path):
    if not os.path.exists(working_directory):
        return f'Error: Working directory "{working_directory}" does not exist'

    if not os.path.isdir(working_directory):
        return f'Error: Working directory "{working_directory}" is not a directory'

    wd = os.path.abspath(working_directory)

    if file_path is not None:
        if file_path.strip() == "":
            return f'Error: File parameter cannot be empty'

        try:
            rp = os.path.abspath(os.path.join(wd, file_path))
        except (TypeError, ValueError) as e:
            return f'Error: Invalid file parameter "{file_path}": {str(e)}'

        if not rp.startswith(wd):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(rp):
            return f'Error: File "{file_path}" not found.'

        if rp[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file.'

        try:
            output = subprocess.run(["python3", rp], timeout=30, capture_output=True, cwd=wd)
        except subprocess.TimeoutExpired as e:
            return f'Error: Execution timed out after {e.timeout} seconds'
        except Exception as e:
            return f"Error: executing Python file: {e}"

        stdout = output.stdout.decode('utf-8')
        stdoutstr = f'STDOUT: {stdout}'
        stderr = output.stderr.decode('utf-8')
        stderrstr = f'STDERR: {stderr}'
        exitcode = output.returncode
        runstr = f'RAN: python3 {rp}'
        if output == None:
            return 'No output produced'
        if exitcode != 0:
            returnitems = [runstr, stderrstr, f'Process exited with code {exitcode}']
        else:
            returnitems = [runstr, stdoutstr, stderrstr]
        return "\n".join(returnitems)
