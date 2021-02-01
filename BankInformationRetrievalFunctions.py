import pandas as pd
import os
from os import path
import csv
ROOT = path.dirname(path.realpath(__file__))
from AccountClasses import LineItem


def getAllyInformation():
    from main import getCategoryInformation,addToCategoryCSV
    print("Gathering Ally statement information.")

    #Return a dict of all transactions that can later be added to the "Income and Expense.csv"
    returnDict = {}

    categories = getCategoryInformation()
    os.chdir("Statements")
    import csv
    with open('transactions.csv','r', newline='') as inFile:
        reader = csv.reader(inFile)
        for rows in reader:
            if rows[4] == " Description":
                continue
            if rows[4] in categories.keys():
                print(rows[4] + " already has a predetermined category. It is " + categories[rows[4]])
                returnDict[rows[4]] = [rows[0], rows[2], rows[3], categories[rows[4]]]

            else:
                print(rows[4] + " will need a new category.")
                print("What category would you like to give to " + rows[4] +"?")
                newCategory = input(">")
                addCategoryDict = {rows[4]:newCategory}
                addToCategoryCSV(addCategoryDict)
                returnDict[rows[4]] = [rows[0], rows[2], rows[3], newCategory]

    os.chdir(ROOT)
    print("Ally statement information has been acquired.")
    return returnDict


def getChaseInformation(directory):
    try:
        os.chdir("Statements")
    except:
        pass
    returnDict = {}
    # Returns a dataframe of the relevant data in the Ally Spreadsheet(s) spreadsheet
    #Since this statement downloads as a large, complex string, we will simply search the
    #directory and use the first file it finds that has "Chase" in the first five letters
    with open(directory, 'r', newline='') as inFile:
        reader = csv.reader(inFile)
        for rows in reader:
            if rows[4] == "Sale":
                rows[4] = "Expense"
            if rows[4] == "Payment":
                rows[4] = "Expense"

            returnDict[rows[2]] = [rows[0], rows[5], rows[4], rows[3]]

        return returnDict



def getSynchronyInformation(directory):
    try:
        os.chdir("Statements")
    except:
        pass
    returnDict = {}
    # Returns a dataframe of the relevant data in the Ally Spreadsheet(s) spreadsheet
    # Since this statement downloads as a large, complex string, we will simply search the
    # directory and use the first file it finds that has "Chase" in the first five letters
    with open(directory, 'r', newline='') as inFile:
        reader = csv.reader(inFile)
        for rows in reader:
            if rows[4] == "Sale":
                rows[4] = "Expense"
            if rows[4] == "Payment":
                rows[4] = "Expense"

            if rows[5] == "":
                rows[5] = rows[6]

            returnDict[rows[3]] = [rows[0], rows[5], rows[4], rows[3]]

        return returnDict

def getTDBankInformation():
    os.chdir('Statements')
    for directory in os.listdir(os.getcwd()):
        if "Transaction History_" in directory:
            dataframe = pd.read_csv(directory)
            return dataframe


def getDCUInformation():
    os.chdir('Statements')
    # Returns a dataframe of the relevant data in the Ally Spreadsheet(s) spreadsheet
    #os.chdir("Statements")
    dataframe = pd.read_csv("export.csv", skiprows=3)
    return dataframe

def getCapitalOneInformation(directory):
    try:
        os.chdir("Statements")
    except:
        pass
    returnDict = {}
    # Returns a dataframe of the relevant data in the Ally Spreadsheet(s) spreadsheet
    # Since this statement downloads as a large, complex string, we will simply search the
    # directory and use the first file it finds that has "Chase" in the first five letters
    with open(directory, 'r', newline='') as inFile:
        reader = csv.reader(inFile)
        for rows in reader:
            if rows[3] == "Description":
                continue

            if not rows[5]:
                rows[5] = rows[6]

            returnDict[rows[3]] = [rows[0], rows[5], rows[4]]

        return returnDict