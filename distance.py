from shapeDescriptors import weight, histogramLimits
import numpy as np
from scipy.optimize import minimize
from scipy.stats import wasserstein_distance
from helper import discard_every_x_from_every_list

def get_manhattan_distance(vec_a, vec_b, range_min, range_max, normalize=True):
    dist = 0
    for number_a, number_b in zip(vec_a, vec_b):
        dist += abs(number_a - number_b)
    if normalize:
        max_dist = (range_max - range_min) * len(vec_a)
        dist /= max_dist

    return dist

def euclidianDist(f1, f2):
    sumDist = 0
    tot_weight = 0
    max_weight = sum(list(weight.values()))
    for key in range(len(f2) - 2):
        ka = getProperty(key)
        k = ka[:2]
        key = key + 2
        if k=="A3" or k=="D1" or k=="D2" or k=="D3" or k=="D4":
            featureDist = (weight[k] / (max_weight * weight[k])) * abs(f1[key] - f2[key]) ** 2
            tot_weight += weight[k] / (max_weight * weight[k])
            sumDist += featureDist
        elif ka not in ['File', 'Class'] :
            featureDist = (weight[ka] / max_weight) * abs(f1[key] - f2[key]) ** 2
            tot_weight += weight[ka] / max_weight
            sumDist += featureDist
    return sumDist**0.5

def getProperty(key):
    if(key >= 12 and key < 20):
        return "A3"
    elif(key >= 20 and key < 28):
        return "D1"
    elif(key >= 28 and key < 36):
        return "D2"
    elif(key >= 36 and key < 44):
        return "D3"
    elif(key >= 44 and key < 52):
        return "D4"
    else :
        return list(weight.keys())[key]
    
def get_cosine_distance(vec_a, vec_b, normalize=True):
    vec_a = vec_a[2:]
    vec_b = vec_b[2:]
    cosine_similarity = np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b))    
    dist = 1 - cosine_similarity
    if normalize:
        dist /= 2
    
    return dist

def emd(v1,v2):
    if len(v1) != len(v2):
        raise ValueError("Not same lenght")
    v1 = v1[2:]
    v2 = v2[2:]
    return wasserstein_distance(v1,v2)