import abc
import os
import matplotlib
if matplotlib.get_backend() != 'agg':
    matplotlib.use('agg')
import matplotlib.pyplot as plt
from sasha.tools.assettools.Asset import Asset


class Plot(Asset):

    ### CLASS VARIABLES ###

    __slots__ = ()
    _width = 8
    file_suffix = 'svg'
    media_type = 'plots'

    ### PRIVATE METHODS ###

    @abc.abstractmethod
    def _build_plot():
        raise NotImplemented

    ### PUBLIC METHODS ###

    def delete(self):
        if self.exists:
            os.remove(self.path)

    def get_image_link(self, request):
        from webhelpers.html import HTML
        href = self.client.get_url(request)
        content = self.get_image_tag(request)
        return HTML.tag('a', href=href, c=content)

    def get_image_tag(self, request):
        from webhelpers.html import HTML
        return HTML.tag('img', src=self.get_static_path(request))

    def write(self, **kwargs):
        fig = self._build_plot()
        ax = fig.gca()
        xlabel = ax.get_xlabel()
        ylabel = ax.get_ylabel()
        font = {}
        ax.set_xlabel(xlabel, **font)
        ax.set_ylabel(ylabel, **font)
        fig.set_size_inches(self._width, self._width * 0.5)
        output_directory, _ = os.path.split(self.path)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        fig.savefig(self.path, bbox_inches='tight', pad_inches=0.05)