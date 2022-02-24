import pandas as pd
import requests
import json
import matplotlib.pyplot as plt
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

# ###--- 1) Pull the Human Capital Source (63) Summary, which contains the Indicator Id
api_url= base_url+source_url+indicators_url
# queries ={'format' :'json', 'per_page' : '6000', 'date' : '2020:2020', 'source': '63'}
queries ={'format' :'json', 'per_page' : '18000', 'mrv' : '3', 'source': '63'}
response=requests.get(api_url, params=queries)
len(response.json()[1]) #check
response.json()[1]

# ###--- 2) Isolate the Indicators, Store in List to Make the indicators portion of the HC URL"---###
indicators_id_hc=[]
indicators_id_hc = [ea['id'] for ea in response.json()[1]]
len(indicators_id_hc) #check
indicators_url ='/indicators/'+';'.join(indicators_id_hc)
indicators_url #check

# ###--- 3) Create new API url to pull all HC indicators by Country!
api_url= base_url+country_url+indicators_url
api_url

# ###--- 4) Pull all Human Capital Indicators by Country---###
response=requests.get(api_url, params=queries)
response.json()[0]


# ###--- NEXT STEPS CONVERT INTO DATAFRAME--- ###
# 1.) Extract Data from JSON Dictionary.
response.json()[1][0]['country']['id']


# 2.) Indicator & Country Key:Value pairs are nested in Dictionary form need to Extract them first and store in LIST
indicator_id=[]
indicator_name=[]
country_id=[]
country_name=[]

for ea in response.json()[1]:
     indicator_id.append(ea['indicator']['id'])
     indicator_name.append(ea['indicator']['value'])
     country_id.append(ea['country']['id'])
     country_name.append(ea['country']['value'])

# check
columns=['indicator_id', 'indicator_name', 'country_id', 'country_name']

# 3.) Convert list labesls to Series

series_labels=[]
for ea in [indicator_id, indicator_name, country_id, country_name]:
    print(len(ea))
    series_labels.append(pd.Series(ea))
# check
series_labels

#*****ISSUE!! NEED TO CHECK COUUNTRIES WITH DIFF # OF ROWS, MAKE SUR ORDER REMAINS INTACT

# 4.) Convert Series labesl  to Dataframes
df_labels=pd.DataFrame(series_labels).T
df_labels.columns=columns
df_labels.head()

# ### -- DELETE?? --- ###
        # pd.Series(list_labels)
        # labels= pd.DataFrame([indicator_id, indicator_name, country_id, country_name]).T
###-----------------###

# 5.) Store and convert JSON data values into a dataframe.
df_data =pd.DataFrame(response.json()[1])

# 6.) Join df labels to df data
df= df_labels.join(df_data)
df.shape

# drop old columns orginal indicator & country from df_data
df.drop(columns=['indicator','country'],inplace=True)
df.shape
df.head()


# ###------- NEXT Inspect data and start CLEANING ------- ###
df.shape

cols_to_check=df.iloc[:1,-4:].columns.to_list()

# RESULT shows that these columns have onlu Blank values and NAN --- NOTE isna and isnull are not capturing blank values! Needed ValueCounts!
for ea in cols_to_check:
    print(ea+":")
    print(df[ea].value_counts(dropna=False))
    print("\n")

df.drop(columns=cols_to_check, inplace=True)
df.shape #check
df.columns.to_list() #check

print('Dataframe created with NaN/empty cols dropped')

df

# ###---- Column checks BEFORE Refactoring-----###

                    #  Filter where isna.any is True-- NOTE series values is a Boolean, no need to set == True; already implied, but you can with no quotes
                    # df.isna().any()[df.isna().any()==True]
                    #
                    # # NOTE there are NAN and BLANK values MUST set dropna to FALSE...
                    # # isna and isnull do not capture blank values
                    # df.scale.value_counts(dropna=False)
                    # df.scale.isnull().value_counts() #check shows that all are either NaN or Blank
                    #
                    # df.scale[df.scale.isna()==False] # additional checks
                    # df.scale[:20] #additional checks CHECKING ROW INDEX 9-13, to verify some are NA some are Blank
                    #
                    # #   --- Rinse & repeat for  unit & obs ---
                    # df.unit.value_counts(dropna=False) # check shows that all are blank
                    # df.obs_status.value_counts(dropna=False) # check shows that all are blank
                    #

#--- NEXT What to do about MISSING VALUES  in the VALUES COLUMN?! --- ### <-- thinking at the most detailed level needed to meet end goal.
# I think I should fill them with NAN,  or drop them.
    # Zero Values may distort graphs
    # Graphs should skip NAN ...or blanks???
    # What would be the consequences of droppiing MISSING values?
        #Which missing values make sense to drop?
        #For timeseries data, for a given country, it may makes sense to
            # take an average for in between years,
            # or uses the last value for later year, or prior years
            # HOWEVER, GIVEN  COVID-19 if there are sharp changes It might not make sense
                #### Need to understand which years in times series are most MISSING
                #### AND the trend, or trend dispruption due to covid.
        #FOR cross Country data, it will make sense to drop them sense you do not have the contextt to impute missing data, based on regional, or like country averages...abs()

df


# ###---- STRATEGY for Evaluating Missing Values: Is it Entire Years? Entire Countries? Entire Indicators? ---- ### <<-- thinking at most broad/ high-level

###--- NEED A CHECK- !

df.groupby('date')['value'].count()

len(df.country_id.unique())
df.groupby(['country_id','indicator_id','date'])['value'].mean()

# ###Evaluated whether to drop entire year = NO!

df.groupby(['country_id','date'])['value'].sum()
df.groupby('date')['value'].count()
# ###Evaluated whether to drop entire countries w all years if 0 values = YES

#REFACTORED - Count MissingNess by Country by Year
for ea in range(2017,2021):
    print(ea , (df[df.date==str(ea)].groupby('country_id')['value'].count() ==0).sum())

# Identify whether the same countries reoccurr

ctry_totals= df.groupby('country_id')['value'].sum()
ctry_drop_ids= ctry_totals[ctry_totals==0].index.to_list()
type(ctry_drop_ids)
ctry_drop_ids

# -- DROPPED Countrys with NaN/ZERO Values for All three years
###****** NOTE SYNTAX!! ~ negates the isin() method and ONLY filters those NOT IN THE LIST!!!*****#############
df=df[~df.country_id.isin(ctry_drop_ids)]

# check
df[df.country_id.isin(ctry_drop_ids)].any().sum()

df.shape


# ### Evaluate remaining MissingNess within country by years
# Evaluate whether MissingNess is across the same indicators

len(df.country_id.unique())
( ==0).sum(0)

#Evaluate Entire  Indicators = NO!
(df.groupby('indicator_id')['value'].sum()==0).sum()

#Evaluate entire Indicators by year = NO!
(df.groupby(['indicator_id','date'])['value'].sum()==0).sum()

# Number Misising remaining
df.value.isna().sum()


for ea in range(2017,2021):
    print(ea , (df[df.date==str(ea)].groupby(['country_id','date','indicator_id'])['value'].count() ==0).sum())

ctry_singleYr_miss=df.groupby(['country_id','date'])['value'].sum()==0

ctry_singleYr_miss=ctry_singleYr_miss[ctry_singleYr_miss==True]

#visualize remaining MissingNess
ctry_singleYr_miss.plot(x='date',y='value')


# Results of evaluation show that remaining MissingNess is at the most detailed level.... cty,ind,yr
# Next steps... back to end notes from last wotking session


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
