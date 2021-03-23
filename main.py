import csv
from BankInformationRetrievalFunctions import *

ROOT = path.dirname(path.realpath(__file__))


#Date, Amount, Type, Description, Category

from datetime import datetime

def try_parsing_date(text):
    for fmt in ('%Y-%m-%d','%m/%d/%Y'):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found')


if __name__ == '__main__':
    from SetupBankStatementCondenser import SetupTool

    accountSetup = SetupTool()

    dataframes = []

    os.chdir("Statements")

    for directory in os.listdir(os.getcwd()):
        os.chdir(ROOT)
        os.chdir("Statements")
        if directory == "transactions.csv":
            ally_Statement_Database = getAllyInformation()
            dataframes.append(ally_Statement_Database)

        elif "Chase" in directory:
            print(directory + " is the Chase credit card statement.")
            allChaseTransactions = getChaseInformation(directory)
            print(allChaseTransactions)
            dataframes.append(allChaseTransactions)

        elif "_transaction_download" in directory:
            print(directory + " is the Capital One credit card statement.")
            allCapitalOneTransactions = getCapitalOneInformation(directory)
            dataframes.append(allCapitalOneTransactions)


        elif "Export" in directory:
            print(directory + " is the DCU statement.")
            allDCUTransactions = getDCUInformation(directory)
            dataframes.append(allDCUTransactions)

        elif "Transaction History_" in directory:
            print(directory + " is the TD Bank credit card statement.")
            allTDTransactions = getTDBankInformation(directory)
            dataframes.append(allTDTransactions)


    import numpy as np

    final_Dataframe = pd.DataFrame(np.concatenate(dataframes), columns=dataframes[0].columns)

    fixed_Dates = []



    final_Dataframe = final_Dataframe.sort_values(by='Date')

    for date in final_Dataframe["Date"]:
        fixed_Dates.append(try_parsing_date(date))
    final_Dataframe["Date"] = fixed_Dates


    final_Dataframe.to_csv("../Output_File.csv")



#Open up chrome tabs for the accounts?
#Go into the downloads folder?
#Needs to be able to categorize transactions that don't already have one.
#Change "Sale" and appropriate "Withdrawal" into "Expense". Change "Deposits" into "Income"
#First thing to focus on would be just iterating though all of the statements and outputting a file.
