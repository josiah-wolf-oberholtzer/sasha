from abc import ABCMeta
import subprocess
from sasha.tools.systemtools import Immutable


class Wrapper(Immutable):

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta

    ### PRIVATE METHODS ###

    def _exec(self, command):
        p = subprocess.Popen(command, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        err = p.stderr.read()
        out = p.stdout.read()
        p.stdout.close()
        p.stderr.close()
        return out, err
