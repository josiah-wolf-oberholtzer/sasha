import numpy as np


class Regression(object):

    def __init__(self, alpha=0.0):
        self.alpha = alpha
        self.__beta = None
        self.__beta0 = None
                
    def learn(self, x, y):
        if not isinstance(x, np.ndarray):
            raise ValueError("x must be an numpy 2d array")

        if not isinstance(y, np.ndarray):
            raise ValueError("y must be an numpy 1d array")

        if x.ndim > 2:
            raise ValueError("x must be an 2d array")
        
        if x.shape[0] != y.shape[0]:
            raise ValueError("x and y are not aligned")

        xm = x - np.mean(x)
        
        n = x.shape[0]
        p = x.shape[1]

        if n < p:
            xd = np.dot(xm, xm.T)
            if self.alpha:
                xd += self.alpha * np.eye(n)
            xdi = np.linalg.pinv(xd)
            self.__beta = np.dot(np.dot(xm.T, xdi), y)
        else:
            xd = np.dot(xm.T, xm)
            if self.alpha:
                xd += self.alpha * np.eye(p)
            xdi = np.linalg.pinv(xd)
            self.__beta = np.dot(xdi, np.dot(xm.T, y))
        
        self.__beta0 = np.mean(y) - np.dot(self.__beta, np.mean(x, axis=0))
   
    def predict(self, x):
        if not isinstance(x, np.ndarray):
            raise ValueError("x must be an numpy 2d array")
        
        if x.ndim > 2:
            raise ValueError("x must be an 2d array")
        
        if x.shape[1] != self.__beta.shape[0]:
            raise ValueError("x and beta are not aligned")
        
        p = np.dot(x, self.__beta) + self.__beta0
        
        return p
    
    def selected(self):
        if self.__beta == None:
            raise ValueError("regression coefficients are not computed. "
                             "Run RidgeRegression.learn(x, y)")

        sel = np.argsort(np.abs(self.__beta))[::-1]
        
        return sel

    def beta(self):
        """Return b_1, ..., b_p.
        """

        return self.__beta

    def beta0(self):
        """Return b_0.
        """

        return self.__beta0
