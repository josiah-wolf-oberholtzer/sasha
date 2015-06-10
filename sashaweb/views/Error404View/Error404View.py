from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config
from sashaweb.views._View import _View


@view_config(renderer='sashaweb:views/Error404View/error_404.mako', context=HTTPNotFound)
class Error404View(_View):

    def __call__(self):
        return {
            'body_class': 'error',
            'message': self.request.exception.message,
            'page_title': self.page_title,
        }

    ### PUBLIC ATTRIBUTES ###

    @property
    def page_title(self):
        return 'SASHA | 404 Not Found'