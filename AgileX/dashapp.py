from gc import callbacks
import os
from os import listdir
from os.path import isfile, join
import json
import dash
from dash import dcc
from dash import html
import dash_colorscales as dcs
from dash.dependencies import ClientsideFunction, Input, Output, State, MATCH, ALL
from dash.exceptions import PreventUpdate
# from mni import create_mesh_data, default_colorscale
import time
from . import git

suptitle = "PlasticPET Paper"

GITHUB_LINK = os.environ.get(
    "GITHUB_LINK",
    "https://github.com/akhilsadam/AgileX",
)

current_path = os.getcwd()

spfold = '.git'

def getfiles():
    return [f.replace(git.ext,"") for f in listdir(git.path) if (not isfile(join(git.path, f)) and spfold not in f)]
modules = []
moduleID = 0

def init_dashboard(server):

    app = dash.Dash(
        server = server,
        routes_pathname_prefix='/dashapp/',
        meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    )

    app.title = "AgileX"
    app.logo = "Agile"
    app.subtitle = "An Agile Document Editor"
    app.version = 0.1

    #---
    app.index_string = '''
    <!DOCTYPE html>
    <html>
        <head>
            {%metas%}
            <title>{%title%}</title>
            {%favicon%}
            {%css%}
        </head>
        <body>
            {%app_entry%}
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
    </html>
    '''.replace('cwdp',current_path)
    #---
    frontend = \
    """html.Div(
        [
            html.Form(
                [
                    html.Div([],className="bkgd"),
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
                                        html.Div(dcc.Input(id='module-new-submit', type='text', value='0')),
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
                                                            dcc.Textarea(id={'type':'module-input-code','instance':moduleid}, value=open(git.path+modulename+'/'+modulename+git.ext, "r").read(), style={'width': '100%'}),
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
                                                    html.H4(git.title+modulename),
                                                ],
                                                className="title",
                                                id={'type':'title','instance':moduleid},
                                            ),
                                            html.Div(
                                                [
                                                ],
                                                id={'type':'graph-container','instance':moduleid},
                                                className="graph-container",
                                            ), 
                                            dcc.Textarea(id={'type':'graph-container-data','instance':moduleid}, value='', readOnly=True, style={'display':'none'}),
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
        print(app)
        return eval(applayout)
    app.layout = serve_layout
    #---|_/

    init_callbacks(app)

    return app.server

def init_callbacks(app):
    # callbacks

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
        modulename = str(int(id['instance']))
        with open(git.path+modulename+'/'+modulename+git.ext, "w") as f:
                f.write(value)
        return "/"

    @app.callback(Output("url", "href"),
        Input('module-new', component_property='n_clicks'),
        State('module-new-submit', 'value'),
        prevent_initial_call=True,
    )
    def new_module(n_clicks,value):
        if n_clicks > 0:
            givenname = str(value)
            global moduleID
            modulename = str(moduleID)
            moduleID+=1
            ospath = git.path+modulename+'/'
            print(ospath)
            try:
                os.mkdir(ospath)
                git.git_submodule_init(ospath)
            except: print("path already exists ...")
            with open(ospath+modulename+git.ext, "a") as f:
                f.write("")
            git.git_update(ospath,"new module "+modulename)
            # global modules
            # modules.append(value)
        return "/"

    #GITGRAPH
    # app.clientside_callback(
    #     ClientsideFunction(
    #         namespace='clientside',
    #         function_name='gitgraph_function'
    #     ),
    #     Output({'type':'graph-data','instance':MATCH}, 'value'),
    #     [Input({'type':'graph-container-data','instance':MATCH}, 'value')],
    #     State({'type':'graph-container','instance':MATCH}, 'id'),
    #     prevent_initial_call=True,
    # )

    @app.callback(Output({'type':'graph-container-data','instance':MATCH}, 'value'),
        Input({'type':'module-commit','instance':MATCH}, component_property='n_clicks'),
        State({'type':'module-commit','instance':MATCH}, 'id'),
    )
    def commit_log(n_clicks,id):
        modulename = str(int(id['instance']))
        os_path = git.path+modulename+'/'
        #wait for new module generation
        time.sleep(0.05)
        #
        git.git_parse(os_path)
        file_path = os_path+git.expfile
        print(os.getcwd())
        print(file_path)
        return file_path
        
    # if __name__ == "__main__":
    #     app.run_server(debug=True)
    