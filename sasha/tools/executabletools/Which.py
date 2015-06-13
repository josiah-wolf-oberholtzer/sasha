import os
from sasha.tools.executabletools.Executable import Executable


class Which(Executable):

    ### SPECIAL METHODS ###

    def __call__(self, program):
        def is_executable(fpath):
            return os.path.exists(fpath) and os.access(fpath, os.X_OK)
        def extension_candidates(file_path):
            yield file_path
            for extension in os.environ.get('PATHEXT', '').split(os.pathsep):
                yield file_path + extension
        file_path, file_name = os.path.split(program)
        if file_path:
            if is_executable(program):
                return program
        else:
            for path in os.environ['PATH'].split(os.pathsep):
                executable_file = os.path.join(path, program)
                for candidate in extension_candidates(executable_file):
                    if is_executable(candidate):
                        return candidate
        return None