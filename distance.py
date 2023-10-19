from shapeDescriptors import weight
import numpy as np

def get_manhattan_distance(vec_a, vec_b, range_min, range_max, normalize=True):
    dist = 0
    for number_a, number_b in zip(vec_a, vec_b):
        dist += abs(number_a - number_b)
    if normalize:
        max_dist = (range_max - range_min) * len(vec_a)
        dist /= max_dist

    return dist

def get_euclidean_distance(vec_a, vec_b, range_min, range_max, normalize=True):
    dist = np.linalg.norm([x-y for (x,y) in zip(vec_a, vec_b)])
    if normalize:
        max_dist = np.sqrt(len(vec_a) * ((range_max - range_min)**2))
        dist /= max_dist
    
    return dist

def get_cosine_distance(vec_a, vec_b, normalize=True):
    cosine_similarity = np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b))    
    dist = 1 - cosine_similarity
    if normalize:
        dist /= 2
    
    return dist