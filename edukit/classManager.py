#!/bin/env python3
import edukit.coreData
import json
from collections import namedtuple

inits = edukit.coreData.initializers()

class classManager(edukit.coreData.coreData):
    
    def __init__(self, className=inits.VAL_DEFAULT_STR, term=inits.VAL_DEFAULT_STR, initalizerInfo = None):
        super().__init__()
        className = className.lower()
        term = term.lower()
        # We are being passed a dictionary that was read from a 
        # json file. Inialize this instance with that info
        if initalizerInfo:
            self.__dict__.update(initalizerInfo)
            for k, v in initalizerInfo.items():
                self.__dict__[k] = v
        else:
            self.className = className
            self.term = term
            self.instructor = inits.VAL_DEFAULT_STR
            self.sections = []
            self.setAttr(inits.KEY_ZYBOOK_CODE, inits.VAL_DEFAULT_STR)
            self.setAttr(inits.KEY_VM_LINK, inits.VAL_DEFAULT_STR)
            self.setAttr(inits.KEY_SLACK_LINK, inits.VAL_DEFAULT_STR)
            self.setJsonFilePath("data/classManager-{}-{}.json".format(className, term))

    def printClassInfo(self):
        print("Class: {}".format(self.className))
        print("Term: {}".format(self.term))
        print("Instructor: {}".format(self.instructor))
        for attr, val in self.attrs.items():
            print("{}: {}".format(attr, val))
        print("Sections: ")
        for s in self.sections:
            print("         {}".format(s))

    def loadClassFile(self):
        return self.loadJsonObject(self.filePath)

    def saveClassFile(self):
        self.saveObjectToJson(self.filePath, self)

    def setClassName(self, className):
        self.className = className.lower()
    
    def setTerm(self, term):
        self.term = term.lower()

    def setInstructor(self, instructor):
        self.instructor = instructor.lower()
    
    def addSection(self, section):
        self.sections.append(section.lower())

    @staticmethod
    def createClass(className, term):
        cm = classManager(className, term)
        cm.saveClassFile()
        return cm
    
    @staticmethod
    def loadClass(className, term):
        className = className.lower()
        term = term.lower()
        filePath = "data/classManager-{}-{}.json".format(className, term)
        with open(filePath) as f:
            data = json.load(f)
        return classManager(initalizerInfo = data)


if __name__ == "__main__":
    cm = classManager.createClass("CSC300", "FA2018")
