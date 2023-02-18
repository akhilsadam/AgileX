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
from dash.html import Kbd as Keyboard
import dash_dangerously_set_inner_html
# from mni import create_mesh_data, default_colorscale
import time
import visdcc
from . import git
from .dashsave import *

suptitle = "workbench"
port = 9050

GITHUB_LINK = os.environ.get(
    "GITHUB_LINK",
    "https://github.com/akhilsadam/AgileX",
)

current_path = os.getcwd()
reg_prefix = '/'
dash_prefix = '/dashapp/'
spfold = '.git'

def getfiles():
    return [f.replace(git.ext,"") for f in listdir(git.path) if (not isfile(join(git.path, f)) and spfold not in f)]
modules = []
moduleID = 0

def init_dashboard(server):

    app = dash.Dash(
        server = server,
        routes_pathname_prefix=dash_prefix,
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
            <link href="//codefence.io/codefence.css" rel="stylesheet">
            <script defer type="text/javascript" src="//codefence.io/codefence.js"></script>
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
                                    html.Div([],className="avance-reculer"),
                                ],
                                className="top",
                            ),
                            """
    backend = \
    """                
                                html.Div(
                                    [
                                        html.Div(dcc.Input(id='module-new-submit', type='text', value='0')),
                                        html.Button('Add Module', id='module-new', type="button", n_clicks=0, style={'display': 'block'}),
                                        html.Button('PDF Export', id='module-pdf', type="button",n_clicks=0, style={'display': 'block'}),
                                        html.Button('Static Site Export', id='module-ss', type="button",n_clicks=0, style={'display': 'block'}),
                                        html.Span('', id='saved'),
                                    ],
                                    className="module-add",
                                    style={'display': 'flex','flex-direction': 'row','padding-left':'2em'},
                                ),
                                dcc.Store(id="annotation_storage"),
                                dcc.Location(id='url', refresh=True),
                                dcc.Location(id='url4', refresh=True),
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
                                                            Keyboard(id={'type':'module-input-key','instance':moduleid}),
                                                            dash_dangerously_set_inner_html.DangerouslySetInnerHTML('''
<code-fence lang='r' switcher='false' heading='LaTeX moduleid' style='word-wrap: break-word; word-break: break-word; width:100%;overflow-x:wrap;'>
    <textarea vue-slot='code' id='{'type':'module-input-code-area','instance':moduleid}' class='module-input-code-area' style='word-wrap: break-word; word-break: break-word;'>moduletext</textarea>
</code-fence>
                                                            '''),
                                                            #dcc.Textarea(id={'type':'module-input-code','instance':moduleid},className='module-input-code', value='', readOnly=True, style={'width': '100%'}),
                                                            #dcc.Input(id={'type':'module-input-code','instance':moduleid},className='module-input-code', value='', type='text', readOnly=False, style={'width': '100%'}),
                                                            # <input id='{'instance':moduleid,'type':'module-input-code'}' class='module-input-code'  value=''  type='text' readOnly=False style='width: 100%;'></input>
                                                            html.Data(id={'type':'module-input-code','instance':moduleid},className='module-input-code', value='''moduletext''', contentEditable=False, style={'width': '100%','display':'none'}),
                                                            visdcc.Run_js(id={'type':'module-input-refresh','instance':moduleid}, run = ''),
                                                        ],
                                                        className='module-input-change',
                                                        id={'type':'module-input-change','instance':moduleid},
                                                    ),
                                                    html.Div(
                                                        [
                                                            html.Hr([],className='hr', style={'z-index':'-2','position':'absolute'}),
                                                            html.Button('Save to HEAD', id={'type':'module-save','instance':moduleid}, type='button', n_clicks=0, className='module-save', style={'display': 'block'}),
                                                            html.Div([
                                                                dcc.Textarea(id={'type':'commit-text','instance':moduleid}, value='', readOnly=False, className='commit-text', style={'height':'38px','margin':'0px','background-color':'rgba(0,0,0,0.6)'}),
                                                            ], className='commit-text-div',),
                                                            html.Button('Commit',id={'type':'module-commit','instance':moduleid}, type='button', n_clicks=0,className='module-commit', style={'display': 'block'}),
                                                            html.Button('Branch',id={'type':'module-branch','instance':moduleid}, type='button', n_clicks=0,className='module-branch', style={'display': 'block'}),
                                                            html.Button('Checkout',id={'type':'module-check','instance':moduleid}, type='button', n_clicks=0,className='module-check', style={'display': 'block'}),
                                                            html.Button('Stash',id={'type':'module-stash','instance':moduleid}, type='button', n_clicks=0,className='module-stash', style={'display': 'block'}),
                                                        ],
                                                        className="module-button",
                                                        id={'type':'module-button','instance':moduleid},
                                                        style={'display': 'flex','flex-direction': 'row'},
                                                    ),
                                                    html.A(id={'type':'url2','instance':moduleid}, style={'visibility':'hidden','width': '0%','display': 'none','height': '0%'}),
                                                ],
                                                className="module-input",
                                                id={'type':'module-input','instance':moduleid},
                                                style={'display': 'block','width': '100%'}
                                            ),
                                            html.Div(
                                                [
                                                    #dcc.Textarea(id={'type':'my-output','instance':moduleid}, value='', readOnly=True, style={'width': '100%','whiteSpace': 'pre-line'}),
                                                    html.Iframe(id={'type':'my-output','instance':moduleid},src=git.dpath+modulename+'/'+'currentTex.html', className="embeds", style={'width': '100%','whiteSpace': 'pre-line'}),
                                                ],
                                                #className="grow-wrap",
                                                className="wrap",
                                            ),
                                        ],
                                        className="element two-thirds column",
                                        style={'overflow-x':'hidden'},
                                    ),
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Div(
                                                        [
                                                            html.H6("HEAD : "+moduleid,className="checkout"),
                                                            dcc.Input(id={'type':'state','instance':moduleid},className="state", value='statetext'),
                                                        ],
                                                        className="title",
                                                        id={'type':'title','instance':moduleid},
                                                    ),
                                                    html.Div(
                                                        [
                                                            html.Div(
                                                                [
                                                                ],
                                                                id={'type':'graph-container','instance':moduleid},
                                                                className="graph-container",
                                                            ), 
                                                        ],
                                                        className="mixblende",
                                                    ),
                                                    html.Div(
                                                        [
                                                            # html.Div([],className="avance-recule-circle"),
                                                        ],
                                                        className="avance-recule"
                                                    ),
                                                    dcc.Textarea(id={'type':'graph-container-data','instance':moduleid},className="gcd", value='', readOnly=True, style={'display':'none'}),
                                                    dcc.Location(id={'type':'reset2','instance':moduleid}, refresh=True),
                                                    dcc.Location(id={'type':'reset3','instance':moduleid}, refresh=True),
                                                    dcc.Location(id={'type':'reset4','instance':moduleid}, refresh=True),
                                                ],
                                                className="version-style",
                                            ),
                                        ],
                                        className="version one-third column",
                                    ),
                                ],
                                className="module",
                            ),"""
    #---|_/
    ## html.H4(git.title+modulename),


    # generate app layout
    def serve_layout():
        global modules
        modules = getfiles()
        applayout = frontend + '\n'.join([modular_comp
                                        .replace("moduleid","\""+str(i)+"\"")
                                        .replace("modulename","\""+modules[i]+"\"")
                                        .replace("moduletext",open(git.path+modules[i]+'/'+modules[i]+git.ext, "r").read().replace("\\","\\\\")) 
                                        .replace("statetext",open(git.path+modules[i]+'/'+git.status+git.ext, "r").read()) 
                                        for i in range(len(modules))]) + backend
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
            
# for updating output in realtime
    # @app.callback(Output({'type': 'my-output','instance' : MATCH}, component_property='value'),
    #     Input({'type':'module-input-code','instance' : MATCH}, component_property='value'))
    # def update_module(input_value):
    #     return "{}".format(input_value)

    app.clientside_callback(
        """
        function(n_keydowns,id) {
            console.log("CLIENTSIDE",id);
            var idn = id['instance'];
            var elements2 = document.getElementsByClassName("CodeMirror")[idn];
            console.log(elements2);
            var text = elements2.CodeMirror.doc.getValue();
            return text;
        }
        """,
        Output({'type':'module-input-code','instance' : MATCH}, component_property='value'),
        Input({'type':'module-input-key','instance' : MATCH}, component_property='n_keydowns'),
        State({'type':'module-input-change','instance' : MATCH}, component_property='id')
    )


    @app.callback(Output({'type':'module-input-refresh','instance':MATCH}, "run"),
        Input({'type':'module-save','instance':MATCH}, component_property='n_clicks'),
        State({'type':'module-input-code','instance':MATCH}, 'value'),
        State({'type':'module-input-code','instance':MATCH}, 'id'),
        prevent_initial_call=True,
    )
    def save_module(n_clicks,value,id):
        print("SAVEMODULE : ",value,id)
        modulename = str(int(id['instance']))
        with open(git.path+modulename+'/'+modulename+git.ext, "w") as f:
            f.write(value)
        git.latex_run(modulename)
        return """var ele = document.getElementsByClassName('embeds')["""+modulename+"""];
        ele.contentWindow.location.reload();"""

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
            ospath = git.path+modulename+'/'
            print(ospath)
            try:
                os.mkdir(ospath)
                git.git_submodule_init(ospath)
            except: print("path already exists ...")
            with open(ospath+modulename+git.ext, "a") as f:
                f.write("")
            with open(ospath+git.status+git.ext, "a") as f:
                f.write(git.states[0])
            with open(ospath+git.gitignore, "a") as f:
                f.write(git.expfile)
            git.latex_run(modulename)
            git.git_sub_init(modulename,"new module "+modulename)
            # global modules
            # modules.append(value)
            moduleID+=1
        return dash_prefix

    @app.callback(Output("url4", "href"),
        Input('module-pdf', component_property='n_clicks'),
        prevent_initial_call=True,
    )
    def export_PDF(n_clicks):
        global modules
        git.latex_export(modules)
        return reg_prefix

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
        State({'type':'commit-text','instance':MATCH}, 'value'),
        prevent_initial_call=True,
    )
    def commit_log(n_clicks,id,value):
        modulename = str(int(id['instance']))
        os_path = git.path+modulename+'/'
        #wait for new module generation
        # time.sleep(0.05)
        #
        if value == "":
            value = "empty commit"
        git.git_update(modulename,value)
        git.git_parse(os_path)
        git.latex_run(modulename)
        # print(os.getcwd())
        # print(file_path)
        return os_path+git.expfile

    @app.callback(Output({'type':'reset2','instance':MATCH}, 'href'),
        Input({'type':'module-branch','instance':MATCH}, component_property='n_clicks'),
        State({'type':'module-branch','instance':MATCH}, 'id'),
        State({'type':'commit-text','instance':MATCH}, 'value'),
        prevent_initial_call=True,
    )
    def branch_log(n_clicks,id,value):
        modulename = str(int(id['instance']))
        os_path = git.path+modulename+'/'
        #wait for new module generation
        # time.sleep(0.05)
        #
        if value != "":
            git.git_update_branch(modulename,value)
            git.git_parse(os_path)
            git.latex_run(modulename)
            file_path = os_path+git.expfile
            # print(os.getcwd())
            # print(file_path)
        return dash_prefix
    
    @app.callback(Output({'type':'reset3','instance':MATCH}, 'href'),
        Input({'type':'module-check','instance':MATCH}, component_property='n_clicks'),
        State({'type':'module-check','instance':MATCH}, 'id'),
        State({'type':'commit-text','instance':MATCH}, 'value'),
        prevent_initial_call=True,
    )
    def checkout_log(n_clicks,id,value):
        modulename = str(int(id['instance']))
        os_path = git.path+modulename+'/'
        #wait for new module generation
        # time.sleep(0.05)
        #
        if value != "":
            git.git_checkout(modulename,value)
            git.git_parse(os_path)
        return dash_prefix

    @app.callback(Output({'type':'reset4','instance':MATCH}, 'href'),
        Input({'type':'module-stash','instance':MATCH}, component_property='n_clicks'),
        State({'type':'module-stash','instance':MATCH}, 'id'),
        prevent_initial_call=True,
    )
    def stash_log(n_clicks,id):
        modulename = str(int(id['instance']))
        git.git_stash(modulename)
        return dash_prefix

    @app.callback(Output({'type':'state','instance':MATCH}, "value"),
        Input({'type':'state','instance':MATCH}, component_property='value'),
        State({'type':'state','instance':MATCH}, 'id'),
        State({'type':'state','instance':MATCH}, 'value'),
        prevent_initial_call=True,
    )
    def save_state(n_clicks,id,value):
        # print("SAVEMODULE : ",value,id)
        modulename = str(int(id['instance']))
        try: index = git.states.index(value[:len(value)-1])
        except: index = -1
        newInd = (index+1) % len(git.states)
        newvalue = git.states[newInd]
        with open(git.path+modulename+'/'+git.status+git.ext, "w") as f:
            f.write(newvalue)
        return newvalue
        
    # if __name__ == "__main__":
    #     app.run_server(debug=True)


    #-------------------------------------------------
    @app.callback(
        Output('saved', 'children'),
        Input('module-ss', 'n_clicks'),
    )
    def save_result(n_clicks):
        if n_clicks == 0:
            return 'not saved'
        make_static(f'http://127.0.0.1:{port}/',target_dir='target')
        make_static(f'http://127.0.0.1:{port}/doc/', target_dir='target/doc')
        make_static(f'http://127.0.0.1:{port}/dashapp/', target_dir='target/dashapp')
        return 'saved'
    