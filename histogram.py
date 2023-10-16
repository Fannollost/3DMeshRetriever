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
        print(counts)
        print(bins)

        # Plot histogram
        fig, ax = plt.subplots()
        ax.hist(bins[:-1], bins=no_bins, weights=counts)
        #ax.hist(bins[:-1], weights=counts, range=[-0.1, 2])
        #ax.hist(bins[:-1], bins, weights=counts, range=[0, 12000])
        ax.set_title(title + ' - New database')
        ax.set_ylabel("Number of samples per bin")
        ax.set_xlabel(data)

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
        plt.xlabel("Model nr.")
        plt.ylabel("Value of data")
        plt.legend(loc="best")

    def showPlots(self):
        plt.show()
