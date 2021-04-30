"""
Python 3.X is required.
"""

import numpy as np
import matplotlib.pyplot as plt
from dual import *


def calc_trace_determinant2(x, y):
    det = fx(x, y)*gy(x, y)-fy(x, y)*gx(x, y)
    tr = fx(x, y)+gy(x, y)
    return tr, det


def fx(x, y):
    return dual(f(dual(x, 1), y)-f(x, y)).im


def fy(x, y):
    return dual(f(x, dual(y, 1))-f(x, y)).im


def gx(x, y):
    return dual(g(dual(x, 1), y)-g(x, y)).im


def gy(x, y):
    return dual(g(x, dual(y, 1))-g(x, y)).im


def newton_method2(f, g, x_range, y_range, epsilon=10**(-13), limit=10**4):
    x_min, x_max = x_range
    y_min, y_max = y_range
    x = np.random.rand()*(x_max-x_min)+x_min
    y = np.random.rand()*(y_max-y_min)+y_min
    err_x, err_y = 1, 1
    count = 0
    while err_x > epsilon or err_y > epsilon:
        _, det = calc_trace_determinant2(x, y)
        dx = (fy(x, y)*g(x, y)-f(x, y)*gy(x, y))/det
        dy = (gx(x, y)*f(x, y)-g(x, y)*fx(x, y))/det
        x = x+dx
        y = y+dy
        err_x = np.abs(dx)
        err_y = np.abs(dy)
        count += 1
        if count > limit:
            raise RuntimeError("Count exceeded limit @ newton_method2.")
    return x, y


def f(x, y):
    """
    This is dummy function.
    Please override this process by using 'global'.
    e.g.
    ##########
    global f

    def f(x,y):
        return x**2 + y**2 + 1
    ##########
    """
    return 0


def g(x, y):
    """
    This is dummy function.
    Please override this process by using 'global'.
    e.g.
    ##########
    global g

    def g(x,y):
        return x**2 + y + 1
    ##########
    """
    return 0


def Brusselator(title='Brusselator'):
    global f, g

    def f(x, y):
        """
        dx/dt = f(x,y)
        """
        return a-(b+1)*x+x**2*y

    def g(x, y):
        """
        dy/dt = g(x,y)
        """
        return b*x-x**2*y

    # plot
    a = 0.5
    b = 1.
    x_range = [0, 3]
    y_range = [0,  10]
    samples = 1000
    p = newton_method2(f, g, x_range, y_range)  # Fixed point
    X, Y = np.meshgrid(
        np.linspace(*x_range, samples),
        np.linspace(*y_range, samples)
    )
    U = np.array(list(map(lambda rowX, rowY: list(map(lambda x, y: f(x, y), rowX, rowY)), X, Y)), float)
    V = np.array(list(map(lambda rowX, rowY: list(map(lambda x, y: g(x, y), rowX, rowY)), X, Y)), float)

    cntr_f = plt.contour(X, Y, U, 0, colors=plt.cm.tab10(0), linewidths=2)
    cntr_g = plt.contour(X, Y, V, 0, colors=plt.cm.tab10(1), linewidths=2)
    handle_p = plt.scatter(*p, marker='o', s=50, c=[plt.cm.tab10(7)], zorder=2)
    ((handle_f, _, _), _) = cntr_f.legend_elements()
    ((handle_g, _, _), _) = cntr_g.legend_elements()

    strm = plt.streamplot(X, Y, U, V, color=np.sqrt(
        U**2+V**2), linewidth=0.5, cmap=plt.cm.jet, density=2)
    cbar = plt.colorbar(strm.lines)
    cbar.set_label(r'$\sqrt{(f(x,y))^2 + (g(x,y))^2}$', rotation=90)
    plt.xlabel('x')
    plt.ylabel('y')

    plt.legend(
        [handle_f, handle_g, handle_p],
        ['f(x, y) = 0', 'g(x, y) = 0', 'Fixed_point'],
        loc='upper right'
    )
    plt.title(f'{title} (a={a}, b={b})')
    plt.grid()
    plt.show()
    plt.close('all')


