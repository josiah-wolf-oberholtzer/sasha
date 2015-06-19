from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config
from sashaweb.views.View import View


@view_config(
    renderer='sashaweb:templates/error_404.mako',
    context=HTTPNotFound,
    )
class Error404View(View):

    ### SPECIAL METHODS ###

    def __call__(self):
        self.request.response.status = 404
        return {
            'body_class': 'error',
            'message': self.request.exception.message,
            'title': self.title,
            }

    ### PUBLIC ATTRIBUTES ###

    @property
    def title(self):
        return 'SASHA | 404 Not Found'