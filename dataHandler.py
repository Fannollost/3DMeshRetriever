import os
import csv
from meshLoading import Mesh
from meshDataTypes import dataTypes
import pandas as pd

class dataExporter:

    def __init__(self, fileName, data):
        self.path = fileName
        self.file = open(self.path, 'w', newline='')
        self.writer = csv.writer(self.file)
        self.writer.writerow(data[0].keys())
        for d in range(len(data)):
            self.writer.writerow(data[d].values())


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

def normalizeDB():
    directories = get_immediate_subdirectories('db/')
    for dir in directories:
        if(os.path.exists('normalisedDB/' + dir) == False):
            os.makedirs('normalisedDB/' + dir)
        normalizeFolder(dir)

def normalizeFolder(folderName):
    files = get_all_files('db/' + folderName + '/') 
    for file in files:
        mesh = Mesh('db/' + folderName + '/' + file)
        mesh.normaliseMesh()             

def get_immediate_subdirectories(dir):
    return [name for name in os.listdir(dir) if os.path.isdir(os.path.join(dir,name))]

def get_all_files(dir):
    return  [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]