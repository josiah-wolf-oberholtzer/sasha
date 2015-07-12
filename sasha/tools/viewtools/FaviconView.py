import os
from pyramid.response import FileResponse
from pyramid.view import view_config


@view_config(route_name='favicon')
class FaviconView(object):

    def __init__(self, request):
        self.request = request

    def __call__(self):
        import sasha
        root = sasha.__path__[0]
        path = os.path.join(root, 'static', 'img', 'favicon.ico')
        return FileResponse(path, request=self.request)