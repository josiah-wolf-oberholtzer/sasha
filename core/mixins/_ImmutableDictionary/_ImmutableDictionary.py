class _ImmutableDictionary(dict):

    ### OVERRIDES ###

    def __delitem__(self, *args):
        raise AttributeError('objects are immutable: "%s".' % self.__class__.__name__)

    def __setitem__(self, *args):
        raise AttributeError('objects are immutable: "%s".' % self.__class__.__name__)
