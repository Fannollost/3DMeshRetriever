import pandas as pd
from helper import get_immediate_subdirectories
from dataHandler import getDistanceToMesh

class Evaluation:
    
    def __init__(self,path):
        self.df = pd.read_csv(path)
    
    def evaluateAccuracyOfDB(self, numberOfResults):
        resultsArray = {}
        for i, row in self.df.iterrows():
            distances = getDistanceToMesh(row["Class"], row["File"],numberOfResults)
            resultsArray[row["Class"] + "/" + row["File"]] = distances

        truePositives = {}
        falsePositives = {}
        for result in resultsArray:
            queryClass = result.split("/")[0]
            resultClasses = [r.split("/")[0] for r in resultsArray[result]]
            truePositives[queryClass] = 0
            falsePositives[queryClass] = 0
            for r in resultClasses:
                if r == queryClass:
                    truePositives[queryClass] += 1
                else:
                    falsePositives[queryClass] += 1
        
        print("True")
        print(truePositives)
        print("False")
        print(falsePositives)