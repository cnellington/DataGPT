# DataGPT
A wrapper for the prompt-debug-plot workflow of data science with ChatGPT.

## Starting
Install any plotting libraries you want to use, as well as the openai API and pandas.
```
datagpt = DataGPT(data_dir='<dir containing one or several .csvs>', figure_dir='<dir to save resulting plots/tables>')
datagpt.run()
```

## Workflow
Sometimes the initial sanity check will fail. If this happens, just restart your run. Here's an example, where I've placed a file metagene_loadings.csv in the data_dir.
```
$ python datagpt.py
Please describe your task to me, or type exit to exit.
$ please make a heatmap of the metagene loadings and save as metagenes.png in figures
Please describe your task to me, or type exit to exit.
$ please use a clustergram to cluster the rows and columns in the heatmap
Please describe your task to me, or type exit to exit.
$ please set figsize to (60, 5)
There was an error in my code. Would you like me to debug? [y]/n
$ y
Please describe your task to me, or type exit to exit.
$ exit
```

The resulting script is simple but would have taken me about 30 minutes to make after parsing documentation to find the right plot type and parameters. Using DataGPT, it took about 2 minutes to describe my visiion for a plot and get a figure.
```
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# load the metagene loadings data
metagene_loadings_df = pd.read_csv('./data/metagene_loadings.csv', index_col=0)

# create the heatmap with clustering and adjusted figure size
clustergrid = sns.clustermap(metagene_loadings_df, cmap='YlGnBu', figsize=(60, 5))

# save the heatmap
fig = clustergrid.fig
fig.savefig('./figures/metagenes.png')
```
