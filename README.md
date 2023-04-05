# Clustering
March 15, 2023

## Setup 

1. Clone or download this Git repository.
2. Either make a new conda environment for this project or add any needed packages to your current environment. 
The `adjusttext` package can be installed with:
```commandline
conda install -c conda-forge adjusttext
```
3. Run the script. What is it doing right now?
4. Determine the content/format of the `covid_state`, `per_capita_state`, `state_totals`, `cases_monthly`, and `deaths_monthly` dataframes.
You can print built-in summaries like `df.head()`, `df.info()`, and `df.describe` to help figure out what each dataframe contains. 

## Basic Cluster Analysis

1. Take a look at the current k-means clustering of states. 
What is being clustered on? 
What do the clusters seem to represent?
2. Try instead clustering on monthly mean data. 
Do the clusters change at all?
3. Now try plotting population total on one of the axes. 
How do the current cluster assignments compare to population? 
4. Change the scatter plot to use per-capita totals. 
Hint: Take a look at how the `state_totals` dataframe was created. 
Do the same but starting with the `per_capita` dataframe.
5. How many "big" clusters do you see, and how would you decide on the number of clusters to use?

## Alternative data representations

Try looking at some other ways of summarizing the data to see how clusters are effected.

- Try constructing a column of the cases/deaths ratio and clustering on it. 
- As opposed to the `mean` try clustering on other summary statistics like the `max`, `std`, or the total number of `0`'s.
- Try clustering on each year individually. Does the clustering structure change by year?

## Alternative clustering methods

Now try out different clustering methods.
You can try any of the methods in the [sci-kit learn cluster module](https://scikit-learn.org/stable/modules/clustering.html).
Do any of them produce clusters you feel fit the data better? 
Try some of the different analyses and data types you played with above in combination with different clustering methods. 

You can also try installing the [UMAP](https://umap.scikit-tda.org/transform.html) package. 
How do these clusters compare?

## Looking for other structure

- As opposed to clustering states, try clustering months. What months appear to be similar?
- Try creating columns with percent of state cases/deaths. How do these clusters compare?
- With your percent columns, cluster death and case version of each state. 
Do any state's death patterns look like other state's case patterns?

## Time Series Clustering

[tslearn](https://tslearn.readthedocs.io/en/stable/index.html) is a Python package centered around time-series analysis. 
Try installing `tslearn` and performing a [dynamic time warping](https://tslearn.readthedocs.io/en/stable/user_guide/clustering.html) k-means analysis.

