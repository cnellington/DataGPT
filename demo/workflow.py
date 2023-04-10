
import pandas as pd
import matplotlib.pyplot as plt

# Reading the data
clinical_covariates = pd.read_csv('./data/clinical_covariates.csv', index_col=0)

# Grouping by disease_type and getting percentage of each race
df = clinical_covariates.groupby('disease_type').apply(lambda x: x['race'].value_counts(normalize=True) * 100)

# Flattening the table
df = df.unstack(level=-1)

# Plotting the data
ax = df.plot(kind='bar', stacked=True, figsize=(10,10))

# Setting the axes labels and title
ax.set_xlabel('Disease Type')
ax.set_ylabel('Percentage of Races')
ax.set_title('Percentage of Races by Disease Type')

# Saving the figure
plt.savefig('./figures/race_percentages.png')
