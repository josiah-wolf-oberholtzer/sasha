from abc import ABCMeta, abstactmethod
import subprocess
from sasha.core.mixins import _Immutable


class _Wrapper(_Immutable):

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta

    ### PRIVATE METHODS ###

    def _exec(self, command):
        p = subprocess.Popen(command, shell = True,
            stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        err = p.stderr.read( )
        out = p.stdout.read( )
        p.stdout.close( )
        p.stderr.close( )
        return out, err
