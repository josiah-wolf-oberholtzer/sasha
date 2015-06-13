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