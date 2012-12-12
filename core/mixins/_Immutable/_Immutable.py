class _Immutable(object):

    __slots__ = ()

    ## OVERLOADS ##

    def __copy__(self, *args):
        return type(self)(self)

    __deepcopy__ = __copy__

    def __delattr__(self, *args):
        raise AttributeError('objects are immutable: "%s".' % self.__class__.__name__)

    def __getstate__(self):
        state = { }
        for slot in self.__slots__:
            state[slot] = getattr(self, slot)
        return state

    def __setattr__(self, *args):
        raise AttributeError('objects are immutable: "%s".' % self.__class__.__name__)

    def __setstate__(self, state):
        for k, v in state.iteritems():
            object.__setattr__(self, k, v)
       
      


