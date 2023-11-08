from shapeDescriptors import weight, histogramLimits
import numpy as np
from scipy.optimize import minimize
from scipy.stats import wasserstein_distance
from helper import discard_every_x_from_every_list,flatten_list
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.decomposition import PCA
from helper import getEveryElementFromEveryList

def getOptimizedWeights(features, labels):
   
    num_features_to_select = 7 
    selector = SelectKBest(score_func=mutual_info_classif, k=num_features_to_select)
    f = [row[:9] for row in features]
    X_first9 = discard_every_x_from_every_list(2,f)
    selector.fit(X_first9,  getEveryElementFromEveryList(0,features))  # Use appropriate class labels (y) or dummy labels if needed
    feature_weights_first9 = selector.scores_

    # Step 3: Apply PCA to the last 150 components
    pca = PCA(n_components=5)  # Reducing to 30 principal components for the last 150 components
    f = [row[9:] for row in features]
    X_last150 = f
    pca.fit(X_last150)
    explained_variance_last150 = pca.explained_variance_ratio_

    # Step 5: Combine the two sets of weights
    combined_weights = np.concatenate((feature_weights_first9, explained_variance_last150))
    return combined_weights
    #intra_class_weights = []
    #classes = getEveryElementFromEveryList(0,features)
    #for cls in np.unique(classes):
    #    selector = SelectKBest(score_func=mutual_info_classif, k=12)
    #    print(cls)
    #    row_class = discard_every_x_from_every_list(2, [row for row in features if row[0] == cls])
    #    selector.fit(row_class, np.ones(np.array(row_class).shape[0]))
    #    feature_weights = selector.scores_
    #    intra_class_weights.append(feature_weights)
#
    #intra_class_weights = [weights / np.sum(weights) for weights in intra_class_weights]
#
    #selector = SelectKBest(score_func=mutual_info_classif, k=12)
    #selector.fit(discard_every_x_from_every_list(2, features), getEveryElementFromEveryList(0,features))
    #inter_class_weights = selector.scores_
    #inter_class_weights /= np.sum(inter_class_weights)
    #final_feature_weights = np.mean(intra_class_weights, axis=0) * inter_class_weights
    return final_feature_weights


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
            continue
            featureDist = (weight[k] / (max_weight)) * abs(f1[key] - f2[key]) ** 2
            tot_weight += weight[k] / (max_weight)
            sumDist += featureDist
        elif ka not in ['File', 'Class'] :
            featureDist = (weight[ka] / max_weight) * abs(f1[key] - f2[key]) ** 2
            tot_weight += weight[ka] / max_weight
            sumDist += featureDist
    return sumDist**0.5

def getProperty(key):
    if(key >= 7 and key < 57):
        return "A3"
    elif(key >= 57 and key < 107):
        return "D1"
    elif(key >= 107 and key < 157):
        return "D2"
    elif(key >= 157 and key < 207):
        return "D3"
    elif(key >= 207 and key < 257):
        return "D4"
    else :
        print(key)
        return list(weight.keys())[key]
    
def get_cosine_distance(vec_a, vec_b, normalize=True):
    vec_a = vec_a[2:]
    vec_b = vec_b[2:]
    cosine_similarity = np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b))    
    dist = 1 - cosine_similarity
    if normalize:
        dist /= 2
    
    return dist

def emd(f1,f2):
    if len(f1) != len(f2):
        raise ValueError("Not same lenght")
    f1 = f1[9:]
    f2 = f2[9:]
    a3 = np.full(50,weight['A3'] / 250)
    d1 = np.full(50,weight['D1'] / 250)
    d2 = np.full(50,weight['D2'] / 250)
    d3 = np.full(50,weight['D3'] / 250)
    d4 = np.full(50,weight['D4'] / 250)
    w = flatten_list([list(a3), list(d1), list(d2), list(d3), list(d4)])
    distance = wasserstein_distance(f1,f2,w)
    
    return distance **0.5