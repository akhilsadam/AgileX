import email
import os
import subprocess
from sys import modules

#if you change these, change the corresponding variables in gitgraph_clientside.mjs, gitgraph.umd.js, codemir.js!

sep = '-'
ext = ".txt"
expfile = "export.json"
path = "AgileX/static/Modules/" 
dpath = "/static/Modules/" 
pathWT = "AgileX/static/ModuleWT/" 
rpathWT = "../../ModuleWT/"
latexpath = "AgileX/static/"
latexcmd = "sh compile.sh "
latexcmdexp = "sh compilePDF.sh "
title = ""
author = ""

name = "Akhil Sadam"
ead = "sadam.akhil@gmail.com"

testing = False

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
        subprocess.call("git init")
        subprocess.call("git checkout master")


def git_sub_init(modulename,msg):
    ospath = path+modulename+'/'
    with cd(ospath):
        os.system("git config user.email \""+ead+"\"")
        os.system("git config user.name \""+name+"\"")
        subprocess.call("git add .")
        subprocess.call("git commit -m \""+msg+"\"")      
    git_parse(ospath)

def git_update(modulename,msg):
    ospath = path+modulename+'/'
    with cd(ospath):
        chb = str(subprocess.check_output("git rev-parse --short HEAD", shell=True))
        # print(chb)
        commit_hash = chb[2:len(chb)-3]
        bnb = str(subprocess.check_output("git rev-parse --short HEAD", shell=True))
        print(bnb)
        branchname = bnb[2:len(bnb)-3]
        print(branchname)
        # print(commit_hash)
        mpath = rpathWT+modulename+sep+commit_hash+'/'
        print(mpath)
        os.system("git worktree add "+mpath+" "+branchname)
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

def latex_run(modulename):
    with cd(latexpath):
        os.system(latexcmd+modulename)
    return

def latex_export(modulelist):
    with cd(latexpath):
        os.system(latexcmdexp+' '.join(modulelist))
    return

git_init()



