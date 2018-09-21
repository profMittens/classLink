#!/bin/env python3
import edukit.coreData
import json
import uuid 
import logging
import csv
import os
import subprocess
from collections import namedtuple
from edukit.studentManager import rosterManager
inits = edukit.coreData.initializers()

# Set up logging
logging.basicConfig(filename="logs/assignments.log", level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")
logger = logging.getLogger(__name__)

def git(*args):
    return subprocess.check_call(['git'] + list(args))

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

    def cloneAssignments(self, aName):
        keyName = inits.KEY_NAME
        keyBaseName = inits.KEY_GITHUBNAME
        keyHandle = inits.KEY_GITHUBHANDLE
        keyLName = inits.KEY_LNAME
        keyFName = inits.KEY_FNAME

        rm = rosterManager.loadRoster(self.className, self.term)

        aFound = False
        da = None
        for a in self.assignments:
            if a[inits.KEY_NAME] == aName:
                da = a 
                break
            
        if da == None:
            print("No assignment with the name {} was found".format(aName))
            return None
            
        outDir = "data/submissions/{}/{}".format(self.term, aName)
        if not(os.path.isdir(outDir)):
            os.makedirs(outDir)

        msg ="Assignment found, downloading to {}".format(outDir)
        logger.info(msg)
        print(msg)
        for s in rm.roster:
            if s[inits.KEY_STATUS] == inits.STATUS_DROPPED:
                continue
            if s[inits.KEY_GITHUBHANDLE] == inits.VAL_DEFAULT_STR:
                continue
            url = "https://github.com/dsu-cs/{}-{}".format(da[keyBaseName], s[keyHandle])
            aPath = outDir+"/{}_{}_{}_{}".format(da[keyName], s[keyLName], s[keyFName], s[keyHandle])
            git_cmd = "git clone {} {}".format(url, aPath)
            logging.info("Executing: {}".format(git_cmd))
            print("Executing: {}".format(git_cmd))
            try:
                git("clone", url, aPath)
            except:
                logging.error("Clone failed")
                print("Clone failed")
        
        for d in os.listdir(outDir):
            print(d)
            rm_cmd = "rm -rf {}/{}/.git*".format(outDir,d)
            #git_cmd = "git add {}/{}/.git".format(out_dir,d)
            os.system(rm_cmd)
            #os.system(git_cmd)

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