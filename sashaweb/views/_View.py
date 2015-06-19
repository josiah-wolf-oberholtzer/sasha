class _View(object):

    ### INITIALIZER ###

    def __init__(self, request):
        self._request = request

    ### PUBLIC ATTRIBUTES ###

    @property
    def title(self):
        return 'SASHA'

    @property
    def request(self):
        return self._request
