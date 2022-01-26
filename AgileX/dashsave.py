# -*- coding: utf-8 -*-
import os
from html.parser import HTMLParser
import re

import dash
import pandas as pd
import plotly.express as px
import requests
from dash import html, dcc, dash_table, Input, Output
from . import git

def patch_file(file_path: str, content: bytes, extra: dict = None) -> bytes:
    if file_path == 'index.html':
        index_html_content = content.decode('utf8')
        extra_jsons = f'''
        var patched_jsons_content={{
        {','.join(["'/" + k + "':" + v.decode("utf8") + "" for k, v in extra.items()])}
        }};
        '''
        patched_content = index_html_content.replace(
            '<footer>',
            f'''
            <footer>
            <script>
            ''' + extra_jsons + '''
            const origFetch = window.fetch;
            window.fetch = function () {
                const e = arguments[0]
                if (patched_jsons_content.hasOwnProperty(e)) {
                    return Promise.resolve({
                        json: () => Promise.resolve(patched_jsons_content[e]),
                        headers: new Headers({'content-type': 'application/json'}),
                        status: 200,
                    });
                } else {
                    return origFetch.apply(this, arguments)
                }
            }
            </script>
            '''
        ).replace(
            'href="/',
            'href="'
        ).replace(
            'src="/',
            'src="'
        ).replace(
            'href="dashapp/',
            'href="'
        ).replace(
            'src="dashapp/',
            'src="'
        ).replace(
            'href="/codefence',
            'href="//codefence'
        ).replace(
            'src="/codefence',
            'src="//codefence'
        )

        patched_content = re.sub(r'\?m=[0-9]*\.[0-9]+', '', patched_content)

        return patched_content.encode('utf8')
    else:
        return content


def write_file(file_path: str, content: bytes, target_dir='target', ):
    target_file_path = os.path.join(target_dir, file_path.lstrip('/').split('?')[0])
    print("FP",target_file_path)
    if 'https' not in target_file_path:
        target_leaf_dir = os.path.dirname(target_file_path)
        os.makedirs(target_leaf_dir, exist_ok=True)
        with open(target_file_path, 'wb') as f:
            f.write(content)
        pass


class ExternalResourceParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.resources = []

    def handle_starttag(self, tag, attrs):
        if tag == 'link':
            for k, v in attrs:
                if k == 'href':
                    self.resources.append(v)
        if tag == 'script':
            for k, v in attrs:
                if k == 'src':
                    self.resources.append(v)


def make_static(base_url, target_dir='target'):
    index_html_bytes = requests.get(base_url).content
    json_paths = ['_dash-layout', '_dash-dependencies', ]
    extra_json = {}
    for json_path in json_paths:
        json_content = requests.get(base_url + json_path).content
        extra_json[json_path] = json_content

    patched_bytes = patch_file('index.html', index_html_bytes, extra=extra_json)
    write_file('index.html', patched_bytes, target_dir)
    parser = ExternalResourceParser()
    parser.feed(patched_bytes.decode('utf8'))
    extra_js = [
        'assets/custom.css',
        'assets/default.css',
        'assets/scrollbar.css',
        'assets/style.css',
        '_dash-component-suites/dash/dcc/async-graph.js',
        '_dash-component-suites/dash/dcc/async-plotlyjs.js',
        '_dash-component-suites/dash/dash_table/async-table.js',
        '_dash-component-suites/dash/dash_table/async-highlight.js',
        '_dash-component-suites/dash/deps/polyfill@7.v2_0_0m1641225909.12.1.min.js',
        '_dash-component-suites/dash/deps/react@16.v2_0_0m1641225909.14.0.min.js',
        '_dash-component-suites/dash/deps/react-dom@16.v2_0_0m1641225909.14.0.min.js',
        '_dash-component-suites/dash/deps/prop-types@15.v2_0_0m1641225909.7.2.min.js',
        '_dash-component-suites/visdcc/bundle.v0_0_40m1642778341.js',
        '_dash-component-suites/dash_dangerously_set_inner_html/bundle.v0_0_2m1642546796.js',
        '_dash-component-suites/dash_colorscales/bundle.v0_0_4m1641226142.js',
        '_dash-component-suites/dash_extensions/dash_extensions.v0_0_67m1642821322.min.js',
        'assets/codemir.js',
        'assets/default.js',
        'assets/gitgraph.umd.js',
        'assets/gitgraph_clientside.mjs',
        'assets/require.js',
        '_dash-component-suites/dash/dash-renderer/build/dash_renderer.v2_0_0m1641225909.min.js',
        '_dash-component-suites/dash/dcc/dash_core_components.v2_0_0m1641225909.js',
        '_dash-component-suites/dash/dcc/dash_core_components-shared.v2_0_0m1641225909.js',
        '_dash-component-suites/dash/html/dash_html_components.v2_0_0m1641225910.min.js',
        '_dash-component-suites/dash/dash_table/bundle.v5_0_0m1641225909.js',
        '_dash-component-suites/dash_extensions/dash_extensions.min.js.map',
        '_dash-component-suites/dash/dcc/dash_core_components.js.map',
        '_dash-component-suites/dash/html/dash_html_components.min.js.map',
        '_dash-component-suites/dash/dcc/dash_core_components-shared.js.map',
        '_dash-component-suites/dash/dash_table/bundle.js.map',
        'assets/custom.css.map',
        '_dash-dependencies',
        '_dash-layout'
    ]
    for resource_url in parser.resources + extra_js:
        resource_url_full = base_url + resource_url
        print(f'get {resource_url_full}')
        resource_bytes = requests.get(resource_url_full).content
        patched_bytes = patch_file(resource_url, resource_bytes)
        write_file(resource_url, patched_bytes, target_dir)
    with git.cd("target"):
        os.system("mkdir dashapp")
        os.system("mv * dashapp/")
        os.system("mv assets/* dashapp/assets/")

