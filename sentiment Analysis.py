#!/usr/bin/env python
# coding: utf-8

# In[61]:


# the requests library to get the data. 
from urllib.request import urlopen , Request
# the BeautifulSoup library to parse data from the website.
from bs4 import BeautifulSoup
# the nltk.sentiment.vader library to perform sentiment analysis on the news headlines. 
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# The Pandas library will be used to store the data in its DataFrame objects
import pandas as pd
# the Matplotlib library will be used to visualize the data. 
import matplotlib.pyplot as plt


# In[62]:


# the url to search other tickers
finviz_url = 'https://finviz.com/quote.ashx?t='

# the list of tickers you want to use
tickers = ['AMZN', 'GOOG', 'TSLA']

news_tables = {}
# Create a for loop to get the full link 
for ticker in tickers:
    url = finviz_url + ticker
    
    req = Request(url=url, headers={'user-agent':'my-app'})
    response = urlopen(req)

    html = BeautifulSoup(response,'lxml')
    # search a spicefic id called news_table in html page
    news_table = html.find(id='news-table')
    # dictionary has a key called ticker
    news_tables[ticker] = news_table
    break


# In[63]:


# now the dictionary has just the table of my result from the webpage
# our data set in a list
parsed_data = []

#The first for loop will iterate over the news,
for ticker, news_table in news_tables.items():
# while the second for loop will iterate over all <tr> tags in the news_table. 
    for row in news_table.findAll('tr'):

        title = row.a.text
#The split() function will split the text placed in <td> tag into a list. 
        date_data = row.td.text.split(' ')

        if len(date_data) == 1:
            time = date_data[0]
        else:
            date = date_data[0]
            time = date_data[1]

        parsed_data.append([ticker, date, time, title])


# In[64]:


# Applaying sentiment Analysis
# 1 - create a data frame
df = pd.DataFrame(parsed_data ,columns = ['ticker', 'date', 'time', 'title'])
# will be used to analyze any given text and give it a score
vader = SentimentIntensityAnalyzer()
# what ever string pass in to this function will give me a score only
f = lambda title: vader.polarity_scores(title)['compound']
df['compound'] = df['title'].apply(f)
df['date'] = pd.to_datetime(df.date).dt.date
print (df.head())


# In[66]:


# Visiualize the data
plt.figure(figsize=(10,8))
mean_df = df.groupby(['ticker', 'date']).mean().unstack()
mean_df = mean_df.xs('compound', axis="columns")
mean_df.plot(kind='bar')
plt.show()


# In[ ]:




