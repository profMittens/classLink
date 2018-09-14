#!/usr/bin/env python3

import argparse
import logging
import sys
import os
import shutil
import json
from edukit import classManager
from edukit import studentManager
from edukit import coreData
from edukit import assignmentManager

# Set up logging
logging.basicConfig(filename="logs/classlink.log", level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")
logger = logging.getLogger(__name__)

# Load any defaults
with open("data/defaults.json") as f:
    defaults = json.load(f)

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", help="Name of the class, such as csc300-DataStructure")
    parser.add_argument("-t", "--term", help="Term for the given class, such as fa18")
    parser.add_argument("-cc","--createClass", help="Create a new instance of a class", action='store_true')
    parser.add_argument("-cr","--createRoster", help="Create a new instance of a roster for a class", action='store_true')
    parser.add_argument("-cl","--createAssignmentList", help="Create a new assingment list/manager for a given class")
    parser.add_argument("-ur", "--updateRoster", help="Update the app's roster using a csv file, provide the path to the csv")
    parser.add_argument("-rt", "--rosterType", help="The type of roster csv that is being used. Valid options: wa, gs")
    parser.add_argument("-a","--attr", help="Name of a class attribute to set")
    parser.add_argument("-v","--val", help="The value of a class attribute to set")
    parser.add_argument("-pci","--printClassInfo", help="Print class information for the default class", action='store_true')
    parser.add_argument("-ca","--createAssignment", help="Create a new assignment that will be added to the list", action='store_true' )
    parser.add_argument("-an","--assignmentName", help="Name of the assignment to add")
    parser.add_argument("-at","--assignmentTemplate", help="Name of the template the assignment was created from")
    parser.add_argument("-ap","--assignmentPoints", help="How many points the assignment is worth")
    parser.add_argument("-ag","--assignmentGithubName", help="The name of the assignment as published on github")
    parser.add_argument("-ad","--assignmentDueData", help="The due date for the assignment, in mm/dd/yyyy format")
    parser.add_argument("-pa","--printAssignments", help="Print the assignment list", action="store_true")
    parser.add_argument("-da","--downloadAssignment", help="Download a given assignment from github")
    parser.add_argument("-uh","--updateGithubHandles", help="Update github handles from the specified csv, use -rt to specify csv type")
    return parser.parse_args()

# TODO: add support for adding terms
def createNewClass(name, term):
    logger.info("Creating new class: {} for {}".format(name, term))
    cm = classManager.classManager(name, term)
#    if len(sections) > 0:
#        for s in sections:
#            cm.addSection(s)
    cm.saveClassFile()

def createNewRoster(name, term):
    logger.info("Creating a new roster for {} {}".format(name, term))
    studentManager.rosterManager.createRoster(name, term)

def createNewAssignmentList(name, term):
    logger.info("Creating a new assignment manager for {} {}".format(name, term))
    assignmentManager.assignmentManager.createAssignmentManager(name, term)

def setClassAttr(attr, val, className=None, classTerm=None):
    if className == None or classTerm == None:
        className = defaults["defaultClass"]
        term = defaults["defaultTerm"]
    else:
        className = className
        term = classTerm

    cm = classManager.classManager.loadClass(className, term)
    cm.setAttr(attr, val)
    cm.saveClassFile()
    logger.info("Set a new class attribute: {} to {}".format(attr, val))

def getClassAttr(attr, name=None, term=None):
    if name == None or term == None:
        className = defaults["defaultClass"]
        term = defaults["defaultTerm"]
    else:
        className = name
        term = term

    cm = classManager.classManager.loadClass(className, term)
    val = cm.attrs[attr]
    print("{}: {}".format(attr, val ))

def printClassInfo(cName=None, cTerm=None):
    if cName == None or cTerm == None:
        className = defaults["defaultClass"]
        term = defaults["defaultTerm"] 
    else:
        className = cName
        term = cTerm

    cm = classManager.classManager.loadClass(className, term)
    cm.printClassInfo()

def getRoster(name, term):
    rm = studentManager.rosterManager.loadRoster(name, term)
    return rm

def updateRoster(args):
    rm = getRoster(args.name, args.term)
    rm.updateRoster(args.updateRoster, args.rosterType)

def addAssignment(args):
    am = assignmentManager.assignmentManager.loadAssignments(args.name, args.term)
    am.addAssignment(args.assignmentName, args.assignmentTemplate, args.assignmentPoints, args.assignmentGithubName, args.assignmentDueData)

def printAssignments(args):
    am = assignmentManager.assignmentManager.loadAssignments(args.name, args.term)
    am.printAssignments(args.name, args.term)

def updateHandles(args):
    sm = studentManager.rosterManager.loadRoster(args.name, args.term)
    sm.updateGithubHandles(args.updateGithubHandles, args.rosterType)

def cloneAssignments(args):
    am = assignmentManager.assignmentManager.loadAssignments(args.name, args.term)
    am.cloneAssignments(args.downloadAssignment)

if __name__ == "__main__":
    args = parseArguments()

    if args.printClassInfo:
        printClassInfo(args.name, args.term)
        exit()

    if args.attr and args.val:
        setClassAttr(args.attr, args.val, args.name, args.term)
    elif args.attr:
        getClassAttr(args.attr, args.name, args.term)
    elif args.attr and not args.val or not args.attr and args.val:
        print("useage: -a <attribute> -v <value>")
        exit()

    # Arguments that require the name of the class and the class term
    if args.name and args.term:
        if args.createClass:
            createNewClass(args.name, args.term)
            createNewRoster(args.name, args.term)
            createNewAssignmentList(args.name, args.term)
            exit()
        if args.createRoster:
            createNewRoster(args.name, args.term)
            exit()
        if args.updateRoster:
            if args.rosterType:
                updateRoster(args)
            else:
                print("-ur requires the use of -rt")
            exit()
        if args.createAssignment:
            if not args.assignmentDueData or\
            not args.assignmentGithubName or\
            not args.assignmentName or\
            not args.assignmentPoints or\
            not args.assignmentTemplate:
                print("Useage: ./classlink -n csc300 -t fa18 -ca -an A1 -at a1_template -ap 20 -ag csc300-a1 -ad 09/10/18")
                exit()
            else:
                addAssignment(args)
                exit()
        if args.printAssignments:
            printAssignments(args)
            exit()
        if args.updateGithubHandles:
            if args.rosterType == "gs":
                updateHandles(args)
            else:
                print("Unrecognized csv type")
            exit()
        if args.downloadAssignment:
            cloneAssignments(args)
            exit()