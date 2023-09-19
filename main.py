import os.path
import sys
#import pymeshlab as pymesh
from meshLoading import Mesh
from renderer import Renderer
import inputArguments as input
from dataExporter import dataExporter
path = "db/"
meshType = "Chess/"
meshId = "D01017.obj"

def main():
    args = sys.argv

    if(len(sys.argv) == 2):
        if(sys.argv[1] == input.ANALYZE):
            #do something
            print("TODO")

        if(sys.argv[1] == input.NORMALIZE):
            #do something 
            print("TODO")

        if(sys.argv[1] == input.EXPORT):
            exporter = dataExporter()
            exporter.exportData()

    if(len(sys.argv) == 3):
        if(sys.argv[1] == input.RENDER):
            r = Renderer()
            m = Mesh(sys.argv[2])
            r.renderMesh(m)
        if(sys.argv[1] == input.ANALYZE):
            m = Mesh(sys.argv[2])
            data = m.getAnalyzedData()
            for d in data:
                print(d + " --> " + str(data[d]))
            

main()
