from shapeDescriptors import weight

def euclidianDistance(fvector1, fvector2):
    totalDistance = 0
    w = 0
    distanceContr = {"A3":0,"D1":0,"D2":0,"D3":0,"D4":0}
    totalWeight = sum(list(weight.values()))
    for key in fvector1.keys():
        k = key[:2]
        if k == "A3" or k == "D1" or k == "D2"  or k == "D3"  or k == "D4":
            fDist = (weight[k] / totalWeight) * 8 * abs(fvector1[key] - fvector2[key]) ** 2
            w += weight[k] / (totalWeight * 8)
            totalDistance += fDist
            distanceContr[k] += fDist
        elif key not in ['Class', 'File']:
            fDist = (weight[key] / sum(list(weight.values()))) * abs(fvector1[key] - fvector2[key]) ** 2
            w += weight[key] / sum(list(weight.values()))
            totalDistance += fDist
            distanceContr[key] = fDist
    if w > 1+1e-9 or w < 1-1e-9:
        raise Exception("Sum of weight not equal to 1 - Sum : "+ str(w))
    distanceContr = {key: val for key,val in sorted(distanceContr.items(), key = lambda ele: ele[1], reverse = True)}
    return totalDistance**0.5, distanceContr
 