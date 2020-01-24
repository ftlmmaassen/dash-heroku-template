# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 11:14:07 2019

@author: Florian

# -*- coding: utf-8 -*-
"""

import sys 
import getpass
import os 
import base64
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import flask 

main_directory = os.getcwd()

os.chdir(main_directory) 
import tab1
os.chdir(main_directory) 
import tab2
os.chdir(main_directory) 
import tab3

import requests
import Image
from PIL import Image
import requests
from io import BytesIO


#==============================================================================
#                                 Own modules 
#==============================================================================

css_directory = os.path.join(main_directory,'assets')
stylesheets = ['style1.css','style2.css',
               'Raleway.css',
               'stylesheet_pop_up.css',
               'Product Sans.css']
static_css_route = '/static/'


#==============================================================================
#                                 Tab Styling  
#==============================================================================

tabs_styles = {
    'height': '35px'
}
tab_style = {
    'borderBottom': '2px solid #000000',
    'padding': '6px',
    'backgroundColor': '#424242',
    'color':'white'
    #'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #FFFFFF',
    'borderBottom': '2px solid #000000',
    'backgroundColor': 'navy',
    'color': 'white',
    'padding': '6px'
    #'fontWeight': 'bold'
}

#______________________________________________________________________________
#
#                                 Create app 
#______________________________________________________________________________

app = dash.Dash() 
app.title = "BUGABOO DOOR DASHBOARD"


@app.server.route('{}<stylesheet>'.format(static_css_route))
def serve_stylesheet(stylesheet):
    if stylesheet not in stylesheets:
        raise Exception(
            '"{}" is excluded from the allowed static files'.format(
                stylesheet
            )
        )
    return flask.send_from_directory(css_directory, stylesheet)

#______________________________________________________________________________
#
#                               App options
#______________________________________________________________________________

app.scripts.config.serve_locally = False
app.config['suppress_callback_exceptions'] = True

#______________________________________________________________________________
#______________________________________________________________________________
#
#                                 LAYOUT
#______________________________________________________________________________
#______________________________________________________________________________

""" This part of the layout describes the main page containing all the tabs.
    On the top of the page, the logo of DataQuest is presented. This logo can
    be changed by replacing the url by an url of another logo (it has to be 
    somewhere online). 
    
    The style part defines the height of the header and the color. It is 
    followed by the definitions of the tabs. I advise to not change this part,
    except for the label part ('NAME TAB1' with value 1 etc.). 
"""

#------------------------------------------------------------------------------    
app.layout = html.Div(children=[
        
        # TITLE BLOCK SUBDIV1
                    html.Div(#
                            ),

        # TAB DEFINITION BLOCKS SUBDIV2
        
                    # Defining the tabs:
                    html.Div([                  
                    dcc.Tabs(id="tabs", value=1, children=[
                    
                    dcc.Tab(label='Bugaboo EMEA Doors', value=1, style=tab_style, selected_style=tab_selected_style)
    
                   # ,dcc.Tab(label='<Tab 2>', value=2, style=tab_style, selected_style=tab_selected_style)
    
                   # ,dcc.Tab(label='<Tab 3>', value=3, style=tab_style, selected_style=tab_selected_style)
    
                                                            ],style=tabs_styles
                    
                    ),
    
         # TAB CONTENT DIVS SUBDIV2
   
                    html.Div(id='tabs-content')],        
                    style= {'padding': '0px 0px 600px 0px',
                             'marginLeft': 'auto', 'marginRight': 'auto', "width":'100%',
                            'boxShadow': '0px 0px 0px 0px rgba(204,204,204,0.4)'
                            } )])
    
    
#------------------------------------------------------------------------------                       
@app.callback(Output('tabs-content', 'children'), [Input('tabs', 'value')])
def display_content(value):
    if value == 1:
       print('USER CLICKED ON TAB 1')
       output = tab1.layout()
       return output 
    elif value == 2:   
        print('USER CLICKED ON TAB 2')
        output = tab2.layout()
        return output   
    elif value == 3:   
        print('USER CLICKED ON TAB 3')
        output = tab3.layout()
    return output 

os.chdir(main_directory) 
#tab3.layout_subtabs(app)                    
                                            
#______________________________________________________________________________
#______________________________________________________________________________
#
#                               CALL BACKS
#______________________________________________________________________________
#______________________________________________________________________________

#tab1.callbacks(app)     

tab2.callbacks(app)    
 
#tab3.callbacks(app)

#______________________________________________________________________________
#______________________________________________________________________________
#    
#                               5.RUN
#______________________________________________________________________________
#______________________________________________________________________________
""" Below the app is extended with some css on the internet. This is mostly for 
    layout reasons (nice type setting etc.), so I recommend not to change this.
    Here also the width of the className's are defined.
"""     
#os.chdir(main_directory)
#external_css = ["https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
#                "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
##                "https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i",
##                "https://codepen.io/cryptocss/pen/geyPdg.css",
##                "https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i",
#               ]
#
#for css in external_css:
#    app.css.append_css({"external_url": css})

for stylesheet in stylesheets:
    app.css.append_css({"external_url": "/static/{}".format(stylesheet)})
    
    
external_js = ["https://code.jquery.com/jquery-3.2.1.min.js",
               "https://cdn.rawgit.com/plotly/dash-app-stylesheets/a3401de132a6d0b652ba11548736b1d1e80aa10d/dash-goldman-sachs-report-js.js"]
 
for js in external_js:
    app.scripts.append_script({"external_url": js})

#------------------------------------------------------------------------------
    
if __name__ == '__main__':
    app.run_server()         