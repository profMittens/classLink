#!/bin/env python3
import edukit.coreData
import json
import uuid 
import logging
import csv
from collections import namedtuple
inits = edukit.coreData.initializers()

# Set up logging
logging.basicConfig(filename="logs/assignments.log", level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")
logger = logging.getLogger(__name__)

class assignmentManager(edukit.coreData.coreData):
    def __init__(self, className=inits.VAL_DEFAULT_STR, term=inits.VAL_DEFAULT_STR, initalizerInfo=None):
        className = className.lower()
        term = term.lower()
        super().__init__()

        # We are being passed a dictionary that was read from a 
        # json file. Inialize this instance with that info
        if initalizerInfo:
            self.__dict__.update(initalizerInfo)
            for k, v in initalizerInfo.items():
                self.__dict__[k] = v
        else:
            self.className = className
            self.term = term
            self.assignments = []
            self.filePath = "data/assignmentManager-{}-{}.json".format(className, term)

    def saveAssignments(self):
        self.saveObjectToJson(self.filePath, self)

    def addAssignment(self, name, template, points, githubName, dueDate):
        a = {}
        a[inits.KEY_NAME] = name
        a[inits.KEY_TEMPLATE] = template
        a[inits.KEY_POINTS] = points
        a[inits.KEY_GITHUBNAME] = githubName
        a[inits.KEY_DUEDATE] = dueDate
        self.assignments.append(a)        
        self.saveAssignments()

    def printAssignments(self, name, term):
        for a in self.assignments:
            print("Name: {}".format(a[inits.KEY_NAME]))
            print("Tempalte: {}".format(a[inits.KEY_TEMPLATE]))
            print("Points: {}".format(a[inits.KEY_POINTS]))
            print("Github Name: {}".format(a[inits.KEY_GITHUBNAME]))
            print("Due Date: {}".format(a[inits.KEY_DUEDATE]))
            print()

    @staticmethod
    def createAssignmentManager(className, term):
        am = assignmentManager(className, term)
        am.saveAssignments()
        return am
    
    @staticmethod
    def loadAssignments(className, term):
        filePath = "data/assignmentManager-{}-{}.json".format(className, term)
        with open(filePath) as f:
            data = json.load(f)
        return assignmentManager(initalizerInfo = data)