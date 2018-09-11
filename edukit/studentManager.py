#!/bin/env python3
import edukit.coreData
import json
import uuid 
import logging
import csv
from collections import namedtuple
inits = edukit.coreData.initializers()

# Set up logging
logging.basicConfig(filename="logs/roster.log", level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")
logger = logging.getLogger(__name__)

class rosterManager(edukit.coreData.coreData):
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
            self.roster = []
            self.filePath = "data/rosterManager-{}-{}.json".format(className, term)

    def saveRoster(self):
        self.saveObjectToJson(self.filePath, self)

    def addStudent(self, fname, lname, email, status, section):
        self.roster.append({})
        s = self.roster[-1]
        s[inits.KEY_FNAME] = fname
        s[inits.KEY_LNAME] = lname
        s[inits.KEY_EMAIL] = email
        s[inits.KEY_STATUS] = inits.STATUS_NEW
        s[inits.KEY_GITHUBHANDLE] = inits.VAL_DEFAULT_STR
        
    def studentIsInRoster(self, fname, lname, fileData=None):
        if fileData == None:
            r = self.roster
        else:
            r = fileData

        for s in r:
            if s[inits.KEY_FNAME] == fname and s[inits.KEY_LNAME] == lname:
                return True
        return False

    def processWaCsv(self, csvPath):
        FULLNAME = 1
        EMAIL = 4
        data = []
        roster = []

        with open(csvPath) as f:
            reader= csv.reader(f)
            for row in reader:
                data.append(row)

        # Restructure the data into a standard dictionary 
        # that the updateRoster function will use
        for s in data:
            full_name = s[FULLNAME]
            email = s[EMAIL]

            # The name comes in as <Last>, <First> <MI>. so split that up
            lname = full_name.split(',')[0]
            fname = full_name.split(',')[1].split(' ')[1]

            _s = {}
            _s[inits.KEY_FNAME] = fname
            _s[inits.KEY_LNAME] = lname
            _s[inits.KEY_EMAIL] = email
            roster.append(_s)

        return roster

    def updateRoster(self, csvPath, csvType):
        if csvType.lower() == inits.VAL_WA.lower():
            updatedRoster = self.processWaCsv(csvPath)
        else:
            msg = "Unsupported csv type: {}".format(csvType)
            logger.error(msg)
            print(msg)
        
        # Check for any new students
        rosterChanged = False
        for s in updatedRoster:
            fname = s[inits.KEY_FNAME]
            lname = s[inits.KEY_LNAME]
            email = s[inits.KEY_EMAIL]
            if not self.studentIsInRoster(fname, lname):
                rosterChanged = True
                msg = "Adding {} {} to the roster".format(fname, lname)
                logger.info(msg)
                print(msg)
                self.addStudent(fname, lname, email, inits.STATUS_NEW, inits.VAL_DEFAULT_STR)

        # Check for any withdrawls, if a student is in our roster but not in 
        # the updated file then they dropped
        for s in self.roster:
            fname = s[inits.KEY_FNAME]
            lname = s[inits.KEY_LNAME]
            email = s[inits.KEY_EMAIL]

            if not self.studentIsInRoster(fname, lname, updatedRoster):
                rosterChanged = True
                s[inits.KEY_STATUS] = inits.STATUS_DROPPED
                msg = "{} {} dropped".format(fname, lname)
                logger.info(msg)
                print(msg)

        if rosterChanged:
            self.saveRoster()

    def getStudent(self, fname, lname):
        for s in self.roster:
            if s[inits.KEY_FNAME] == fname and s[inits.KEY_LNAME] == lname:
                return s
        return None

    @staticmethod
    def createRoster(className, term):
        rm = rosterManager(className, term)
        rm.saveRoster()
        return rm
    
    @staticmethod
    def loadRoster(className, term):
        filePath = "data/rosterManager-{}-{}.json".format(className, term)
        with open(filePath) as f:
            data = json.load(f)
        return rosterManager(initalizerInfo = data)
