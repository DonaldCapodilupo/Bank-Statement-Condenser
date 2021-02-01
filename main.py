import csv
from BankInformationRetrievalFunctions import *
from AccountClasses import OutputFile
ROOT = path.dirname(path.realpath(__file__))

def writeToCSV():
    import csv
    csv_file = "Income and Expenses.csv"
    headers = ["Date","Amount","Type"," Description","Category"]
    if os.path.isfile('Income and Expenses.csv'):
        pass
    else:
        with open(csv_file, 'w', newline='') as csvFile:

            writer = csv.writer(csvFile)
            writer.writerow(headers)

#Returns a dictionary of all descriptions and categories present in "Categories.csv"
def getCategoryInformation():
    os.chdir(ROOT)
    with open('Categories.csv','r', newline='') as inFile:
        reader = csv.reader(inFile)
        categories = {rows[0]: rows[1] for rows in reader}
    return categories

#Check to see if the current item is in the dictionary
def checkCategory():
    with open(directory, 'r', newline='') as inFile:
        reader = csv.reader(inFile)
        categories =  {rows[0]:rows[1] for rows in reader}
        return categories

#Adds lines to the categories csv if there is something in the transactions.csv but not in the categories.csv
def addToCategoryCSV(newCategoryDict):
    establishedCategories = getCategoryInformation()

    with open('Categories.csv', 'a', newline='') as inFile:
        writer = csv.writer(inFile)

        for row in newCategoryDict.items():
            if row[0] not in establishedCategories.keys():
                writer.writerow(row)
            else:
                print(row[0] + " has been given a category of " + row[1])

def addToIncomeAndExpenseCSV(dictOfNewItems):
    os.chdir(ROOT)
    with open('Income and Expenses.csv', 'a', newline='') as inFile:
        writer = csv.writer(inFile)

        for description, listOfValues in dictOfNewItems.items():
            writer.writerow([description, listOfValues[0], listOfValues[1], listOfValues[2], listOfValues[3]])




if __name__ == '__main__':
    from SetupBankStatementCondenser import SetupTool
    accountSetup = SetupTool()

    os.chdir("Statements")

    for directory in os.listdir(os.getcwd()):
        if directory == "transactions.csv":
            print(directory + " is the Ally Bank statement.")
            allAllyTransactions = getAllyInformation()
            addToIncomeAndExpenseCSV(allAllyTransactions)


        elif "Chase" in directory:
            print(directory + " is the Chase credit card statement.")
            allChaseTransactions = getChaseInformation(directory)
            addToIncomeAndExpenseCSV(allChaseTransactions)

        elif "_transaction_download" in directory:
            print(directory + " is the Capital One credit card statement.")
            allCapitalOneTransactions = getCapitalOneInformation(directory)
            addToIncomeAndExpenseCSV(allCapitalOneTransactions)


        else:
            print(directory + " is not a reconized statement in the Statements directory..")




    #checkCategory(getCategoryInformation(), getChaseInformation())

    writeToCSV()





#Open up chrome tabs for the accounts?
#Go into the downloads folder?
#Needs to be able to categorize transactions that don't already have one.
#Change "Sale" and appropriate "Withdrawal" into "Expense". Change "Deposits" into "Income"
#First thing to focus on would be just iterating though all of the statements and outputting a file.
