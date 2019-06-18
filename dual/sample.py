import numpy as np
import matplotlib.pyplot as plt
from dual import *


def normal(x, mu, sigma2):
    return exp(-0.5*(x-mu)**2/sigma2)/(np.sqrt(2*np.pi*sigma2))


if __name__ == '__main__':
    mu, sigma2 = 0., 4.
    X = np.linspace(-5, 7)
    _Y = [normal(dual(x, 1), mu, sigma2) for x in X]
    Y = [dual(y).re for y in _Y]
    dY_dX = [dual(_y-y).im for _y, y in zip(_Y, Y)]
    plt.title('Normal distribution')
    plt.plot(X, Y, label='N({}, {})'.format(mu, sigma2))
    plt.plot(X, dY_dX, label='Derivative of N({}, {})'.format(mu, sigma2))
    plt.legend(loc='upper right')
    plt.grid()
    plt.show()
