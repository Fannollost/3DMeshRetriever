import os.path
import sys
#import pymeshlab as pymesh
from meshLoading import Mesh
from renderer import Renderer
from helper import discard_every_x_from_every_list, getEveryElementFromEveryList, get_1_from_list
import inputArguments as input
from dataHandler import dataExporter, exportBasicData, normalizeFolder, normalizeDB, getAllFeatures, getFolderFeatures,normaliseFeatures, getAllDistances, getDistanceToMesh, getFeatures
from histogram import Graph
import paths
from tsne import tsne, getColor
import pylab
import mplcursors
from shapeDescriptors import weight
import numpy as np
from evaluation import Evaluation
path = "db/"
meshType = "Chess/"
meshId = "D01017.obj"

#-------------------------------------------------------------------------------------
# TO RENDER, USE:                   python main.py render path_file
#-------------------------------------------------------------------------------------
def Render(length, meshPath):
    r = Renderer()
    if(length == 3):
        m = Mesh(meshPath)
        r.renderMesh(m)
    else:                          #python main.py render path_file (any character)
        r.renderWireFrame(meshPath)

#------------------------------------------------------------------------------------
# TO ANALYZE, USE:                  python main.py analyze path_file
#------------------------------------------------------------------------------------
def Analyze(meshPath):
    m = Mesh(meshPath)
    data = m.getAnalyzedData()
    for d in data:
        print(d + " --> " + str(data[d]))

#------------------------------------------------------------------------------------
# TO NORMALISE, USE:                python main.py normalise <database> <folder>
# TO NORMALISE EVERYTHING, USE      python main.py normalise <database> all
#------------------------------------------------------------------------------------
def Normalise(folder, db = ''):
    print(folder)
    database = ""
    if db == 'mini':
        database = input.MINIDB
    elif db == 'micro':
        database = input.MICRODB
    elif db == 'db':
        database = input.DB
    elif db == 'macro':
        database = input.MACRO
    
    if(os.path.exists('normalisedDB') == False):
        os.mkdir('normalisedDB')
    if(folder != 'all'):
        print(folder)
        if(os.path.exists('normalisedDB/' + folder + '/') == False):
            os.makedirs('normalisedDB/' + folder + '/')
        folderData = normalizeFolder(folder, database)
        dataExporter('normalisedData.csv', folderData)
    else:
        dbData = normalizeDB(database)
        dataExporter(paths.normalisedDBCSV, dbData)

#------------------------------------------------------------------------------------
# TO EXPORT DATA, USE:              python main.py export basicdata
# TO EXPORT NORMALISED DATA, USE:   python main.py export basicdata normalised
#------------------------------------------------------------------------------------
def Export(meshPath):
    if(meshPath == input.BASICDATA):
        data = exportBasicData('false')
        exporter = dataExporter('basicdata.csv',data)
    if(meshPath == input.NORMALISE):
        data = exportBasicData('normalised')
        exporter = dataExporter(paths.normalisedDBCSV,data)

#------------------------------------------------------------------------------------
#FOR FEATURES, USE:                 python main.py features <folder> 
#FOR ALL FEATURES, USE:             python main.py features <database> <all>
#------------------------------------------------------------------------------------
def Feature(folder):
    features = []
    if(folder == 'all'):
        features = getAllFeatures()
    elif(folder != ''):
        features = getFolderFeatures(folder)
    print(features)
    dataExporter(paths.featuresCSV, features)
    #normaliseFeatures(paths.featuresCSV, 'featuresnormalised.csv')


#------------------------------------------------------------------------------------
#FOR NORMALISE FEATURES USE:        python main.py query <folder> <object>  
#------------------------------------------------------------------------------------
def QueryMesh(folder, mesh, nrOfResults):
    normaliseFeatures(paths.featuresCSV, 'featuresnormalised.csv')
    getDistanceToMesh(folder, mesh, nrOfResults)

#------------------------------------------------------------------------------------
#FOR DISTANCE MATRIX USE:           python main.py distance
#------------------------------------------------------------------------------------
def DistanceMatrix():
    normaliseFeatures(paths.featuresCSV, 'featuresnormalised.csv')
    getAllDistances()

#------------------------------------------------------------------------------------
#FOR VISUALIZATION USE:             python main.py tsne
#------------------------------------------------------------------------------------
def VisualizeFeatureSpace():
    normaliseFeatures(paths.featuresCSV, 'featuresnormalised.csv')
    features, headers = getFeatures()
    allClasses = getEveryElementFromEveryList(0, features)
    allModels = getEveryElementFromEveryList(1,features)
    labels = []
    for cIdx in range(len(allClasses)):
        labels.append(allClasses[cIdx] + "-" + allModels[cIdx])

    classes = get_1_from_list(allClasses)
    colors = getColor(classes)
    allColors = [ colors[c] for c in allClasses]
    #colors = [allClassesfor color in colors] allClasses
    features = discard_every_x_from_every_list(2, features)
    
    headers = headers[2:]
    weightedFeatures = []
    for feat in features:
        f = []
        for head in range(len(headers[2:])):
            h = headers[head] 
            if(h[:2] == "A3" or h[:2] == "D1" or h[:2] == "D2" or h[:2] == "D3" or h[:2] == "D4"):
                h = h[:2]
            f.append(feat[head] * weight[h])
        weightedFeatures.append(f)
        
    Y = tsne(np.array(weightedFeatures),2,47,15)
    f = pylab.scatter(Y[:, 0], Y[:, 1], 20,allColors)
    cursor = mplcursors.cursor(f)
    cursor.connect("add", lambda sel: sel.annotation.set_text(labels[sel.index]))
    pylab.show()

