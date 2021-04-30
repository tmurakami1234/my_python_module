'''
@author: Taishu Murakami <tmurakami.1234@gmail.com>
'''

import math


def is_dual(obj):
    return hasattr(obj, 're') and hasattr(obj, 'im')


def to_dual(obj):
    if is_dual(obj):
        return obj
    elif isinstance(obj, tuple):
        return dual(*obj)
    else:
        return dual(obj)


class dual:
    def __init__(self, re=0, im=0):
        _re = 0
        _im = 0
        if is_dual(re):
            _re = re.re
            _im = re.im
        else:
            _re = re
        if is_dual(im):
            _re = _re - im.im
            _im = _im + im.re
        else:
            _im = _im + im
        self.__dict__['re'] = _re
        self.__dict__['im'] = _im

    def __setattr__(self, name, value):
        raise TypeError('Dual numbers are immutable.')

    def __hash__(self):
        if not self.im:
            return hash(self.re)
        return hash((self.re, self.im))

    def __repr__(self):
        if not self.im:
            return 'dual({})'.format(self.re)
        else:
            return 'dual({},{})'.format(self.re, self.im)

    def __str__(self):
        if not self.im:
            return repr(self.re)
        else:
            return 'dual({},{})'.format(self.re, self.im)

    def __neg__(self):
        return dual(-self.re, -self.im)

    def __pos__(self):
        return self

    def __abs__(self):
        return math.hypot(self.re, self.im)

    def __int__(self):
        if self.im:
            raise ValueError("Can't convert Dual with nonzero im to int.")
        return int(self.re)

    def __long__(self):
        if self.im:
            raise ValueError("Can't convert Dual with nonzero im to long.")
        return long(self.re)

    def __float__(self):
        if self.im:
            raise ValueError("Can't convert Dual with nonzero im to float.")
        return float(self.re)

    def __nonzero__(self):
        return not (self.re == self.im == 0)

    def __add__(self, other):
        other = to_dual(other)
        return dual(self.re+other.re, self.im+other.im)

    __radd__ = __add__

    def __sub__(self, other):
        other = to_dual(other)
        return dual(self.re-other.re, self.im-other.im)

    def __rsub__(self, other):
        other = to_dual(other)
        return other-self

    def __mul__(self, other):
        other = to_dual(other)
        return dual(self.re*other.re, self.re*other.im+self.im*other.re)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = to_dual(other)
        d = float(other.re*other.re)
        if not d:
            raise ZeroDivisionError('Dual division.')
        return dual(self.re*other.re/d, (self.im*other.re-self.re*other.im)/d)

    def __rtruediv__(self, other):
        other = to_dual(other)
        return other/self

    def __pow__(self, n):
        if is_dual(n):
            if n.im:
                if self.im:
                    raise TypeError('Dual to the Dual power.')
                else:
                    return dual(1, n.im*math.log(self.re))
            n = n.re
        return dual(pow(self.re, n), n*pow(self.re, n-1)*self.im)

    def __rpow__(self, base):
        base = to_dual(base)
        return pow(base, self)


def exp(z):
    z = to_dual(z)
    return dual(math.exp(z.re), math.exp(z.re)*z.im)


def log(z):
    z = to_dual(z)
    return dual(math.log(z.re), float(z.im)/z.re)


def sin(z):
    z = to_dual(z)
    return dual(math.sin(z.re), math.cos(z.re)*z.im)


def cos(z):
    z = to_dual(z)
    return dual(math.cos(z.re), -math.sin(z.re)*z.im)


def tan(z):
    return sin(z)/cos(z)


def sinh(z):
    return 0.5*(exp(z)-exp(-z))


def cosh(z):
    return 0.5*(exp(z)+exp(-z))


def tanh(z):
    return sinh(z)/cosh(z)


def sqrt(z):
    return z**0.5


def test():
    print('Examples of dual module\n')
    a, b = 1, 2
    print('a = {}\t\t\t{}'.format(a, type(a)))
    print('b = {}\t\t\t{}'.format(b, type(b)))
    print('dual(a,b) = {}\t{}'.format(dual(a, b), type(dual(a, b))))
    print('dual(a) = {}\t\t{}'.format(dual(a), type(dual(a))))
    print('dual(a,0) = {}\t\t{}'.format(dual(a, 0), type(dual(a, 0))))
    print('------------------------------')
    x = dual(0, 1)
    print('x = {}\t\t{}'.format(x, type(x)))
    print('x.re = {}\t\t{}'.format(x.re, type(x.re)))
    print('x.im = {}\t\t{}'.format(x.im, type(x.im)))
    print('dual(x) = {}\t{}'.format(dual(x), type(dual(x))))
    print('------------------------------')
    x = dual(0, 1)
    a = 2
    print('x = {}\t\t{}'.format(x, type(x)))
    print('a = {}\t\t\t{}'.format(a, type(a)))
    print('x + a = {}'.format(x+a))
    print('x - a = {}'.format(x-a))
    print('x * a = {}'.format(x*a))
    print('x / a = {}'.format(x/a))
    print('------------------------------')
    x, y = dual(1, 2), dual(2, 5)
    print('x = {}'.format(x))
    print('y = {}'.format(y))
    print('x + y = {}'.format(x+y))
    print('x - y = {}'.format(x-y))
    print('x * y = {}'.format(x*y))
    print('x / y = {}'.format(x/y))
    print('sin(x) = {}'.format(sin(x)))
    print('exp(x)*log(y) = {}'.format(exp(x)*log(y)))
    print('tanh(sin(y)) = {}'.format(tanh(sin(y))))
    print('------------------------------')
    X = [i for i in range(3)]
    Y = [2*i for i in range(3)]
    Z = [dual(x, y) for x, y in zip(X, Y)]
    print('X = {}'.format(X))
    print('Y = {}'.format(Y))
    print('Z = [dual(x,y) for x,y in zip(X,Y)] = {}'.format(Z))
    print('[z.re for z in Z] = {}'.format([z.re for z in Z]))


if __name__ == '__main__':
    test()
