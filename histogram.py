import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import json
import seaborn as sns
from helper import getEveryElementFromEveryList
import ast

# Parameters
#N = 100
N = 2400
#no_bins = int(round(np.sqrt(N)))  # Recommended number of bins
no_bins = 30

DescriptorName = ['A3', 'D1', 'D2', 'D3', 'D4']

class Graph():
    def getDescriptorList(self):
        descriptors = []
        for j in ['A3','D1','D2','D3','D4']:
            descriptor = []
            for i in range(50):
                descriptor.append(j + "_" + str(i))
            descriptors.append(descriptor)
        return descriptors

    def getHisto(self, csv, data, title):
        df = pd.read_csv(csv)
        db_data = df[data]

        # Compute histogram
        counts, bins = np.histogram(db_data, bins=no_bins)
        #counts, bins = np.histogram(db_data, bins=no_bins, range=[8000,12000])
        #print(counts)
        #print(bins)

        # Plot histogram
        fig, ax = plt.subplots()
        ax.hist(bins[:-1], bins=no_bins, weights=counts)
        #ax.hist(bins[:-1], weights=counts, range=[-0.1, 2])
        #ax.hist(bins[:-1], bins, weights=counts, range=[0, 12000])
        ax.set_title(title + ' - New database')
        ax.set_ylabel("Number of samples per bin")
        ax.set_xlabel(data)
    
    def getLinePlotDescriptors(self, csv):
        df = pd.read_csv(csv)
        #print(len(df['Class'].unique()))
        height = 7
        width = 9
        DescriptorList = self.getDescriptorList()
        #print(DescriptorList)
        for i in range(0, len(DescriptorList)):
            # Create subplots
            figure, axis = plt.subplots(height,width)
            count = 0

            # Retrieve descriptor name and columns
            descriptorColumns = DescriptorList[i]
            currentName = DescriptorName[i]
            # Retrieve the data for each class
            for className in df['Class'].unique():
                classData = df.loc[df['Class'] == className]
                #currentData = classData[['A3_0','A3_1','A3_2','A3_3','A3_4','A3_5','A3_6','A3_7']].T - Example
                currentData = classData[descriptorColumns].T

                # Get the coordinates of the subplot and put the data in it
                x = int((count / width))
                y = count % width
                axis[x,y].plot(currentData, label=className)
                axis[x,y].set_title(currentName + ' ' + className)
                count = count + 1

        plt.show()


    def getEvaluation(self,csv,data, title,subdata = ''):
        df = pd.read_csv(csv)
        labels = list(df['Class'])
        db_data = df[data]
        values = []
        if(subdata != ''): 
            for d in db_data:
                d = d.strip()
                d = d.replace("'", "\"")
                data = json.loads(d)
                value = data.get('Average', None)
                values.append(value)
        # Compute histogram
        sorted_lab_val = sorted(list(zip(labels,values)), key = lambda x: x[1])
        sorted_labels, sorted_values = zip(*sorted_lab_val)

        plt.bar(sorted_labels,sorted_values)
        #for i, value in enumerate(sorted_values):
        #    plt.text(i, value, str(value), ha='center', va='bottom')
        plt.xticks(rotation=90)
        plt.xlabel('Class')
        plt.ylabel('Accuracy')
        plt.title('Average Accuracy per class')
        #counts, bins = np.histogram(db_data, bins=no_bins, range=[8000,12000])
        #print(counts)
        #print(bins)


    def getBar(self, csv, data, title):
        df = pd.read_csv(csv)

        fig, ax = plt.subplots()
        ax.set_title(title)
        ax.set_ylabel("Number of samples per bin")
        ax.set_xlabel(data)
        data = df[data].value_counts().plot(kind='bar')

    def getBoxplot(self, data, title):
        df1 = pd.read_csv('basicdata.csv')
        data_1 = df1[data]
        df2 = pd.read_csv('normalisedDBData.csv')
        data_2 = df2[data]
        data = [data_1, data_2]

        fig, ax = plt.subplots()
        ax.set_title(title)
        
        bp = ax.boxplot(data)

    def getlinePlot(self, data, title):
        #df1 = pd.read_csv('basicdata.csv')
        df1 = pd.read_csv('features.csv')
        
        #df1 = pd.read_csv('normalisedDBdata.csv')

        for cls in df1['Class'].unique():
            data_1 = df1.loc[df1['Class'] == cls]
            print(df1.loc[df1['Class'] == cls])
            data_1 = data_1[data]
            print(data_1)
            #data_2 = df2[data]
            #plt.plot(data_1)
            plt.plot(data_1, label=cls)
            #plt.plot(data_2, label=title + ' normalised')
            plt.xlabel("Model nr.")
            plt.ylabel("Value of data")
            plt.legend(loc="best")
            plt.show()

    def getLinePlotDescriptor(self, data, bins = list(range(1,9))):
        
        plt.plot(data)

        pass

    def getViolinPlot(self,data, datatype):
        df = pd.read_csv(data)
        data_1 = df[datatype].tolist()
        values = []
        for value in data_1:
            value = ast.literal_eval(value)
            values.append([value[0][0],
            value[1][1],
            value[2][2]])


        df = pd.DataFrame(values, columns=['X', 'Y', 'Z'])
        sns.set(style="whitegrid")
        sns.violinplot(data=df,  cut =0)

    def showPlots(self):
        plt.show()
