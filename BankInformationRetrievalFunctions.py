import pandas as pd
import os
from os import path
import csv
ROOT = path.dirname(path.realpath(__file__))

def getCategoryInformation():
            import csv
            with open(ROOT+'/Categories.csv', 'r', newline='') as inFile:
                reader = csv.reader(inFile)
                categories = {rows[0]: rows[1] for rows in reader}
            return categories

def addCategoryToCSV(description, category):
    with open('../Categories.csv', 'a') as document:
        document.write(description.replace(",", "") + "," + str(category) + '\n')

def getAllyInformation():

    ally_Statement = pd.read_csv("transactions.csv").replace(["Withdrawal","Deposit"],["Expense","Income"])

    categories_To_Add = []

    known_Categories = getCategoryInformation()

    for description in ally_Statement[" Description"]:
        if "FEDEX" in description and "DDIR" in description:
            categories_To_Add.append("Fedex Income")

        elif description.replace(",","") in known_Categories.keys():
            categories_To_Add.append(known_Categories[description.replace(",","")])
        else:
            print(description + " Does not have a known category")
            print("What is the category?")
            user_Input = input(">")
            with open('../Categories.csv', 'a') as document:
                document.write(description.replace(",","") + "," + user_Input + '\n')
            categories_To_Add.append(user_Input)

    ally_Statement["Categories"] = categories_To_Add
    ally_Statement = ally_Statement.drop([" Time"], axis=1)


    return ally_Statement

#Date, Amount, Type, Description, Category
def getChaseInformation(directory):
    chase_Statement = pd.read_csv(directory).replace(["Sale","Payment"],["Expense","Adjustment"])
    chase_Statement = chase_Statement.drop(["Post Date"], axis = 1)
    chase_Statement = chase_Statement.drop(["Memo"], axis = 1)
    modified_Chase_Statement = pd.DataFrame(
        {
            "Date": list(chase_Statement["Transaction Date"]),
            "Amount": list(chase_Statement["Amount"]),
            "Type":list(chase_Statement["Type"]),
            "Description":list(chase_Statement["Description"]),
            "Category":list(chase_Statement["Category"])
        }
    )

    known_Categories = getCategoryInformation()

    for description, category in zip(chase_Statement["Description"], chase_Statement["Category"]):
        if description.replace(",", "") not in known_Categories.keys():
            addCategoryToCSV(description.replace(",", ""),category)

    modified_Chase_Statement["Category"] = modified_Chase_Statement["Category"].fillna("Pay Down Liability")
    return modified_Chase_Statement

def getCapitalOneInformation(directory):
    capital_One_Statement = pd.read_csv(directory)
    capital_One_Statement = capital_One_Statement.drop(["Posted Date"], axis=1)
    capital_One_Statement = capital_One_Statement.drop(["Card No."], axis=1)
    modified_Capital_One_Statement = pd.DataFrame(
        {
            "Date": list(capital_One_Statement["Transaction Date"]),
            "Amount": capital_One_Statement["Debit"].fillna(capital_One_Statement["Credit"]),
            "Type": list(capital_One_Statement["Description"]),
            "Description": list(capital_One_Statement["Description"]),
            "Category": list(capital_One_Statement["Category"])
        }
    )

    known_Categories = getCategoryInformation()

    for description, category in zip(capital_One_Statement["Description"], capital_One_Statement["Category"]):
        if description.replace(",", "") not in known_Categories.keys():
            addCategoryToCSV(description.replace(",", ""), category)

    return modified_Capital_One_Statement

def getDCUInformation(directory):
    dcu_Statement = pd.read_csv(directory, skiprows=3)

    modified_DCU_Statement = pd.DataFrame(
        {
            "Date": list(dcu_Statement["Date"]),
            "Amount": dcu_Statement["Amount Debit"].fillna(dcu_Statement["Amount Credit"]),
            "Type": list(dcu_Statement["Description"]),
            "Description": list(dcu_Statement["Memo"].replace(["DEPOSIT","WITHDRAWAL","DIVIDEND"],["Transfer From Asset","Expense","Dividend Income"]))
        }
    )

    categories_To_Add = []
    known_Categories = getCategoryInformation()

    #dcu_Statement["Categories"] = categories_To_Add

    for description in dcu_Statement["Memo"]:
        if str(description).replace(",", "") not in known_Categories.keys():
            print(str(description) + " Does not have a known category")
            print("What is the category?")
            user_Input = input(">")
            addCategoryToCSV(str(description).replace(",", ""), user_Input)
            categories_To_Add.append(user_Input)
        elif str(description).replace(",", "") == 'nan':
            categories_To_Add.append("Yo what the fuck.")
        else:
            categories_To_Add.append(known_Categories[description])
    modified_DCU_Statement["Categories"] = categories_To_Add
    return modified_DCU_Statement

def getTDBankInformation(directory):
    td_Statement = pd.read_csv(directory)
    modified_TD_Statement = pd.DataFrame(
        {
            "Date": list(td_Statement["Date"]),
            "Amount": list(td_Statement["Amount"]),
            "Type": list(td_Statement["Activity Type"]),
            "Description": list(td_Statement["Merchant Name"]),
            "Category": list(td_Statement["Merchant Category"])
        }
    )
    return modified_TD_Statement


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






