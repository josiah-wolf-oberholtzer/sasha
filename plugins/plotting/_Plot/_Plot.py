import os
import matplotlib
if matplotlib.get_backend( ) != 'agg':
    matplotlib.use('agg')
import matplotlib.pyplot as plt
from sasha import SASHA
from sasha.core.plugins._MediaPlugin import _MediaPlugin


class _Plot(_MediaPlugin):

    media_type = 'plots'
    file_suffix = 'png'

    _width = 8

    ### PRIVATE METHODS ###

    def _build_plot( ):
        raise Exception('Not implemented here.')

    ### PUBLIC METHODS ###

    def delete(self): 
        if self.exists:
            os.remove(self.path)

    def write(self, **kwargs):
        fig = self._build_plot( )

        ax = fig.gca( )
        xlabel = ax.get_xlabel( )
        ylabel = ax.get_ylabel( )
        font = { }
#        font = {'fontname': 'Helvetica'}
        ax.set_xlabel(xlabel, **font)
        ax.set_ylabel(ylabel, **font)

        fig.set_size_inches(self._width, self._width * 0.5)
        fig.savefig(self.path, bbox_inches = 'tight', pad_inches = 0.05) # pad_inches must be > 0
