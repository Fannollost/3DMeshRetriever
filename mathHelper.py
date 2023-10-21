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

def areaTriangle(a, b, c):
    return length(crossProduct(vector(a,b), vector(a,c))) / 2


def vector(v1, v2):
    return [v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2]]

def angleBetween(vect1, vect2):
    x = np.dot(vect1,vect2) / (length(vect1) * length(vect2))
    if x < -1 : x = -1
    if x > 1 : x = 1
    return np.arccos(x)

def volumeTetrahydron(vect1, vect2, vect3):
    return abs(np.dot(np.cross(vect1,vect2), vect3) / 6)