def Van_der_Pol_oscillator(title='Van der Pol oscillator'):
    global f, g

    def f(x, y):
        """
        dx/dt = f(x,y)
        """
        return mu*(x-1/3*x**3-y)

    def g(x, y):
        """
        dy/dt = g(x,y)
        """
        return 1/mu*x

    # plot
    mu = 2.
    x_range = [-2, 2]
    y_range = [-4,  4]
    samples = 1000
    p = newton_method2(f, g, x_range, y_range)  # Fixed point
    X, Y = np.meshgrid(
        np.linspace(*x_range, samples),
        np.linspace(*y_range, samples)
    )
    U = np.array(list(map(lambda rowX, rowY: list(map(lambda x, y: f(x, y), rowX, rowY)), X, Y)), float)
    V = np.array(list(map(lambda rowX, rowY: list(map(lambda x, y: g(x, y), rowX, rowY)), X, Y)), float)

    cntr_f = plt.contour(X, Y, U, 0, colors=plt.cm.tab10(0), linewidths=2)
    cntr_g = plt.contour(X, Y, V, 0, colors=plt.cm.tab10(1), linewidths=2)
    handle_p = plt.scatter(*p, marker='o', s=50, c=[plt.cm.tab10(7)], zorder=2)
    ((handle_f, _, _), _) = cntr_f.legend_elements()
    ((handle_g, _, _), _) = cntr_g.legend_elements()

    strm = plt.streamplot(X, Y, U, V, color=np.sqrt(
        U**2+V**2), linewidth=0.5, cmap=plt.cm.jet, density=2)
    cbar = plt.colorbar(strm.lines)
    cbar.set_label(r'$\sqrt{(f(x,y))^2 + (g(x,y))^2}$', rotation=90)
    plt.xlabel('x')
    plt.ylabel('y')

    plt.legend(
        [handle_f, handle_g, handle_p],
        ['f(x, y) = 0', 'g(x, y) = 0', 'Fixed point'],
        loc='upper right'
    )
    plt.title(f'{title} (mu={mu})')
    plt.grid()
    plt.show()
    plt.close('all')


def Simple_damped_pendulum(title='Simple damped pendulum'):
    global f, g

    def f(x, y):
        """
        dx/dt = f(x,y)
        """
        return y

    def g(x, y):
        """
        dy/dt = g(x,y)
        """
        return -a*y-b*sin(x)

    # plot
    a = 1.
    b = 10.
    x_range = [-10, 10]
    y_range = [-10,  10]
    samples = 1000
    p = newton_method2(f, g, x_range, y_range)  # Fixed point
    X, Y = np.meshgrid(
        np.linspace(*x_range, samples),
        np.linspace(*y_range, samples)
    )
    U = np.array(list(map(lambda rowX, rowY: list(map(lambda x, y: f(x, y), rowX, rowY)), X, Y)), float)
    V = np.array(list(map(lambda rowX, rowY: list(map(lambda x, y: g(x, y), rowX, rowY)), X, Y)), float)

    cntr_f = plt.contour(X, Y, U, 0, colors=plt.cm.tab10(0), linewidths=2)
    cntr_g = plt.contour(X, Y, V, 0, colors=plt.cm.tab10(1), linewidths=2)
    handle_p = plt.scatter(*p, marker='o', s=50, c=[plt.cm.tab10(7)], zorder=2)
    ((handle_f, _, _), _) = cntr_f.legend_elements()
    ((handle_g, _, _), _) = cntr_g.legend_elements()

    strm = plt.streamplot(X, Y, U, V, color=np.sqrt(
        U**2+V**2), linewidth=0.5, cmap=plt.cm.jet, density=2)
    cbar = plt.colorbar(strm.lines)
    cbar.set_label(r'$\sqrt{(f(x,y))^2 + (g(x,y))^2}$', rotation=90)
    plt.xlabel('x')
    plt.ylabel('y')

    plt.legend(
        [handle_f, handle_g, handle_p],
        ['f(x, y) = 0', 'g(x, y) = 0', 'Fixed point'],
        loc='upper right'
    )
    plt.title(f'{title} (a={a}, b={b})')
    plt.grid()
    plt.show()
    plt.close('all')


if __name__ == '__main__':
    Brusselator()
    Van_der_Pol_oscillator()
    Simple_damped_pendulum()
