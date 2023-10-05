import os.path
import sys
#import pymeshlab as pymesh
from meshLoading import Mesh
from renderer import Renderer
import inputArguments as input
from dataHandler import dataExporter, exportBasicData, normalizeFolder, normalizeDB
from histogram import Graph
from featureExtractor import FeatureExtractor

path = "db/"
meshType = "Chess/"
meshId = "D01017.obj"

def main():
    args = sys.argv


    if(len(sys.argv) == 2):
        if(sys.argv[1] == input.ANALYZE):
            #do something
            print("TODO")

    if(len(sys.argv) == 5):
        # TO RENDER WITH WIREFRAME, USE:    python main.py render path_file wireframe
        if(sys.argv[1] == input.RENDER and sys.argv[4] == 'wireframe'):
            r = Renderer()
            r.renderWireFrame(sys.argv[3])

    if(len(sys.argv) == 3 or len(sys.argv) == 4):
        # TO RENDER, USE:                   python main.py render path_file
        if(sys.argv[1] == input.RENDER):
            r = Renderer()
            if(len(sys.argv) == 3):
                m = Mesh(sys.argv[2])
                r.renderMesh(m)
            else:                          #python main.py render path_file (any character)
                r.renderWireFrame(sys.argv[2])
                
        # TO ANALYZE, USE:                  python main.py analyze path_file
        if(sys.argv[1] == input.ANALYZE):
            m = Mesh(sys.argv[2])
            data = m.getAnalyzedData()
            for d in data:
                print(d + " --> " + str(data[d]))
        # TO NORMALISE, USE:                python main.py normalise
        # TO NORMALISE EVERYTHING, USE      python main.py normalise all
        if(sys.argv[1] == input.NORMALISE):
            if(os.path.exists('normalisedDB') == False):
                os.mkdir('normalisedDB')
            if(sys.argv[2] != 'all'):
                print(sys.argv[2])
                if(os.path.exists('normalisedDB/' + sys.argv[2] + '/') == False):
                    os.makedirs('normalisedDB/' + sys.argv[2] + '/')
                folderData = normalizeFolder(sys.argv[2])
                dataExporter('normalisedData.csv', folderData)
            else:
                dbData = normalizeDB()
                dataExporter('normalisedDBData.csv', dbData)
        # TO EXPORT DATA, USE:              python main.py export basicdata
        # TO EXPORT NORMALISED DATA, USE:   python main.py export basicdata normalised
        if(sys.argv[1] == input.EXPORT):
            if(sys.argv[2] == input.BASICDATA):
                data = exportBasicData('false')
                exporter = dataExporter('basicdata.csv',data)
            if(sys.argv[2] == input.NORMALISE):
                data = exportBasicData('normalised')
                exporter = dataExporter('normalisedDBData.csv',data)
        #FOR FEATURES, USE:                 python main.py features <path to mesh> 
        if(sys.argv[1] == input.FEATURE):
            if(sys.argv[2] == ''):
                print("PUT VALID MESH PATH")

            fEx = FeatureExtractor(sys.argv[2])
            features = fEx.getFeatures()
            print(features)
            dataExporter('features.csv', features)


    if(sys.argv[1] == input.GRAPH):
        h = Graph()
        #h.getHisto('basicdata.csv','Barycenter distance to origin','basic data')
        # h.getHisto('normalisedDBData.csv','Barycenter distance to origin', 'normalised data')
        #h.getBoxplot('Barycenter distance to origin', 'Barycenter distance')
        #h.getHisto('basicdata.csv', 'Amount of Vertices', 'Amount of Vertices')
        #h.getHisto('basicdata.csv', 'Amount of Faces', 'Amount of Faces')
        #h.getHisto('basicdata.csv', 'Biggest axis boundingbox', 'Biggest axis boundingbox')
        #h.getHisto('normalisedDBData.csv', 'Amount of Vertices', 'Amount of Vertices')
        #h.getHisto('normalisedDBData.csv', 'Amount of Faces', 'Amount of Faces')
        h.getHisto('basicdata.csv', 'Barycenter distance to origin', 'Barycenter distance')
        #h.getlinePlot('Barycenter distance to origin', 'Barycenter distance')
        
        h.showPlots()
        h.getHisto('basicdata.csv', 'Biggest axis boundingbox', 'Biggest axis boundingbox')
        #h.getlinePlot('Biggest axis boundingbox', 'Biggest axis boundingbox')
        h.showPlots()
            

main()