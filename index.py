#!/usr/bin/python3
from flags import Flags
import time
import sys
import getopt
import subprocess
import os
import sys
from sys import platform
from upmcore import python as corepy
from upmindex import python as indexpy
from upmcore import njs as corenjs
from upmindex import njs as indexnjs
from upmcore import ruby as corerb
from upmindex import ruby as indexrb
from upmcore import elisp as coreel
import upmguess as guess
import ctypes
from funcs import *
import requests
from os import system as execa
def run(command):
    return subprocess.check_output(command,shell=True).decode("utf-8")
def execute(c,s=False):


    import subprocess
    process = None
    try:
        bashCommand = c
        bc = bashCommand.split()
        nc = []
        for item in bc:
            item = item.replace("%20"," ")
            nc.append(item)
        process = subprocess.run(c.replace("%20"," "), check=True,text=True)
        o = process.stdout
        if o != None:
            return o
        else:
            return ""
    except Exception as e:
        if str(e).endswith("1.") == False:
            if s == False:
                return e
    return
def execai(c):
    if c.startswith("s:"):
        c = c.replace("s:","")
        return run(c)

    else:
        print(f"--> {c}")
        execute(c)
os.system = execai
def cfg():
    upx = None
    files = []
    for file in os.listdir(os.getcwd()):
        files.append(file)
    if "index.json" in files:
        with open(f"{os.getcwd()}/index.json") as l:
            upx = json.load(l)
    return upx

def all(opt,arg,args):

    list = ["install"]
    for item in args:
        list.append(item)

def isAdmin():
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin



if platform == "win32" or platform == "win64":
    dpath = f"{os.getenv('APPDATA')}/upm"
    path = os.getenv('APPDATA')
elif platform == "linux" or platform == "linux2" or platform == "darwin":
    dpath = "/etc/upm"
    path = "/etc"

files = []
for file in os.listdir(f"{path}/"):
   files.append(file)
if "upm" not in files:
    if isAdmin() == False:
        print("Error: Administrator is required for the first run !")
        sys.exit(1)
    else:

       print("--> Creating data core...")
       os.system(f"cd {path} && mkdir upm")
       os.system(f"cd {path}/upm && mkdir plugins")
       os.system(f"touch {path}/upm/config.json")
       os.system(f"touch {path}/upm/sources.json")
       os.system(f"touch {path}/upm/version.txt")
       with open(f"{path}/upm/config.json","w") as config:
           config.write("{}")
       with open(f"{path}/upm/sources.json","w") as sources:
           sources.write("{}")
       version = requests.request("GET",url="https://k0nami.github.io/upm/version.txt")
       with open(f"{path}/upm/version.txt","w") as ver:
           ver.write(version.text)
       print("--> Created data core !")



def send_help():
    print('USAGE: upm [options]')
    print('A Universal package manager created by k0nami\n')
    print('Basic options:\n')
    print('--language : Pick a language to use\n')
    print('--install  : install package(s)\n')
    print('--remove   : remove package(s)\n')
    print('--list     : list package(s) installed\n')
    print('--info     : get information on a package\n')
    print('--search   : search a package\n')
    print("--lock     : install from the lockfile\n")
    print("--listlangs: list lanuages availiable\n")
    print("--als      : check aliases for lanuages\n")
    print("--guess    : guess the main language\n")
    print("--default  : upm guesses the main language and runs that default installation eg. npm install\n")


advanced = ["language =","help","guess","install =","install","project","remove =","remove","lock","info =","search =","listlangs","als","default","plugin =","dep","dependencies","pm =","init","start"]


def log(c):
    print(f"[Index]: {c}")
