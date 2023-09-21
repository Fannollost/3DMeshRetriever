import os.path
import sys
#import pymeshlab as pymesh
from meshLoading import Mesh
from renderer import Renderer
import inputArguments as input
from dataHandler import dataExporter, exportBasicData, normalizeFolder, normalizeDB
path = "db/"
meshType = "Chess/"
meshId = "D01017.obj"

def main():
    args = sys.argv


    if(len(sys.argv) == 2):
        if(sys.argv[1] == input.ANALYZE):
            #do something
            print("TODO")

    if(len(sys.argv) == 3 or len(sys.argv) == 4):
        # TO RENDER, USE:                   python main.py render path_file
        if(sys.argv[1] == input.RENDER):
            r = Renderer()
            m = Mesh(sys.argv[2])
            r.renderMesh(m)
        # TO ANALYZE, USE:                  python main.py analyze path_file
        if(sys.argv[1] == input.ANALYZE):
            m = Mesh(sys.argv[2])
            data = m.getAnalyzedData()
            for d in data:
                print(d + " --> " + str(data[d]))
        # TO NORMALISE, USE:                python main.py normalise
        if(sys.argv[1] == input.NORMALISE):
            if(os.path.exists('normalisedDB') == False):
                os.mkdir('normalisedDB')
            if(sys.argv[2] != ''):
                if(os.path.exists('normalisedDB/' + sys.argv[2] + '/') == False):
                    os.makedirs('normalisedDB/' + sys.argv[2] + '/')
                normalizeFolder(sys.argv[2])
            else:
                normalizeDB()
        # TO EXPORT DATA, USE:              python main.py export basicdata
        # TO EXPORT NORMALISED DATA, USE:   python main.py export basicdata normalised
        if(sys.argv[1] == input.EXPORT):
            if(sys.argv[2] == input.BASICDATA):
                data = exportBasicData(sys.argv[3])
                exporter = dataExporter('basicdata.csv',data)
            
            

main()
