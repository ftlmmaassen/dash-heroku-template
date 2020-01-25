# -*- coding: utf-8 -*-
"""
Created on Thu May 16 13:33:20 2019

@author: Florian
"""

import os 
import getpass

import pandas as pd


main_directory = os.chdir(r"C:\\Users\\florian.maassen\\Desktop\\Dashboard\\BGB_Dash\\Tab1\\DOOR_EMEA_MAP")

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


#==============================================================================
#                               General modules
#==============================================================================
#==============================================================================
#                           Tab specific deinitions
#==============================================================================



#==============================================================================
#                                    Data
#==============================================================================

   
     
from plotly.offline import plot
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import os
import json
import seaborn
from datetime import datetime

seaborn.set(style='ticks')


# Set dot coloring, func1
def return_color(x):
    if x == 'A':
        return 'black'
    elif x == 'B':
        return 'maroon'
    else:
        return 'navy'
    
#colorscale used in heatmap
 
pl_deep=[[0.0, '#9095ab'],
         [0.1, '#848dad'],
         [0.2, '#7884ae'],
         [0.3, '#6d7cb0'],
         [0.4, '#9173b2'],
         [0.5, '#556bb4'],
         [0.6, '#4962b5'],
         [0.7, '#3d5ab7'],
         [0.8, '#3152b9'],
         [0.9, '#2549bb'],
         [1.0, '#0230c0']]
    
# Set upper lowerbound sizing of DoorDots, func2
def var_check(x, lower_bound=10, upper_bound=20):
    if lower_bound <= x <= upper_bound:
        return x
    else:
        return (upper_bound + lower_bound) / 2

#set working directory    
# os.chdir(r"C:\Users\florian.maassen\Desktop\Dashboard\BGB_Dash\Tab1\DOOR_EMEA_MAP")

#Read BGB Doorfile - 22/01/2020
#df = pd.read_csv('Bugaboo_Source_Data.csv')
url = 'https://raw.githubusercontent.com/ftlmmaassen/dash-heroku-template/master/Tab1/DOOR_EMEA_MAP/Bugaboo_Source_Data.csv'
df=pd.read_csv(url)


#Apply sizing and coloring to door dataframe based on func1 and func2
df['Color_Code'] = df['Door_Classification'].apply(lambda x: return_color(x))
df['Size'] = df['Door_Revenue_Estimate'].apply(lambda x: var_check(x/1000))


#mapbox access token to use plotly geomapbox etc
mapbox_access_token = 'pk.eyJ1IjoiZmxvcmlhbm1hYXNzZW4iLCJhIjoiY2s0YjF0aWZsMDlobTNlbzJ4OXllZG43dCJ9.fpt1QgNM4wfcqErAvd4LVA'

#assign doors to separate dataframes based on classification
df_a = df.loc[df['Door_Classification'] == 'A']
df_b = df.loc[df['Door_Classification'] == 'B']
df_c = df.loc[df['Door_Classification'] == 'C']
       



## PREPARATION FOR CHROLOPLETMAPBOX
## NUTS LEVEL SELECTED = 2
## LIST OF NUTS AVAILABLE ON DRIVE

nutslevel = str(2)
geojson_filename = 'NUTS_RG_01M_2016_4326_LEVL_'+nutslevel+'.geojson'
with open(geojson_filename) as f:
    jdata = json.load(f)

    
L = len(jdata['features'])

jdata['features'][0]

for k in range(L):
    jdata['features'][k]['id'] = f'{k}'

  
#usage of array for data was to be able to append multiple macro variables
# ideally with selection menu built into the dashboard
    
data = []  
data.append(go.Choroplethmapbox(locations = [jdata['features'][k]['id'] for k in range(L)],
                                             
                                    #HERE WE SHOULD LINK THE MACRO VAR TO THE GEO-AREA
                                     z = np.random.randint(0, 11,  size=L), #synthetic data
                                     colorscale = pl_deep,
                                     colorbar = dict(thickness=10, ticklen=1),
                                     geojson = jdata,
                                     marker_line_width=0, marker_opacity=0.4,
                                     text = ['Region Name: '+jdata['features'][k]['properties']['NUTS_NAME'] for k in range(L)],
                                     visible=False,
                                     name = '<b>Geo-Area'))
  
data[0]['visible'] = True
  
#START BUILDING PLOT

""" START WITH CHOROPLET BASE LAYER """        
#create scattermapbox figure that plots doors on a map
#build on three thraces (base with c doors, two additional traces on b and c doors)
fig = go.Figure(data[0])

""" ADD SCATTER LAYERS SPECIFIED BY DOOR CLASSIFICATION """      


fig.add_trace(go.Scattermapbox(
        ## C DOORS TRACE
        lat=df_a['Latitude'],
        lon=df_a['Longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            color = df_a['Color_Code'],
            size = df_a['Size']
        ),
        text='Door Name: '  +df_a['Door_Name']+'<br>'+ \
             'Parent Account: '+ df_a['Account_Name'] +'<br>',
             name = '<b>A Doors'
    ))       

fig.add_trace(go.Scattermapbox(
        ## B DOORS TRACE
        lat=df_b['Latitude'],
        lon=df_b['Longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            color = df_b['Color_Code'],
            size = df_b['Size']
        ),
        text='Door Name: '  +df_b['Door_Name']+'<br>'+ \
             'Parent Account: '+ df_b['Account_Name'] +'<br>',
             name = '<b>B Doors'
    ))        


fig.add_trace(go.Scattermapbox(
        ## C DOORS TRACE
        lat=df_c['Latitude'],
        lon=df_c['Longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            color = df_c['Color_Code'],
            size = df_c['Size']
        ),
        text='Door Name: '  +df_c['Door_Name']+'<br>'+ \
             'Parent Account: '+ df_c['Account_Name'] +'<br>',
        name = '<b>C Doors'
    ))
        
## UPDATE FIGURE LAYOUT AND PAGE HTML ELEMENTS
fig.update_layout(title = '<b>BUGABOO'+ '</b> - EMEA DOORS',
                  font=dict(
        family="Helvetica",
        size=20,
        color="#181818"
    ),
    hovermode='closest',
    mapbox=go.layout.Mapbox(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=52,
            lon=5
        ),
        pitch=0,
        zoom=6, 
        style="light"
    )
)

fig.update_layout(
    legend=go.layout.Legend(
        x=0,
        y=1,
        traceorder="normal",
        font=dict(
            family="Helvetica",
            size=20,
            color="black"
        ),
        bgcolor="rgb(236, 239, 241)",
        bordercolor="Black",
        borderwidth=1
    )
)        




#==============================================================================
#                               Functions
#==============================================================================

#______________________________________________________________________________
#
#                                Layout
#______________________________________________________________________________
def layout():
    output = html.Div([         
            
          
                                html.Div(
                                        [dcc.Graph(style={'height': '90vh'},
                                                    id = 'matrix',
                                                    figure = fig,
                                                    )
                                        ]
                                        )                      
                                ])

    return output                                   

#______________________________________________________________________________
#
#                                Callbacks
#______________________________________________________________________________
def callbacks(app):  
    @app.callback(Output('output-state2', 'children'),
                  [Input('submit-button', 'n_clicks')],
                  [State('input-1-state', 'value')])
    def update_output2(n_clicks, input1):
            return u'''
                The Button has been pressed {} times,
                Select NUTS level is "{}",
            '''.format(n_clicks, input1)