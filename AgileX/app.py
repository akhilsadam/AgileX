from gc import callbacks
import os
import json
import dash
from dash import dcc
from dash import html
import dash_colorscales as dcs
from dash.dependencies import Input, Output, State, MATCH, ALL
from dash.exceptions import PreventUpdate
from mni import create_mesh_data, default_colorscale
import ast

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

app.title = "AgileX : An Agile Document Editor"
app.version = 0.1

server = app.server

GITHUB_LINK = os.environ.get(
    "GITHUB_LINK",
    "https://github.com/plotly/dash-sample-apps/tree/master/apps/dash-brain-viewer",
)

sep = '-'
modules = ['1-1-1','1-1-2','1-1-3']
#moduleid = modules[0]

#---
frontend = \
"""html.Div(
    [
        html.Div(
            [
                """
backend = \
"""                dcc.Store(id="annotation_storage"),
            ],
            className="main",
        ),
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
                                                dcc.Textarea(id={'type':'module-input-code','instance':moduleid}, value='', style={'width': '100%'}),
                                            ],
                                        ),
                                        html.Button('Save to disk', id={'type':'module-save','instance':moduleid}, n_clicks=0, style={'display': 'block'}),
                                    ],
                                    className="module-input",
                                    id={'type':'module-input','instance':moduleid},
                                    style={'display': 'block','width': '100%'}
                                ),
                                html.Div(
                                    [
                                        dcc.Textarea(id={'type':'my-output','instance':moduleid}, value='', style={'width': '100%','whiteSpace': 'pre-line'}),
                                    ],
                                ),
                            ],
                            className="element two-thirds column",
                        ),
                        html.Div(
                            [
                                html.Div(
                                        [
                                            html.H4("Module "+modulename),
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
applayout = frontend + '\n'.join([modular_comp.replace("moduleid","\""+str(i)+"\"").replace("modulename","\""+modules[i]+"\"") for i in range(len(modules))]) + backend
# print(applayout)
app.layout = eval(applayout)
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

if __name__ == "__main__":
    app.run_server(debug=True)
