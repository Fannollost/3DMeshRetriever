import numpy as np
from matplotlib import pyplot as plt
import random
import pandas as pd
from collections import Counter

# Parameters
N = 100
no_bins = int(round(np.sqrt(N)))  # Recommended number of bins
# no_bins = <TRY_A_DIFFERENT_SETTING>
#print("Number of bins: ", no_bins)

# Generate random sample data
#data = np.array([random.randint(0, no_bins) for _ in range(N)])

df = pd.read_csv('basicdata.csv')
data = df['Amount of Faces']

# Compute histogram
counts, bins = np.histogram(data, bins=no_bins)

# Plot histogram
fig, ax = plt.subplots()
ax.hist(bins[:-1], bins, weights=counts)
ax.set_title("Faces of basic data")
ax.set_ylabel("Number of samples per bin")
ax.set_xlabel("Amount of Faces")

data = df['Amount of Vertices']
counts, bins = np.histogram(data, bins=no_bins)

# Plot histogram
fig2, ax = plt.subplots()
ax.hist(bins[:-1], bins, weights=counts)
ax.set_title("Vertices of basic data")
ax.set_ylabel("Number of samples per bin")
ax.set_xlabel("Amount of Vertices")

# Plot bar
fig3, ax = plt.subplots()
ax.set_title("Classes of basic data")
ax.set_ylabel("Number of samples per bin")
ax.set_xlabel("Classes")
data = df['Class'].value_counts().plot(kind='bar')

plt.show()
