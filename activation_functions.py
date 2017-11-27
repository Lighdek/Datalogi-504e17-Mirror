import numpy
import math


euler = 2.7182818284590452353602874713527


def relu(x):
    return max(0, x)


def sigmod(x):
    return 1/1 + math.pow(euler, -x)


def tanh(x):
    return pow(euler, x)-pow(euler, -x) / pow(euler, x) + pow(euler, -x)


def l_relu(x,a):
    if x >= 0:
        return x
    else:
        return a*x


#deriv


def d_relu(x):
    if x < 0:
        return 0
    else:
        return 1


def d_sigmod(x):
    return x * (1 - sigmod(x))


def d_tanh(x):
    return 1-pow(tanh(x))


def d_l_relu(x, a):
    if x < 0:
        return a
    else:
        return 1
