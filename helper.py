import pickle
import json


def readProject(name: str):
    with open(f"./.projects/{name}", "rb") as project:
        return pickle.load(project)
    
def saveProject(name:str, data):
    with open(f"./.projects/{name}", "wb") as project:
        pickle.dump(data, project)

def loadJson(dir):
    with open(dir, 'r') as f:
        return json.load(f)

def dumpJson(dir,data):
    with open(dir, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent = 4, ensure_ascii=True)

def genFunc(path, lines):
    with open(path, 'w') as f:
        f.writelines(line + '\n' for line in lines)
