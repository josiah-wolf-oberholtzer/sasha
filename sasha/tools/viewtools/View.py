from webhelpers import paginate


class View(object):

    ### INITIALIZER ###

    def __init__(self, request):
        self._request = request

    ### PUBLIC ATTRIBUTES ###

    @property
    def page_url(self):
        return paginate.PageURL_WebOb(self.request)

    @property
    def request(self):
        return self._request

    @property
    def title(self):
        return 'SASHA'