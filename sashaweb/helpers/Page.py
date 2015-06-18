from string import Template
from webhelpers import paginate
from webhelpers.html import HTML


class Page(paginate.Page):

    def _pagerlink(self, page, text):
        # Let the url_for() from webhelpers create a new link and set
        # the variable called 'page_param'. Example:
        # You are in '/foo/bar' (controller='foo', action='bar')
        # and you want to add a parameter 'page'. Then you
        # call the navigator method with page_param='page' and
        # the url_for() call will create a link '/foo/bar?page=...'
        # with the respective page number added.
        link_params = {}
        # Use the instance kwargs from Page.__init__ as URL parameters
        link_params.update(self.kwargs)
        # Add keyword arguments from pager() to the link as parameters
        link_params.update(self.pager_kwargs)
        link_params[self.page_param] = page

        # Get the URL generator
        if self._url_generator is not None:
            url_generator = self._url_generator
        else:
            try:
                import pylons
                url_generator = pylons.url.current
            except (ImportError, AttributeError):
                try:
                    import routes
                    url_generator = routes.url_for
                    config = routes.request_config()
                except (ImportError, AttributeError):
                    raise NotImplementedError("no URL generator available")
                else:
                    # if the Mapper is configured with explicit=True we have to fetch
                    # the controller and action manually
                    if config.mapper.explicit:
                        if hasattr(config, 'mapper_dict'):
                            for k, v in config.mapper_dict.items():
                                if k != self.page_param:
                                    link_params[k] = v

        # Create the URL to load a certain page
        link_url = url_generator(**link_params)

        if self.onclick:  # create link with onclick action for AJAX
            # Create the URL to load the page area part of a certain page (AJAX
            # updates)
            link_params[self.partial_param] = 1
            partial_url = url_generator(**link_params)
            try:  # if '%s' is used in the 'onclick' parameter (backwards compatibility)
                onclick_action = self.onclick % (partial_url,)
            except TypeError:
                onclick_action = Template(self.onclick).safe_substitute({
                    "partial_url": partial_url,
                    "page": page
                    })
            a_tag = HTML.a(text, href=link_url, onclick=onclick_action, **self.link_attr)
        else:  # return static link
            a_tag = HTML.a(text, href=link_url, **self.link_attr)
        li_tag = HTML.li(a_tag)
        return li_tag

    def _range(self, regexp_match):
        """
        Return range of linked pages (e.g. '1 2 [3] 4 5 6 7 8').

        Arguments:

        regexp_match
            A "re" (regular expressions) match object containing the
            radius of linked pages around the current page in
            regexp_match.group(1) as a string

        This function is supposed to be called as a callable in
        re.sub.

        """
        radius = int(regexp_match.group(1))

        # Compute the first and last page number within the radius
        # e.g. '1 .. 5 6 [7] 8 9 .. 12'
        # -> leftmost_page  = 5
        # -> rightmost_page = 9
        leftmost_page = max(self.first_page, (self.page - radius))
        rightmost_page = min(self.last_page, (self.page + radius))

        nav_items = []

        # Create a link to the first page (unless we are on the first page
        # or there would be no need to insert '..' spacers)
        if self.page != self.first_page and self.first_page < leftmost_page:
            nav_items.append(self._pagerlink(self.first_page, self.first_page))

        # Insert dots if there are pages between the first page
        # and the currently displayed page range
        if leftmost_page - self.first_page > 1:
            # Wrap in a SPAN tag if nolink_attr is set
            text = '..'
            if self.dotdot_attr:
                text = HTML.span(c=text, **self.dotdot_attr)
            text = HTML.li(text, **{'class': 'disabled'})
            nav_items.append(text)

        for thispage in xrange(leftmost_page, rightmost_page + 1):
            # Hilight the current page number and do not use a link
            if thispage == self.page:
                text = '%s' % (thispage,)
                # Wrap in a SPAN tag if nolink_attr is set
                if self.curpage_attr:
                    text = HTML.span(c=text, **self.curpage_attr)
                text = HTML.li(text, **{'class': 'active'})
                nav_items.append(text)
            # Otherwise create just a link to that page
            else:
                text = '%s' % (thispage,)
                nav_items.append(self._pagerlink(thispage, text))

        # Insert dots if there are pages between the displayed
        # page numbers and the end of the page range
        if self.last_page - rightmost_page > 1:
            text = '..'
            # Wrap in a SPAN tag if nolink_attr is set
            if self.dotdot_attr:
                text = HTML.span(c=text, **self.dotdot_attr)
            text = HTML.li(text, **{'class': 'disabled'})
            nav_items.append(text)

        # Create a link to the very last page (unless we are on the last
        # page or there would be no need to insert '..' spacers)
        if self.page != self.last_page and rightmost_page < self.last_page:
            nav_items.append(self._pagerlink(self.last_page, self.last_page))

        return self.separator.join(nav_items)