from pyramid.url import static_url


class Helper(object):

    def __init__(self, arg):
        self.request = arg

    ### PUBLIC ATTRIBUTES ###

    @property
    def static_url(self):
        return static_url(self.static_path, self.request)
