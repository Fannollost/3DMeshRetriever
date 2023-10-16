import os.path
import sys
#import pymeshlab as pymesh
from meshLoading import Mesh
from renderer import Renderer
import inputArguments as input
from dataHandler import dataExporter, exportBasicData, normalizeFolder, normalizeDB, getAllFeatures, getFolderFeatures,normaliseFeatures, getDistances
from histogram import Graph
import paths
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

    database = ""
    if db == 'mini':
        database = input.MINIDB
    elif db == 'micro':
        database = input.MICRODB
    elif db == 'db':
        database = input.DB
    
    if(os.path.exists('normalisedDB') == False):
        os.mkdir('normalisedDB')
    if(folder != 'all'):
        print(folder)
        if(os.path.exists('normalisedDB/' + folder + '/') == False):
            os.makedirs('normalisedDB/' + folder + '/')
        folderData = normalizeFolder(folder)
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

#------------------------------------------------------------------------------------
#FOR NORMALISE FEATURES USE:        python main.py query
#------------------------------------------------------------------------------------
def NormaliseFeatures():
    normaliseFeatures(paths.featuresCSV, 'featuresnormalised.csv')

#------------------------------------------------------------------------------------
#FOR DISTANCE MATRIX USE:           python main.py distance
#------------------------------------------------------------------------------------
def DistanceMatrix():
    normaliseFeatures(paths.featuresCSV, 'featuresnormalised.csv')
    getDistances()


#------------------------------------------------------------------------------------
#FOR GRAPHS, USE:                   python main.py graphs
#------------------------------------------------------------------------------------
def Graph():
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
    h.showPlots()

def main():
    args = sys.argv

    #FOR NORMALISE FEATURES USE:        python main.py query
    if(sys.argv[1] == input.QUERY):
        NormaliseFeatures()
    
    #FOR DISTANCE MATRIX USE:           python main.py distance
    if(sys.argv[1] == input.DISTANCE):
        DistanceMatrix()
        
    if(len(sys.argv) == 3 or len(sys.argv) == 4 or len(sys.argv) == 5):
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
            Export(sys.arv[2])

        #FOR FEATURES, USE:                 python main.py features <folder> 
        #FOR ALL FEATURES, USE:             python main.py features <database> all
        if(sys.argv[1] == input.FEATURE):
           Feature(sys.argv[2])

        # TO RENDER WITH WIREFRAME, USE:    python main.py render path_file wireframe
        if(sys.argv[1] == input.RENDER and sys.argv[4] == 'wireframe'):
            r = Renderer()
            r.renderWireFrame(sys.argv[3])

    if(sys.argv[1] == input.GRAPH):
        Graph()
        
main()