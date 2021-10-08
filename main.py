import csv
from BankInformationRetrievalFunctions import *

#ROOT = path.dirname(path.realpath(__file__))


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
    from Backend import *

    accountSetup = SetupTool()

    list_Of_Statements_As_Dataframes = []

    for statement in os.listdir("Statements"):
        if "Ally" in statement:
            list_Of_Statements_As_Dataframes.append(ally_Statement_To_Dataframe(statement))
        if "Chase" in statement:
            list_Of_Statements_As_Dataframes.append(chase_Statement_To_Dataframe(statement))
        if "DCU" in statement:
            list_Of_Statements_As_Dataframes.append(dcu_Statement_To_Dataframe(statement))
    output_Dataframe = pd.concat(list_Of_Statements_As_Dataframes, ignore_index=True)
    output_Dataframe["Amount"] = output_Dataframe["Amount"].abs()
    output_Dataframe.to_csv("Output.csv")
    print(output_Dataframe)





#Open up chrome tabs for the accounts?
#Go into the downloads folder?
#Needs to be able to categorize transactions that don't already have one.
#Change "Sale" and appropriate "Withdrawal" into "Expense". Change "Deposits" into "Income"
#First thing to focus on would be just iterating though all of the statements and outputting a file.
