import os
import subprocess # just to call an arbitrary command e.g. 'ls'

sep = '-'
ext = ".txt"
path = "../Modules/"
title = ""

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
        subprocess.call("git status")


git_init()