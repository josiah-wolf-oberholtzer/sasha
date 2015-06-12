import numpy


class Regression(object):

    ### INITIALIZER ###

    def __init__(self, alpha=0.0):
        self._alpha = alpha
        self._beta = None
        self._beta0 = None

    ### PUBLIC METHODS ###

    def learn(self, x, y):
        if not isinstance(x, numpy.ndarray):
            message = "x must be an numpy 2d array"
            raise ValueError(message)
        if not isinstance(y, numpy.ndarray):
            message = "y must be an numpy 1d array"
            raise ValueError(message)
        if x.ndim > 2:
            message = "x must be an 2d array"
            raise ValueError(message)
        if x.shape[0] != y.shape[0]:
            message = "x and y are not aligned"
            raise ValueError(message)
        xm = x - numpy.mean(x)
        n = x.shape[0]
        p = x.shape[1]
        if n < p:
            xd = numpy.dot(xm, xm.T)
            if self.alpha:
                xd += self.alpha * numpy.eye(n)
            xdi = numpy.linalg.pinv(xd)
            self._beta = numpy.dot(numpy.dot(xm.T, xdi), y)
        else:
            xd = numpy.dot(xm.T, xm)
            if self.alpha:
                xd += self.alpha * numpy.eye(p)
            xdi = numpy.linalg.pinv(xd)
            self._beta = numpy.dot(xdi, numpy.dot(xm.T, y))
        self._beta0 = (
            numpy.mean(y) -
            numpy.dot(self._beta, numpy.mean(x, axis=0))
            )

    def predict(self, x):
        if not isinstance(x, numpy.ndarray):
            message = "x must be an numpy 2d array"
            raise ValueError(message)
        if x.ndim > 2:
            message = "x must be an 2d array"
            raise ValueError(message)
        if x.shape[1] != self._beta.shape[0]:
            message = "x and beta are not aligned"
            raise ValueError(message)
        prediction = numpy.dot(x, self._beta) + self._beta0
        return prediction

    def selected(self):
        if self._beta is None:
            message = "Regression coefficients are not computed. "
            message += "Run RidgeRegression.learn(x, y)"
            raise ValueError(message)
        selected = numpy.argsort(numpy.abs(self._beta))[::-1]
        return selected

    ### PUBLIC PROPERTIES ###

    @property
    def alpha(self):
        return self._alpha

    @property
    def beta(self):
        return self._beta

    @property
    def beta0(self):
        return self._beta0