def upm():
    x = Flags(sys.argv)
    opt = x.flag
    arg = x.arg
    args = x.args




    if opt in ["-h","help"]:
      send_help()
    if opt in ["get"]:
        if arg == "pip":
            log("Downloading pip...")
            c = requests.get("https://bootstrap.pypa.io/pip/get-pip.py").text
            with open("get-pip.py","w+") as pi:
                pi.write(c)
            log("Updating pip configuration...")
            os.system("s:python3 get-pip.py")
            log("Running Postinstall...")
            print("--> rm -rf get-pip.py")
            os.remove("get-pip.py")
            ver = os.system("s:pip --version").split()[1]
            log(f"Installed pip v{ver}")
        if arg == "poetry":
            log("Downloading poetry...")
            c = requests.get("https://install.python-poetry.org/").text
            with open("get-poetry.py","w+") as pi:
                pi.write(c)
            log("Updating poetry configuration...")
            os.system("s:python3 get-poetry.py")
            log("Running Postinstall...")
            print("--> rm -rf get-poetry.py")
            #os.remove("get-poetry.py")
            #ver = os.system("s:poetry --version").split()[2]
            #log(f"Installed poetry v{ver}")
    if opt in ["-g","guess"]:
        guess.guess()
    if opt in ['-l',"language"]:
      if arg == "py" or arg == "python":
        if "search" == args[0]:
          indexpy.search(args)
        if "li" == args[0] or "list" == args[0]:
            corepy.list()
        if "r" == args[0] or "remove" == args[0]:

            corepy.remover(args)
            add2upm("Python",args)
        if "l" == args[0] or "lock" == args[0]:
            corepy.lock()
        if "i" == args[0] or "install" == args[0] or "add" == args[0]:
            print(args)

            corepy.install(args)
            add2upm("Python",args)
        if "in" == args[0] or "info" == args[0]:
            indexpy.info(args)
      if arg == "njs" or arg == "nodejs":
        if "search" == args[0]:
          indexnjs.search(args)
        if "li" == args[0] or "list" == args[0]:
            corenjs.list()
        if "r" == args[0] or "remove" == args[0]:
            corenjs.remover(args)
            add2upm("Nodejs",args)
        if "i" == args[0] or "install" == args[0] or "add" == args[0]:

            corenjs.install(args)
            add2upm("Nodejs",args)
        if "in" == args[0] or "info" == args[0]:
            indexnjs.info(args)
      if arg == "rb" or arg == "ruby":
        if "search" == args[0]:
          indexrb.search(args)
        if "li" == args[0] or "list" == args[0]:
            corerb.list()
        if "r" == args[0] or "remove" == args[0]:

            corerb.remover(args)
            add2upm("Ruby",args)
        if "i" == args[0] or "install" == args[0] or "add" == args[0]:

            corerb.install(args)
            add2upm("Ruby",args)
        if "in" == args[0] or "info" == args[0]:
            indexrb.info(args)
      if arg == "el" or arg == "elisp":
        if "li" == args[0] or "list" == args[0]:
            coreel.list()
        if "r" == args[0] or "remove" == args[0]:

            coreel.remover(args)
            add2upm("Elisp",args)
        if "i" == args[0] or "install" == args[0] or "add" == args[0]:

            coreel.install(args)
            add2upm("Elisp",args)
    if opt in ["init"]:
        temp = """
{
"Name": "Enter package name",
"Author(s)": ["author1","author2","author3"],
"Description": "An example package...",
"Version": "0.0.1",
"Run": "echo please enter a run script",
"Main_file": "used to guess imports",
"Python": [],
"Nodejs": [],
"Ruby": [],
"Elisp": []
}
        """
        print("--> Creating index.json...")
        os.system("touch index.json")
        with open(f"{os.getcwd()}/index.json","w") as x:
            x.write(temp)
    if opt in ["imports"]:
        tp = ""
        lang = guess.alz()
        f = arg
        if lang == "python":
            if cfg()["Main_file"] != "used to guess imports":
                f = cfg()["Main_file"]

            for i in corepy.guess_import(f):
                if i == corepy.guess_import(f)[-1]:
                    tp += f"{i}"
                else:
                    tp += f"{i}, "
            print(tp)

    if opt in ["-imp","import"]:
        lang = guess.alz()
        f = arg
        if lang == "python":
            if cfg()["Main_file"] != "used to guess imports":
                f = cfg()["Main_file"]
            ex = ""


            opt = "install"
            arg = ""
            args = [*corepy.guess_import(f),*args]


    if opt in ["-i","install"]:
        files = []

        list = ["install"]
        if arg == "":
            pass
        else:
            list.append(arg)
        for item in args:
            list.append(item)
        lang = guess.alz()
        if lang == "python":
            corepy.install(list)
        if lang == "njs":
            corenjs.install(list)
        if lang == "rb":
            corerb.install(list)
    if opt in ["-c","lock"]:
        lang = guess.alz()
        if lang == "python":
            corepy.lock()
        if lang == "njs":
            corenjs.lock()
        if lang == "rb":
            corerb.lock()
    if opt in ["-dep","dependencies"]:
        lang = guess.alz()
        if lang == "python":
            corepy.list()
        if lang == "njs":
            corenjs.list()
        if lang == "rb":
            corerb.list()
    if opt in ["-r","remove"]:
        list = ["remove"]
        list.append(arg)
        for item in args:
            list.append(item)
        lang = guess.alz()
        if lang == "python":
            corepy.remover(list)
        if lang == "njs":
            corenjs.remover(list)
        if lang == "rb":
            corerb.remover(list)
    if opt in ["-n","info"]:
        list = ["info"]
        list.append(arg)
        for item in args:
            list.append(item)
        lang = guess.alz()
        if lang == "python":
            indexpy.info(list)
        if lang == "njs":
            indexnjs.info(list)
        if lang == "rb":
            corerb.info(list)
    if opt in ["-s","search"]:
        list = ["search"]
        list.append(arg)
        for item in args:
            list.append(item)
        lang = guess.alz()
        if lang == "python":
            indexpy.search(list)
        if lang == "njs":
            indexnjs.search(list)
        if lang == "rb":
            corerb.search(list)
    if opt in ["listlangs"]:
        print("Python (Poetry)\nNodejs (Npm)")
    if opt in ["alias","aliases"]:
        print("Aliases[python]: [python,py]")
        print("Aliases[nodejs]: [njs,nodejs]")
        print("Aliases[ruby]  : [rb,ruby]")
    if opt in ["-d","default"]:
        list = ["install"]
        for item in args:
            list.append(item)
        lang = guess.alz()
        if lang == "python":
            corepy.install(list)
        if lang == "njs":
            corenjs.install(list)
        if lang == "rb":
            corerb.install(list)
    if opt in ["-p","plugin"]:
        plugins = []
        for file in os.listdir(f"{dpath}/plugins"):
            plugins.append(file)
        if args[0] not in plugins:
            return print("[Index]: Plugin not found.")
        else:
            output = ""
            for item in args:
                if item != args[0]:
                    output += f" {item}"
            os.system(f"cd {dpath}/plugins && python {args[0]}{output}")
    if opt in ["source","-so"] or sys.argv[1] in ["-a","pm"]:
        if isAdmin() == False:
            return print("Error: Administrator is required for sources")
        if "add" == arg or "+" == arg:
            if args == []:
                return print("Error: Please include add arguments eg. upm source add <alias> <link to source>")
            addsrc(dpath,args[0],args[1])
        if "remove" == arg or "-" == arg:
            if args == []:
                return print("Error: Please include add arguments eg. upm source remove <alias>")
            removesrc(dpath,args[0])
        if "update" == arg:
            update(dpath)
    if opt in ["start"] or sys.argv[1] in ["start"]:
        upx = cfg()
        torun = upx["Run"]
        print(f"""--> Running: "{torun}" """)
        os.system(torun)

try:
    version = requests.request("GET",url="https://n30nyx.github.io/upm/version.txt")
    version = version.text
    version = version.replace("\n","")
    version  =version.replace(" ","")
    version = int(version)
    f = open(f"{dpath}/version.txt","r")
    content = f.read()
    content = content.replace("\n","")
    content  = content.replace(" ","")
    content = int(content)
    if version > content:
        print("-----\nAn update is availiable! Please type upm --update or get it manually from the github repo.\n-----")
except:
    ok = "ok"

upm()
