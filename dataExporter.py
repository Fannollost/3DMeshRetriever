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



def exportBasicData():
    directories = get_immediate_subdirectories('db/')
    alldata = []
    files = get_all_files('db/' + 'bed' + '/') 
    for file in files:
        mesh = Mesh('db/' + 'bed' + '/' + file)
        data = mesh.getAnalyzedData()
        alldata.append(data)             
            
    return alldata

def get_immediate_subdirectories(dir):
    return [name for name in os.listdir(dir) if os.path.isdir(os.path.join(dir,name))]

def get_all_files(dir):
    return  [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]