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
            for f in get_all_files("normalisedDB/" + c):
                objectAmount +=1 
        
        return classAmount, objectAmount

    def getObjectAmount(self, category):
        return len(self.df.loc[self.df["Class"] == category])

    def evaluateAccuracyOfDB(self, numberOfResults, classToEvaluate="all"):
        resultsArray = {}
        for i, row in self.df.iterrows():
            if(classToEvaluate != "all"):
                if(classToEvaluate != row["Class"]):
                    continue             
            distances = getDistanceToMesh(row["Class"], row["File"], self.getObjectAmount(row["Class"]))
            resultsArray[row["Class"] + "/" + row["File"]] = distances

        evaluation = []
        result = {}
        for result in resultsArray:
            truePositives = 0
            falsePositives = 0
            trueNegatives = 0
            falseNegatives = 0

            queryClass = result.split("/")[0]
            queryFile = result.split("/")[1]
            resultClasses = [r.split("/")[0] for r in resultsArray[result]]
            for r in resultClasses:
                if r == queryClass:
                    truePositives += 1
                else:
                    falsePositives += 1
            trueNegatives = self.objectAmount - falsePositives - self.getObjectAmount(queryClass)
            falseNegatives = self.getObjectAmount(queryClass) - truePositives
            print("TRUE: " + str(truePositives + trueNegatives) )
            print("TOT" + str(self.objectAmount))
            result = {
                "class": queryClass,
                "file": queryFile,
                "truePositives": truePositives,
                "falsePositives": falsePositives,
                "trueNegatives": trueNegatives,
                "falseNegatives": falseNegatives,
                "Specificity": trueNegatives / (falsePositives + trueNegatives),
                "Sensitivity": truePositives / (truePositives + falseNegatives),
                "Precision" : truePositives / (truePositives + falsePositives),
                "Accuracy" : (truePositives + trueNegatives) / self.objectAmount
            }
            evaluation.append(result)

        #for i in self.df["Class"].unique():
        #    #truePositives[i] = truePositives[i] / self.getObjectAmount(i)
        #    #falsePositives[i] = falsePositives[i] / self.getObjectAmount(i)
        #    trueNegatives[i] = self.objectAmount * self.objectAmount - falsePositives[i] - self.getObjectAmount(i) * self.getObjectAmount(i)
        #    falseNegatives[i] =  self.getObjectAmount(i) * self.getObjectAmount(i) - truePositives[i]
        
        return evaluation

    def getOverallStats(self, evaluation):
        overall = {}
        for m in ['Specificity', 'Sensitivity', 'Precision', 'Accuracy']:
            average, median, minimum, maximum = self.getAllStats(m,evaluation)
            overall[m + "/average"] = average
            overall[m + "/median"] = median
            overall[m + "/minimum"] = minimum
            overall[m + "/maximum"] = maximum
        return overall


    def getAllStats(self,metric, dict):
        average = 0
        median = []
        minimum = 100
        maximum = 0
        for c in dict:
            average += c[metric]["Average"]
            median.append(c[metric]["Median"])
            minimum = min(minimum, c[metric]["Min"])
            maximum = max(maximum, c[metric]["Average"])
        average /= len(median)
        median = median[int(len(median) / 2)]
        return average, median, minimum, maximum
            
    def getStatsPerClass(self, evaluation):
        classEvaluation = []
        classes = []
        for c in evaluation:
            if c["class"] not in classes:
                classes.append(c["class"])
            
        for c in classes:
            classSpecific = [item for item in evaluation if item.get("class") == c]
            print(classSpecific)
            specificity = self.calculateMetric("Specificity", classSpecific)
            sensitivity = self.calculateMetric("Sensitivity", classSpecific)
            precision = self.calculateMetric("Precision", classSpecific)
            accuracy = self.calculateMetric("Accuracy", classSpecific)
            result = {
                "Class" : c,
                "Specificity" : specificity,
                "Sensitivity" : sensitivity,
                "Precision" : precision,
                "Accuracy" : accuracy
            }
            classEvaluation.append(result)
        return classEvaluation
    
    def calculateMetric(self, metric, dict):
        metric = {
                "Average" : sum([item.get(metric) for item in dict]) / len(dict),
                "Median" : [item.get(metric) for item in dict][int(len(dict) / 2)],
                "Min" : min([item.get(metric) for item in dict]),
                "Max" : max([item.get(metric) for item in dict])
            }
        return metric