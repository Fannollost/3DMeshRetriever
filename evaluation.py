import pandas as pd
from helper import get_immediate_subdirectories, get_all_files
from dataHandler import getDistanceToMesh

class Evaluation:
    

    def __init__(self,path):
        self.df = pd.read_csv(path)
        self.classAmount, self.objectAmount = self.getDatabaseStats()

    def getDatabaseStats(self):
        classAmount = len(get_immediate_subdirectories("normalisedDB"))
        objectAmount = 0

        for c in get_immediate_subdirectories("normalisedDB"):
            for f in get_all_files(c):
                objectAmount +=1 
        
        return classAmount, objectAmount

    def getObjectAmount(self, category):
        return len(self.df["Class" == category])

    def evaluateAccuracyOfDB(self, numberOfResults, classToEvaluate="all"):
        resultsArray = {}
        for i, row in self.df.iterrows():
            if(classToEvaluate != "all"):
                if(classToEvaluate != row["Class"]):
                    continue             
            distances = getDistanceToMesh(row["Class"], row["File"], self.getObjectAmount())
            resultsArray[row["Class"] + "/" + row["File"]] = distances

        truePositives = {}
        falsePositives = {}
        trueNegatives = {}
        falseNegatives = {}
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

        for i in self.df["Class"].unique():
            truePositives[i] = truePositives[i] / self.getObjectAmount()
            falsePositives[i] = falsePositives[i] / self.getObjectAmount()

        falseNegatives = falsePositives
        
        print("True")
        print(truePositives)
        print("False")
        print(falsePositives)