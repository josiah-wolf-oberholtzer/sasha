from pyramid.view import view_config
from sasha.tools.viewtools.View import View


@view_config(
    route_name='help',
    renderer='sasha:templates/help.mako',
    )
class HelpView(View):

    ### SPECIAL METHODS ###

    def __call__(self):
        return {
            'body_class': 'help',
            'title': self.title,
            }

    ### PUBLIC ATTRIBUTES ###

    @property
    def title(self):
        return 'SASHA | Help'