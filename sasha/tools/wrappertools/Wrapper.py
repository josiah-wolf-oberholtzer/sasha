from abc import ABCMeta
import subprocess


class Wrapper(object):

    ### CLASS VARIABLES ###

    __metaclass__ = ABCMeta
    __slots__ = ()

    ### PRIVATE METHODS ###

    def _exec(self, command):
        p = subprocess.Popen(command, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        err = p.stderr.read()
        out = p.stdout.read()
        p.stdout.close()
        p.stderr.close()
        return out, err