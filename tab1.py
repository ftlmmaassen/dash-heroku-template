# -*- coding: utf-8 -*-
"""
Created on Thu May 16 13:33:20 2019

@author: Florian
"""

import os 
import getpass

import pandas as pd

main_directory = os.chdir(r"C:\\Users\\florian.maassen\\Desktop\\Dashboard\\BGB_Dash\\Tab1\\DOOR_EMEA_MAP")
from Door_Dashboard_v1 import create_heatmap


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

fig = create_heatmap()
        
        
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