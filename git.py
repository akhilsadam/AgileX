import os
import subprocess
from gga.parse import *

#if you change these, change the corresponding variables in gitgraph_clientside.mjs !

sep = '-'
ext = ".txt"
expfile = "export.json"
path = "assets/Modules/" 
title = ""
author = ""

testing = True


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
            print("GIT Repository Exists; remove repo ?")
            if testing :
                print("Removing as part of testing...")
                os.system("rm -R .git")
                subprocess.call("git init")
            else:
                print("Not removing...")
        else:
            subprocess.call("git init")

def git_submodule_init(ospath):
    with cd(ospath):
        subprocess.call("git submodule init")
        subprocess.call("git checkout master")


def git_update(ospath,msg):
    with cd(ospath):
        subprocess.call("git add .")
        subprocess.call("git commit -m \""+msg+"\"")

def git_parse(ospath):
    with cd(ospath):
        os.system("git2json > " + expfile)
    return
        # p = subprocess.Popen(['git2json'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # output, err = p.communicate(b"input data that is passed to subprocess' stdin")
        # rc = p.returncode
        # out = output[:len(output)-5]
    # json_data = invoke_git_log(limit=0, directory=ospath)
    # return parse_json_output(json_data) 

git_init()



