import os
import subprocess


class Executable(object):

    ### PRIVATE METHODS ###

    def _exec(self, command):
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            )
        stderr = process.stderr.read()
        stdout = process.stdout.read()
        process.stdout.close()
        process.stderr.close()
        return stdout, stderr

    ### PUBLIC METHODS ###

    @staticmethod
    def find_executable(executable_name):
        def is_executable(fpath):
            return os.path.exists(fpath) and os.access(fpath, os.X_OK)
        def extension_candidates(file_path):
            yield file_path
            for extension in os.environ.get('PATHEXT', '').split(os.pathsep):
                yield file_path + extension
        file_path, file_name = os.path.split(executable_name)
        if file_path:
            if is_executable(executable_name):
                return executable_name
        else:
            for path in os.environ['PATH'].split(os.pathsep):
                executable_file = os.path.join(path, executable_name)
                for candidate in extension_candidates(executable_file):
                    if is_executable(candidate):
                        return candidate
        return None