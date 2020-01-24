# -*- coding: utf-8 -*-
"""
Created on Thu May 16 13:33:20 2019

@author: Florian
"""

import os 
import getpass

import pandas as pd


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


        
        
#==============================================================================
#                               Functions
#==============================================================================

#______________________________________________________________________________
#
#                                Layout
#______________________________________________________________________________
def layout():
    output = html.Div([
                    # ENTER BLOCKS HERE
                ])
    return output                                 

#______________________________________________________________________________
#
#                                Callbacks
#______________________________________________________________________________
def callbacks(app):  
    @app.callback(Output('output-state2', 'children'),
                  [Input('submit-button', 'n_clicks')],
                  [State('input-1-state', 'value'),
                   State('input-2-state', 'value')])
    def update_output2(n_clicks, input1, input2):
            return u'''
                The Button has been pressed {} times,
                Input 1 is "{}",
                and Input 2 is "{}"
            '''.format(n_clicks, input1, input2)