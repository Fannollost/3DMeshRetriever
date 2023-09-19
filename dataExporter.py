import os
import csv
from meshLoading import Mesh
from meshDataTypes import dataTypes


class dataExporter:

    def __init__(self):
        self.path = 'data.csv'
        self.file = open(self.path, 'w')
        self.writer = csv.writer(self.file)

    def exportData(self):
        self.writer.writerow(dataTypes.CLASS.value + ',' + 
                             dataTypes.AMOUNT_FACES.value + ',' + 
                             dataTypes.AMOUNT_VERTICES.value + ',' + 
                             dataTypes.BARY_CENTER.value + ',' + 
                             dataTypes.SIZE.value + ',' + 
                             dataTypes.MAX_SIZE.value)
        
        directories = os.scandir('db/')
        print(directories)
        for directory in directories:
            files = os.listdir('db/' + directory + '/')   
            for file in directory:
                mesh = Mesh('db/' + directory + '/' + file)
                data = mesh.getAnalyzedData()
                self.writer.writerow(data)
        self.file.close()
        print('EXPORTING DATA SUCCESFULL')