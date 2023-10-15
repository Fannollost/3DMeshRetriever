import os
import csv
from meshLoading import Mesh
from meshDataTypes import dataTypes
import pandas as pd
from featureExtractor import FeatureExtractor
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from distance import euclidianDistance


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

def getDistances():
    DB = getFeatures()
    res = []
    i =0
    for obj1 in DB:
        row = {}
        row['OBJ1']=obj1["Class"]+'/'+obj1["File"]
        for obj2 in DB:
            row[obj2["Class"]+'/'+obj2["File"]] = euclidianDistance(obj1, obj2)[0]
        res.append(row)
        i+=1
        if i%20==0 : print(str(int(i/380*100))+" %")
    makeCSVfromArray(res, 'distanceEucl.csv',)
    return res

def getFeatures():
    df = pd.read_csv('featuresnormalised.csv')
    databasefeatures = []
    line = {}
    for i, row in df.iterrows():
        for colName in df.columns:
            line[colName] = row[colName]
        if len(line)>0: databasefeatures.append(line)
    return databasefeatures

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
        folderData = getFolderFeatures()
        DBfeatures.append(folderData)
    return DBfeatures

def normalizeDB():
    directories = get_immediate_subdirectories('db/')
    DBdata = []
    for dir in directories:
        if(os.path.exists('normalisedDB/' + dir) == False):
            os.makedirs('normalisedDB/' + dir)
        folderData = normalizeFolder(dir)
        DBdata.append(folderData)
    return DBdata

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

def get_immediate_subdirectories(dir):
    return [name for name in os.listdir(dir) if os.path.isdir(os.path.join(dir,name))]

def get_all_files(dir):
    return  [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]