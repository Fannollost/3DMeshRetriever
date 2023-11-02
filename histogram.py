import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

# Parameters
#N = 100
N = 2400
#no_bins = int(round(np.sqrt(N)))  # Recommended number of bins
no_bins = 30

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

        for className in df['Class'].unique():
            classData = df.loc[df['Class'] == className]
            SurfaceAreaData = classData[['A3_0','A3_1','A3_2','A3_3','A3_4','A3_5','A3_6','A3_7']]
            print(SurfaceAreaData)
            #counts, bins = np.histogram(SurfaceAreaData, bins=10)
            plt.plot(SurfaceAreaData, label=className)
            plt.show()
            
            # fig, ax = plt.subplots()
            # ax.hist(bins[:-1], bins=10, weights=counts)
            # ax.set_title("Surface Area for: " + className)
            # ax.set_ylabel("Number of samples per bin")
            # ax.set_xlabel(className + " values")

        # for name in df.columns:
        #     print(name)
        

        # counts, bins = np.histogram(db_data, bins=no_bins)
        # # Plot histogram
        # fig, ax = plt.subplots()
        # ax.hist(bins[:-1], bins=no_bins, weights=counts)
        # #ax.hist(bins[:-1], weights=counts, range=[-0.1, 2])
        # #ax.hist(bins[:-1], bins, weights=counts, range=[0, 12000])
        # ax.set_title(title + ' - New database')
        # ax.set_ylabel("Number of samples per bin")
        # ax.set_xlabel(data)

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
        df1 = pd.read_csv('basicdata.csv')
        data_1 = df1[data]
        df2 = pd.read_csv('normalisedDBData.csv')
        data_2 = df2[data]
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
