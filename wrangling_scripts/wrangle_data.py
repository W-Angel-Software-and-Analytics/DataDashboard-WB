import pandas as pd
import requests
import json
from collections import defaultdict
import plotly.graph_objs as go


###---My comments are in this format; Course comments in #, anythin in ###--- will be deleted when project is complete---

print("HELLO! Wrangle_data.py file accessed")

###------THIS SECTION IS TO TEST CREATING THE JOINED LIST OF BOTH ID & NAME ----###
            # test1=[]
            # test2=[]
            #
            # for ea in req.json()[1]:
            #     test1.append(ea['id'])
            #     test2.append(ea['name'])
            #
            # test1
            # test2



# Use this file to read in your data and prepare the plotly visualizations. The path to the data files are in
# `data/file_name.csv`

# ----I chose to Connect to World Bank API instead of using a csv download because I wanted to the app to dynamically update----#
# ###--------EXAMPLE API REQUESTS--------###
# ### req = requests.get('https://api.worldbank.org/v2/country', params=queries)
# ###req = requests.get('https://api.worldbank.org/v2/indicators', params=queries)
# ###req = requests.get('https://api.worldbank.org/v2/countries/all/indicators/SP.POP.TOTL', params=queries)
# ###req = requests.get('https://api.worldbank.org/v2/source/1/indicators', params=queries)
# ###--- Country, Indicator, Aggregate

# ###CREATE API URL

base_url ='https://api.worldbank.org/v2'
country_url= '/countries/all'
source_url= '/source/63'
indicators_url= '/indicators/'

###--- 1) Pull the Human Capital Source (63) Summay, which containes the idicator Id
api_url= base_url+source_url+indicators_url
# queries ={'format' :'json', 'per_page' : '6000', 'date' : '2020:2020', 'source': '63'}
queries ={'format' :'json', 'per_page' : '18000', 'mrv' : '3', 'source': '63'}
response=requests.get(api_url, params=queries)
len(response.json()[1]) #check
response.json()[0]

###--- 2) Isolate the Indicators, Store in List to Make the indicators portion of the HC URL"---###
indicators_id_hc=[]
indicators_id_hc = [ea['id'] for ea in response.json()[1]]
len(indicators_id_hc) #check
indicators_url ='/indicators/'+';'.join(indicators_id_hc)
indicators_url #check

###--- 3) Create new API url to pull all HC indicators by Country!
api_url= base_url+country_url+indicators_url
api_url

###--- 4) Pull all Human Capital Indicators by Country---###
response=requests.get(api_url, params=queries)
response.json()[0]


###--- NEXT STEPS
# 1.) Extract Data from JSON Dictionary.
response.json()[1][0]['country']['id']

indicator_id=[]
indicator_name=[]
country_id=[]
country_name=[]

for ea in response.json()[1]:
     indicator_id.append(ea['indicator']['id'])
     indicator_name.append(ea['indicator']['value'])
     country_id.append(ea['country']['id'])
     country_name.append(ea['country']['value'])

#check
columns=['indicator_id', 'indicator_name', 'country_id', 'country_name']


list_labels=[]
for ea in [indicator_id, indicator_name, country_id, country_name]:
    print(len(ea))
    list_labels.append(pd.Series(ea))
list_labels
list_labels=pd.DataFrame(list_labels).T
list_labels.columns=columns
list_labels

# pd.Series(list_labels)


# labels= pd.DataFrame([indicator_id, indicator_name, country_id, country_name]).T




data

# 2.) Store into a dataframe.
data =pd.DataFrame(response.json()[1])
df= list_labels.join(data)
df.shape
df.drop(columns=['indicator','country'],inplace=True)
df.shape
df.head()

pd.DataFrame()

# def return_figures():
#     """Creates four plotly visualizations
#
#     Args:
#         None
#
#     Returns:
#         list (dict): list containing the four plotly visualizations
#
#     """
#
#     # first chart plots arable land from 1990 to 2015 in top 10 economies
#     # as a line chart
#
#     graph_one = []
#     graph_one.append(
#       go.Scatter(
#       x = [0, 1, 2, 3, 4, 5],
#       y = [0, 2, 4, 6, 8, 10],
#       mode = 'lines'
#       )
#     )
#
#     layout_one = dict(title = 'Chart One',
#                 xaxis = dict(title = 'x-axis label'),
#                 yaxis = dict(title = 'y-axis label'),
#                 )
#
# # second chart plots ararble land for 2015 as a bar chart
#     graph_two = []
#
#     graph_two.append(
#       go.Bar(
#       x = ['a', 'b', 'c', 'd', 'e'],
#       y = [12, 9, 7, 5, 1],
#       )
#     )
#
#     layout_two = dict(title = 'Chart Two',
#                 xaxis = dict(title = 'x-axis label',),
#                 yaxis = dict(title = 'y-axis label'),
#                 )
#
#
# # third chart plots percent of population that is rural from 1990 to 2015
#     graph_three = []
#     graph_three.append(
#       go.Scatter(
#       x = [5, 4, 3, 2, 1, 0],
#       y = [0, 2, 4, 6, 8, 10],
#       mode = 'lines'
#       )
#     )
#
#     layout_three = dict(title = 'Chart Three',
#                 xaxis = dict(title = 'x-axis label'),
#                 yaxis = dict(title = 'y-axis label')
#                        )
#
# # fourth chart shows rural population vs arable land
#     graph_four = []
#
#     graph_four.append(
#       go.Scatter(
#       x = [20, 40, 60, 80],
#       y = [10, 20, 30, 40],
#       mode = 'markers'
#       )
#     )
#
#     layout_four = dict(title = 'Chart Four',
#                 xaxis = dict(title = 'x-axis label'),
#                 yaxis = dict(title = 'y-axis label'),
#                 )
#
#     # append all charts to the figures list
#     figures = []
#     figures.append(dict(data=graph_one, layout=layout_one))
#     figures.append(dict(data=graph_two, layout=layout_two))
#     figures.append(dict(data=graph_three, layout=layout_three))
#     figures.append(dict(data=graph_four, layout=layout_four))
#
#     return figures
