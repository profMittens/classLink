#!/bin/env python3

import json
import datetime
import pickle
from json import JSONEncoder
import json
import enum
from pprint import pprint

class csvFormats(enum.Enum):
    WA = 1

class initializers():
    def __init__(self):
        self.VAL_DEFAULT_STR = "NA"
        self.VAL_DEFAULT_ID = 0
        self.KEY_ZYBOOK_CODE = "zybook_code"
        self.KEY_VM_LINK = "vm_link"
        self.KEY_SLACK_LINK = "vm_link"
        self.STATUS_NEW = "new"
        self.STATUS_DROPPED = "dropped"
        self.STATUS_ACTIVE = "active"
        self.KEY_FNAME = "fname"
        self.KEY_LNAME = "lname"
        self.KEY_EMAIL = "email"
        self.KEY_UUID = "uuid"
        self.KEY_STATUS = "status"
        self.KEY_SECTION = "section"
        self.VAL_WA = "wa"
        self.KEY_NAME = "name"
        self.KEY_TEMPLATE = "template"
        self.KEY_POINTS = "points"
        self.KEY_GITHUBNAME = "githubName"
        self.KEY_DUEDATE = "due_date"
        self.OP_UPDATE_GITHUB_HANDLE = "uh"
        self.KEY_GITHUBHANDLE="github_handle"

class PythonObjectEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (list, dict, str, int, float, bool, type(None))):
            return JSONEncoder.default(self, obj)
        return {'_python_object': pickle.dumps(obj)}

def as_python_object(dct):
    print(dict)
    if '_python_object' in dct:
        return pickle.loads(str(dct['_python_object']))
    return dct

class coreData():
    
    def __init__(self):
        self.attrs = {}
        self.filePath = "NA"

    def setAttr(self, attr, value):
        self.attrs[attr] = value

    def getAttr(self, attr):
        return self.attrs[attr]

    def printAttrs(self):
        for key in self.attrs.keys():
            print(key)

    def saveObjectToJson(self, filePath, obj):
        with open(filePath, 'w') as f:
            json.dump(obj.__dict__, f, cls=PythonObjectEncoder, indent=4)

    def loadJsonObject(self, filePath):
        with open(filePath) as f:
            data = json.load(f, object_hook=as_python_object)
            return data

    def setJsonFilePath(self, filePath):
        self.filePath = filePath