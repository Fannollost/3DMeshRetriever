import os
import csv
from meshLoading import Mesh
from meshDataTypes import dataTypes
import pandas as pd
from featureExtractor import FeatureExtractor
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from distance import get_cosine_distance, get_euclidean_distance
import paths
from helper import flatten_list, get_all_files, get_immediate_subdirectories
import heapq
class dataExporter:

    def __init__(self, fileName, data):
        self.path = fileName
        self.file = open(self.path, 'w', newline='')
        self.writer = csv.writer(self.file)
        self.writer.writerow(data[0].keys())
        for d in range(len(data)):
            self.writer.writerow(data[d].values())

def normaliseFeatures(featuresfile, toSave):
    df = pd.read_csv(featuresfile)
    columns = df.columns
    for column in columns:
        if column[:2] not in ['A3', 'D1', 'D2', 'D3', 'D4'] and column not in ['File', 'Class']:
            minVal = min(df[column].tolist())
            maxVal = max(df[column].tolist())
            df[column] = (df[column] - minVal) / (maxVal - minVal)
    
    """df = pd.read_csv(featuresfile)
    scaler = MinMaxScaler()

    group_size = 8
    column_groups = [df.columns[-40 + i:-40 + i + group_size] for i in range(0, 40, group_size)]

    for group in column_groups:
        for column in group[2:]:
            if df[column].dtype in [int, float]:
                df[column] = scaler.fit_transform(df[[column]])"""
    df.to_csv(toSave, index=False)

def getAllDistances():
    DB = getFeatures()
    
    distances = []
    for a in range(len(DB)):
        for b in range(a + 1,len(DB)):
            obj_a = DB[a]
            obj_b = DB[b]
            distance = get_euclidean_distance(obj_a[2:], obj_b[2:],0,1)
            name_a = obj_a[0] + "/" + obj_a[1]
            name_b = obj_b[0] + "/" + obj_b[1]
            distances.append((name_a,name_b,distance))
    return distances

def getDistanceToMesh(folder, mesh, nrOfResults):
    print(nrOfResults)
    fEx = FeatureExtractor('normalisedDB/' + folder + '/' + mesh)
    data = {dataTypes.CLASS.value : folder, dataTypes.FILE.value : mesh}
    features = fEx.getFeatures()
    data.update(features)
    query_mesh_features = list(data.values())

    DB = getFeatures()
    distances = []
    for a in range(len(DB)):
        obj_a = DB[a]
        if(obj_a[0].lower() + "/" + obj_a[1].lower() == folder.lower() + "/" + mesh.lower()):
            continue
        distance = get_euclidean_distance(obj_a[2:], query_mesh_features[2:], 0, 1, True)
        name_a = obj_a[0] + "/" + obj_a[1]
        distances.append((name_a,distance))
    
    sorted_result = sorted(distances,key=lambda couple:couple[1])
    x_closest_results = sorted_result[:int(nrOfResults)]

    resultpaths = []

    for result in x_closest_results:
        resultpaths.append(result[0])
        lowest_distance = result[1]
        most_resemblence = result[0]
        print("RESEMBLANCE: " + most_resemblence + " WITH DISTANCE " + str(lowest_distance))
    
    return resultpaths




def getFeatures():
    df = pd.read_csv('features.csv')
    header = df.columns.tolist()
    data_array = df.to_numpy().tolist()
    return data_array

def exportBasicData(normalised):
    if(normalised == 'normalised'):
        db = 'normalisedDB/'
    else:
        db = 'db/'
    directories = get_immediate_subdirectories(db)
    alldata = []
    for dir in directories:
        files = get_all_files(db + dir + '/') 
        for file in files:
            mesh = Mesh(db + dir + '/' + file)
            data = mesh.getAnalyzedData()
            alldata.append(data)             
            
    return alldata

def getFolderFeatures(folderName):
    files = get_all_files('normalisedDB/' + folderName + '/')
    folderData = []
    for file in files:
        fEx = FeatureExtractor('normalisedDB/' + folderName + '/' + file)
        data = {dataTypes.CLASS.value : folderName, dataTypes.FILE.value : file}
        features = fEx.getFeatures()
        data.update(features)
        folderData.append(data)
    return folderData

def getAllFeatures():
    directories = get_immediate_subdirectories('normaliseddb/')
    DBfeatures = []
    for dir in directories:
        folderData = getFolderFeatures(dir)
        DBfeatures.append(folderData)
    
    return flatten_list(DBfeatures)

def normalizeDB(db):
    directories = get_immediate_subdirectories(db)
    DBdata = []
    for dir in directories:
        if(os.path.exists('normalisedDB/' + dir) == False):
            os.makedirs('normalisedDB/' + dir)
        folderData = normalizeFolder(dir)
        DBdata.append(folderData)
    print(DBdata)
    return flatten_list(DBdata)

def normalizeFolder(folderName):
    files = get_all_files('db/' + folderName + '/') 
    folderData = []
    for file in files:
        mesh = Mesh('db/' + folderName + '/' + file)
        data = mesh.normaliseMesh() 
        folderData.append(data)
    return folderData
                
def makeCSVfromArray(array, filename):
    df = pd.DataFrame(array, array[0].keys())
    df.to_csv(filename,mode="w")