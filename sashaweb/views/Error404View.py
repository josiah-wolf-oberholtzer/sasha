from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config
from sashaweb.views._View import _View


@view_config(
    renderer='sashaweb:templates/error_404.mako',
    context=HTTPNotFound,
    )
class Error404View(_View):

    def __call__(self):
        return {
            'body_class': 'error',
            'message': self.request.exception.message,
            'title': self.title,
        }

    ### PUBLIC ATTRIBUTES ###

    @property
    def title(self):
        return 'SASHA | 404 Not Found'