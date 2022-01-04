from gc import callbacks
import os
from os import listdir
from os.path import isfile, join
import json
import dash
from dash import dcc
from dash import html
import dash_colorscales as dcs
from dash.dependencies import Input, Output, State, MATCH, ALL
from dash.exceptions import PreventUpdate
from mni import create_mesh_data, default_colorscale
import ast
from .git import *

suptitle = "PlasticPET Paper"


app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

app.title = "AgileX"
app.logo = "Agile"
app.subtitle = "An Agile Document Editor"
app.version = 0.1

server = app.server

GITHUB_LINK = os.environ.get(
    "GITHUB_LINK",
    "https://github.com/akhilsadam/AgileX",
)

def getfiles():
    return [f.replace(ext,"") for f in listdir(path) if not isfile(join(path, f))]
modules = []
#---
frontend = \
"""html.Div(
    [
        html.Form(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H4(suptitle,className="name"),
                                        html.A(app.title,href=GITHUB_LINK,className="logo"),
                                    ],
                                    className="top-text",
                                    style={'display': 'flex','flex-direction': 'row','justify-content': 'space-between','margin-left':'2em','margin-right':'1.25em'},
                                ),
                            ],
                            className="top",
                        ),
                        """
backend = \
"""                
                            html.Div(
                                [
                                    html.Div(dcc.Input(id='module-new-submit', type='text')),
                                    html.Button('Add Module', id='module-new', n_clicks=0, style={'display': 'block'}),
                                ],
                                className="module-add",
                                style={'display': 'flex','flex-direction': 'row','padding-left':'2em'},
                            ),
                            dcc.Store(id="annotation_storage"),
                            dcc.Location(id='url', refresh=True),
                    ],
                    className="main",
                ),
            ],
            action="#0",
        )
    ],
)"""
modular_comp = \
                        """html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.Dropdown(id={'type':'module-input-dropdown','instance':moduleid}, className='code-dropdown',
                                            options=[
                                                {'label': 'Show code', 'value': 'on'},
                                                {'label': 'Hide code', 'value': 'off'}
                                            ],
                                            value = 'off'
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        dcc.Textarea(id={'type':'module-input-code','instance':moduleid}, value=open(path+modulename+'/'+modulename+ext, "r").read(), style={'width': '100%'}),
                                                    ],
                                                    className="grow-wrap",
                                                ),
                                                html.Div(
                                                    [
                                                        html.Button('Save to disk', id={'type':'module-save','instance':moduleid}, n_clicks=0, style={'display': 'block'}),
                                                        html.Button('Commit', id={'type':'module-commit','instance':moduleid}, n_clicks=0, style={'display': 'block'}),
                                                    ],
                                                    className="module-button",
                                                    id={'type':'module-button','instance':moduleid},
                                                    style={'display': 'flex','flex-direction': 'row'},
                                                ),
                                                dcc.Location(id={'type':'url2','instance':moduleid}, refresh=True),
                                            ],
                                            className="module-input",
                                            id={'type':'module-input','instance':moduleid},
                                            style={'display': 'block','width': '100%'}
                                        ),
                                        html.Div(
                                            [
                                                dcc.Textarea(id={'type':'my-output','instance':moduleid}, value='', readOnly=True, style={'width': '100%','whiteSpace': 'pre-line'}),
                                            ],
                                            className="grow-wrap",
                                        ),
                                    ],
                                    className="element two-thirds column",
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                                [
                                                    html.H4(title+modulename),
                                                ],
                                            className="title",
                                            id={'type':'title','instance':moduleid},
                                        ),
                                    ],
                                    className="version one-third column",
                                ),
                            ],
                            className="module",
                        ),"""
#---|_/

# generate app layout
def serve_layout():
    global modules
    modules = getfiles()
    applayout = frontend + '\n'.join([modular_comp.replace("moduleid","\""+str(i)+"\"").replace("modulename","\""+modules[i]+"\"") for i in range(len(modules))]) + backend
    # print(applayout)
    return eval(applayout)
app.layout = serve_layout
#---|_/

# callbacks
modular_cbs = [\
    """Output(component_id='module-input'+sep+moduleid, component_property='style'),
    Input(component_id='module-input-dropdown'+sep+moduleid, component_property='value')""", \
    """Output(component_id='my-output'+sep+moduleid, component_property='value'),
    Input(component_id='module-input-code'+sep+moduleid, component_property='value')""" \
]

@app.callback(Output({'type': 'module-input','instance' : MATCH}, component_property='style'),
    Input({'type':'module-input-dropdown','instance' : MATCH}, component_property='value'))
def show_hide_element(visibility_state):
    if visibility_state == 'on':
        return {'display': 'block'}
    if visibility_state == 'off':
        return {'display': 'none'}

@app.callback(Output({'type': 'my-output','instance' : MATCH}, component_property='value'),
    Input({'type':'module-input-code','instance' : MATCH}, component_property='value'))
def update_module(input_value):
    return "{}".format(input_value)

@app.callback(Output({'type':'url2','instance':MATCH}, "href"),
    Input({'type':'module-save','instance':MATCH}, component_property='n_clicks'),
    State({'type':'module-input-code','instance':MATCH}, 'value'),
    State({'type':'module-input-code','instance':MATCH}, 'id'),
    prevent_initial_call=True,
)
def save_module(n_clicks,value,id):
    global modules
    modulename = str(modules[int(id['instance'])])
    with open(path+modulename+'/'+modulename+ext, "w") as f:
            f.write(value)
    return "/"

@app.callback(Output("url", "href"),
    Input('module-new', component_property='n_clicks'),
    State('module-new-submit', 'value'),
    prevent_initial_call=True,
)
def new_module(n_clicks,value):
    if n_clicks > 0:
        modulename = str(value)
        ospath = path+modulename+'/'
        print(ospath)
        try:
            os.mkdir(ospath)
        except: print("path already exists ...")
        with open(ospath+str(value)+ext, "a") as f:
            f.write("")
        # global modules
        # modules.append(value)
    return "/"

if __name__ == "__main__":
    app.run_server(debug=True)
