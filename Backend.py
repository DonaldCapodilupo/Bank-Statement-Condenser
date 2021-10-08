import pandas as pd
import csv, re

pd.set_option("display.max_rows", None, "display.max_columns", None)

pattern_Categories = {
    "MARK ONE": "Mark One Income",
    "FEDEX": "Fedex Income",
    "eCheck Deposit": "Misc Income",
    "EXPRESS SERVICES": "Mark One Income",
    "TAX REF": "Misc Income",
    "MASTTAXRFD": "Misc Income",
    "TD BANK PAYMENT": "Pay Down Liability",
    "Mturk": "Mturk Income",
    "INDUSTRIAL STREET": "Marijuana",
    "Interest Pa": "Interest Income",
    "66 INDUSTRIAL AVE": "Marijuana",
    "PATCARE": "Marijuana",
    "ATM Fee Reimbursement": "Reduce Expense",
    "COINBASE": "Transfer to Asset",
    "INDUSTRIAL AVE": "Marijuana",
    "CAPITAL ONE": "Pay Down Liability",
    "CHASE CREDIT CRD EPAY": "Pay Down Liability",
    "PAYMENT FOR AMZ STORECARD": "Pay Down Liability",
    "transfer to": "Transfer to/from Account",
    "transfer from": "Transfer to/from Account",
    "VANGUARD SELL INVESTMENT": "Transfer to/from Account",
    "VANGUARD BUY INVESTMENT": "Transfer to/from Account",
    "ALLY BANK $TRANSFER": "Transfer to/from Account",


}

dcu_Pattern_Categories = {"TRANSFER": "Transfer to/from Account"}


def add_New_Specific_Category(description):
    print("What category would you give to " + description + " ?")
    new_Category = input(">")
    with open('Categories.csv', 'a', newline='') as doc:
        writer = csv.writer(doc)
        writer.writerow([description, new_Category])
    return new_Category

def check_Hard_Coded_Categories(description):
    for pattern in pattern_Categories.keys():
        if re.search(pattern, description):
            print(
                description + " is close enough to a income and has been given a category of: " +
                pattern_Categories[pattern])
            return pattern_Categories[pattern]

def check_Specific_Categories_CSV(categories_Dataframe, description):
    desired_Row = categories_Dataframe.loc[categories_Dataframe['Description'] == description].values
    print("Category found for " + description + ". " + desired_Row[0][1])
    return desired_Row[0][1]


def get_Categories(description):
    categories = pd.read_csv("Categories.csv")

    #Check hardcoded, regex descriptions
    if check_Hard_Coded_Categories(description):
        return check_Hard_Coded_Categories(description)

    #Check specific categories in Categories.csv
    elif description in categories["Description"].values:
        return check_Specific_Categories_CSV(categories, description)
        # See if its a common item

    else:
        #No category, create one and add it to Categories.csv
        print("Did not find a match for: " + description)
        return add_New_Specific_Category(description)


def ally_Statement_To_Dataframe(statement_Name):
    statement = pd.read_csv("Statements/" + statement_Name)
    statement = statement.drop(columns=[" Time"])

    list_Of_Categories = []

    # Categorize Transactions
    for row in statement.values:
        description = row[3]
        list_Of_Categories.append(get_Categories(description))

    statement["Category"] = list_Of_Categories
    statement = statement.rename(columns={" Amount": "Amount",
                                          " Type": "Type",
                                          " Description": "Description"})

    return statement


def chase_Statement_To_Dataframe(statement_Name):
    statement = pd.read_csv("Statements/" + statement_Name)

    #Organize Columns
    # Date, Amount, Type, Description, Category
    new_statement = statement[["Transaction Date", "Amount", "Type", "Description", "Category"]]

    #No need to add categories, this statement already has a "Category" column.

    #Reorganize columns
    new_statement = new_statement.rename(columns={"Transaction Date": "Date"})

    return new_statement


def dcu_Statement_To_Dataframe(statement_Name):
    statement = pd.read_csv("Statements/" + statement_Name, skiprows=3)


    statement["Amount"] = statement["Amount Debit"].fillna(statement["Amount Credit"])

    statement = statement.drop(
        ["Transaction Number", "Balance", "Amount Debit", "Amount Credit", "Check Number", "Fees  "], axis=1)

    statement = statement.rename(columns={"Description": "Type", "Memo": "Description"})

    list_Of_Categories = []

    for row in statement.values:
        type_Row = row[1]  # If Div - Category = interest income
        description = row[2]
        if type_Row == "DIVIDEND":
            list_Of_Categories.append("Interest Income")
            continue
        elif description in dcu_Pattern_Categories.keys():
            for pattern in dcu_Pattern_Categories.keys():
                if re.search(pattern, description):
                    print(
                        description + " is close enough to a income and has been given a category of: " +
                        dcu_Pattern_Categories[pattern])
                    list_Of_Categories.append(dcu_Pattern_Categories[pattern])
                    continue
        else:
            list_Of_Categories.append(get_Categories(description))

    new_statement = statement[["Date", "Amount", "Type", "Description", ]]  # Category

    print(new_statement)
