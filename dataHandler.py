import os
import csv
from meshLoading import Mesh
from meshDataTypes import dataTypes
import pandas as pd
from featureExtractor import FeatureExtractor
from sklearn.preprocessing import MinMaxScaler
import numpy as np


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

    for column in df.columns[2:]:
        if df[column].dtype in [int, float]:
            df[column] = scaler.fit_transform(df[[column]])

    df.to_csv(toSave, index=False)

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
                

def get_immediate_subdirectories(dir):
    return [name for name in os.listdir(dir) if os.path.isdir(os.path.join(dir,name))]

def get_all_files(dir):
    return  [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]