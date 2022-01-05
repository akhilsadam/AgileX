import os
import subprocess # just to call an arbitrary command e.g. 'ls'
from gga.parse import *

sep = '-'
ext = ".txt"
path = "../Modules/"
title = ""
author = ""


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

def git_init():
    # enter the directory
    with cd(path):
        # subprocess.call("ls")
        state=subprocess.call("git status")
        if state==0:
            print("GIT Repository Exists")
        else:
            subprocess.call("git init")

def git_submodule_init(ospath):
    with cd(ospath):
        subprocess.call("git submodule init")
        subprocess.call("git checkout master")


def git_update(msg):
    subprocess.call("git add .")
    subprocess.call("git commit -m \""+msg+"\"")

def gitparse(ospath):
    json_data = invoke_git_log(limit=0, directory=ospath)
    return parse_json_output(json_data) 

git_init()