def EvaluateCBRS(k_nearest):
    normaliseFeatures(paths.featuresCSV, 'featuresnormalised.csv')
    eval = Evaluation("featuresnormalised.csv")
    eval.evaluateAccuracyOfDB(k_nearest)

#------------------------------------------------------------------------------------
#FOR GRAPHS, USE:                   python main.py graphs
#------------------------------------------------------------------------------------
def Graphs():
    h = Graph()
    #h.getHisto('basicdata.csv','Barycenter distance to origin','basic data')
    # h.getHisto(paths.normalisedDBCSV,'Barycenter distance to origin', 'normalised data')
    #h.getBoxplot('Barycenter distance to origin', 'Barycenter distance')
    #h.getHisto('basicdata.csv', 'Amount of Vertices', 'Amount of Vertices')
    #h.getHisto('basicdata.csv', 'Amount of Faces', 'Amount of Faces')
    #h.getHisto('basicdata.csv', 'Biggest axis boundingbox', 'Biggest axis boundingbox')
    #h.getHisto(paths.normalisedDBCSV, 'Amount of Vertices', 'Amount of Vertices')
    #h.getHisto(paths.normalisedDBCSV, 'Amount of Faces', 'Amount of Faces')
    h.getHisto('basicdata.csv', 'Barycenter distance to origin', 'Barycenter distance')
    #h.getlinePlot('Barycenter distance to origin', 'Barycenter distance')
    
    h.showPlots()
    h.getHisto('basicdata.csv', 'Biggest axis boundingbox', 'Biggest axis boundingbox')
    #h.getlinePlot('Biggest axis boundingbox', 'Biggest axis boundingbox')
    #h.getlinePlot("Barycenter distance to origin", "Barycenter distance to origin")
    h.showPlots()
    #h.getHisto('basicdata.csv', 'Biggest axis boundingbox', 'Biggest axis boundingbox')
    #h.getlinePlot('Biggest axis boundingbox', 'Biggest axis boundingbox')

def main():
    args = sys.argv
    
    #FOR DISTANCE MATRIX USE:           python main.py distance
    if(sys.argv[1] == input.DISTANCE):
        DistanceMatrix()

    #FOR VISUALIZATION USE:             python main.py tsne
    if(sys.argv[1] == input.TSNE):
        VisualizeFeatureSpace()

    if(sys.argv[1] == input.GRAPH):
        Graphs()

    if(len(sys.argv) == 3 or len(sys.argv) == 4 or len(sys.argv) == 5 or len(sys.argv)==6):
        # TO RENDER, USE:                   python main.py render path_file
        if(sys.argv[1] == input.RENDER):
            Render(len(sys.argv),sys.argv[2])
                
        # TO ANALYZE, USE:                  python main.py analyze path_file
        if(sys.argv[1] == input.ANALYZE):
            Analyze(sys.argv[2])

        # TO NORMALISE, USE:                python main.py normalise <database> <folder>
        # TO NORMALISE EVERYTHING, USE      python main.py normalise <database> all
        if(sys.argv[1] == input.NORMALISE):
            Normalise(sys.argv[3], sys.argv[2])

        # TO EXPORT DATA, USE:              python main.py export basicdata
        # TO EXPORT NORMALISED DATA, USE:   python main.py export basicdata normalised
        if(sys.argv[1] == input.EXPORT):
            Export(sys.argv[2])

        #FOR FEATURES, USE:                 python main.py features <folder> 
        #FOR ALL FEATURES, USE:             python main.py features <database> all
        if(sys.argv[1] == input.FEATURE):
           Feature(sys.argv[2])

        # TO RENDER WITH WIREFRAME, USE:    python main.py render path_file wireframe
        if(sys.argv[1] == input.RENDER and sys.argv[4] == 'wireframe'):
            r = Renderer()
            r.renderWireFrame(sys.argv[3])

        #FOR NORMALISE FEATURES USE:        python main.py query <folder> <file> <resultsWanted>
        if(sys.argv[1] == input.QUERY):
            QueryMesh(sys.argv[2], sys.argv[3], sys.argv[4])

        if(sys.argv[1] == input.EVALUATE):
            print("FF")
            EvaluateCBRS(sys.argv[2])

main()
        