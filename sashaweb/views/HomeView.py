from pyramid.view import view_config
from sashaweb.views.View import View


@view_config(
    route_name='home',
    renderer='sashaweb:templates/home.mako',
    )
class HomeView(View):

    ### SPECIAL METHODS ###

    def __call__(self):
        return {
            'body_class': 'home',
            'title': self.title,
            }

    ### PUBLIC ATTRIBUTES ###

    @property
    def title(self):
        return 'SASHA | Home'