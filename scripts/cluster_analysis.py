import seaborn as sns
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from adjustText import adjust_text

sns.set(rc={'figure.figsize':(10,10)})

def main():
    #Download covid data from the NYTimes repo
    #url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv"
    #covid_us = pd.read_csv(url)

    url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"
    covid_state = pd.read_csv(url, index_col=0)

    state_pops = pd.read_csv('data\population-us-2020-census.csv', thousands=',')
    
    #This file is 100MB, so only do county analysis if you have a big harddrive
    #url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
    #us_county = pd.read_csv(url)

    #Convert dates to date objects
    covid_state.index = pd.to_datetime(covid_state.index)

    #Get new cases and deaths from cumulative values
    covid_state = covid_state.sort_values(by=['state', 'date'])
    covid_state['new-cases'] = covid_state.groupby(['state'])['cases'].diff().fillna(covid_state['cases'])
    covid_state['new-deaths'] = covid_state.groupby(['state'])['deaths'].diff().fillna(covid_state['deaths'])

    #Get rolling averages
    grouped_state = covid_state.groupby('state')
    covid_state["7-day-cases"] = grouped_state['new-cases'].\
        transform(lambda x: x.rolling("7D").mean())
    covid_state["7-day-deaths"] = grouped_state['new-deaths'].\
        transform(lambda x: x.rolling("7D").mean())
    #Resets index to columns
    covid_state = covid_state.reset_index()

    num_cols = ['cases','deaths','7-day-cases','7-day-deaths']
    per_capita_state = covid_state.merge(state_pops, how='left', on='state')
    per_capita_state[num_cols] = per_capita_state[num_cols].div( per_capita_state['resident.population'], axis=0)
    print(per_capita_state)

    #Make a dataframe of monthly averages
    state_monthly = covid_state.groupby(['state',
                            pd.PeriodIndex(covid_state['date'], 
                            freq="M")])['new-cases','new-deaths'].mean()
    state_monthly = state_monthly.reset_index()
    state_monthly['date'] = state_monthly['date'].astype(str)
    cases_monthly = state_monthly.pivot(index='state', 
                                        columns='date', 
                                        values='new-cases').fillna(0)
    deaths_monthly = state_monthly.pivot(index='state', 
                                         columns='date', 
                                         values='new-deaths').fillna(0)

    #Make a datafame of total deaths and cases for each state
    state_totals = covid_state.groupby('state')['cases','deaths'].max()
    print(state_totals)

   
    #Scatterplot of states
    ax = sns.scatterplot(data=state_totals, x="cases", y="deaths", )
    #loop over those rows to annotate
    texts = []
    for i,row in state_totals.iterrows():
        texts.append(ax.text(row['cases'], row['deaths'],i))
    plt.tight_layout()
    adjust_text(texts, arrowprops=dict(arrowstyle='->', color='red'))
    plt.show()
   

    #Clustering on monthly average new cases
    n = 5
    kmeans = KMeans(n_clusters=n, random_state=0).fit(cases_monthly)
    for i in range(n):
        print(cases_monthly.index[kmeans.labels_ == i])
    state_totals['cluster'] = kmeans.labels_

    #Scatterplot of states colored by cluster
    ax = sns.scatterplot(data=state_totals, x="cases", y="deaths", hue='cluster', s=100)
    plt.tight_layout()
    plt.show()

    #Pivoted dataframe
    #state_cases_wide = covid_state.pivot(index='state', columns='date', values='7-Day-Cases').fillna(0)
    #state_deaths_wide = covid_state.pivot(index='state', columns='date', values='7-Day-Deaths').fillna(0)
    return
main()