import numpy as np

def dist(a, b):
    if len(a) != len(b):
        raise("Dimmensionality is not the same")

    res = 0
    for i in range(len(a)):
        res += (b[i] - a[i]) ** 2
    return res**0.5

def length(vect):
    return dist(vect, [0, 0, 0])


def crossProduct(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
