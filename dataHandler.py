import os
import csv
from meshLoading import Mesh
from meshDataTypes import dataTypes
import pandas as pd
from featureExtractor import FeatureExtractor
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from distance import get_cosine_distance
import paths
from helper import flatten_list, get_all_files, get_immediate_subdirectories

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
    scaler = MinMaxScaler()

    group_size = 8
    column_groups = [df.columns[-40 + i:-40 + i + group_size] for i in range(0, 40, group_size)]

    for group in column_groups:
        for column in group[2:]:
            if df[column].dtype in [int, float]:
                df[column] = scaler.fit_transform(df[[column]])

    df.to_csv(toSave, index=False)

def getAllDistances():
    DB = getFeatures()
    res = []
    i = 0
    
    distances = []
    for a in range(len(DB)):
        for b in range(i + 1,len(DB)):
            obj_a = DB[a]
            obj_b = DB[b]
            distance = get_cosine_distance(obj_a[2:], obj_b[2:])
            name_a = obj_a[0] + "/" + obj_a[1]
            name_b = obj_b[0] + "/" + obj_b[1]
            distances.append((name_a,name_b,distance))
    #makeCSVfromArray(res, 'distanceEucl.csv',)
    print(distances)
    return distances

def getFeatures():
    df = pd.read_csv('featuresnormalised.csv')
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
        folderData = getFolderFeatures('normaliseddb/' + dir)
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