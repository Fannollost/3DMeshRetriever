import os
import pymeshlab as pml

def getEveryElementFromEveryList(x, deeperList):
    return [list[x] for list in deeperList]

def get_immediate_subdirectories(dir):
    return [name for name in os.listdir(dir) if os.path.isdir(os.path.join(dir,name))]

def get_all_files(dir):
    return  [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]

def flatten_list(listOfLists):
    return [item for sublist in listOfLists for item in sublist]

def discard_every_x_from_every_list(x, listOfList, first = True):
    if(first):
        return [sub_list[x:] for sub_list in listOfList]
    else:
        return [sub_list[:x] for sub_list in listOfList]

def get_1_from_list(list):
    l = []
    for obj in list:
        if obj in l:
            continue
        else:
            l.append(obj)
    return l
