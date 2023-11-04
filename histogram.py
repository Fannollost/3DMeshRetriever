import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

# Parameters
#N = 100
N = 2400
#no_bins = int(round(np.sqrt(N)))  # Recommended number of bins
no_bins = 30

DescriptorName = ['A3', 'D1', 'D2', 'D3', 'D4']

DescriptorList = [
    ['A3_0','A3_1','A3_2','A3_3','A3_4','A3_5','A3_6','A3_7'],
    ['D1_0','D1_1','D1_2','D1_3','D1_4','D1_5','D1_6','D1_7'],
    ['D2_0','D2_1','D2_2','D2_3','D2_4','D2_5','D2_6','D2_7'],
    ['D3_0','D3_1','D3_2','D3_3','D3_4','D3_5','D3_6','D3_7'],
    ['D4_0','D4_1','D4_2','D4_3','D4_4','D4_5','D4_6','D4_7']
]

class Graph():
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
        height = 2
        width = 4

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
                x = int(count / width)
                y = count % width
                axis[x,y].plot(currentData, label=className)
                axis[x,y].set_title(currentName + ' descriptor - ' + className)
                count = count + 1

        plt.show()


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
        #df1 = pd.read_csv('features.csv')
        df1 = pd.read_csv('normalisedDBdata.csv')

        data_1 = df1[data]
        #data_2 = df2[data]
        #plt.plot(data_1)
        plt.plot(data_1, label=title)
        plt.plot(data_2, label=title + ' normalised')
        plt.xlabel("Model nr.")
        plt.ylabel("Value of data")
        plt.legend(loc="best")

    def getLinePlotDescriptor(self, data, bins = list(range(1,9))):
        
        plt.plot(data)

        pass

    def showPlots(self):
        plt.show()
