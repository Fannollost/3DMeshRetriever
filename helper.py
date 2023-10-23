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
