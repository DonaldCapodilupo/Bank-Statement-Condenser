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
        if type_Row == "DIVIDEND":
            list_Of_Categories.append("Interest Income")
        else:
            list_Of_Categories.append("Transfer to/from Asset")

    statement["Category"] = list_Of_Categories
    new_statement = statement[["Date", "Amount", "Type", "Description", "Category"]]  # Category

    return new_statement


def capital_One_Statement_To_Dataframe(statement_Name):
    statement = pd.read_csv("Statements/" + statement_Name)

    statement["Amount"] = statement["Debit"].fillna(statement["Credit"])

    list_Of_Categories = []

    new_Statement = statement.drop(["Posted Date", "Card No.", "Debit", "Credit", "Category"], axis=1)

    for row in new_Statement.values:
        description = row[1]
        if "CAPITAL ONE ONLINE PYMT" in description:
            list_Of_Categories.append("Transfer to/form Asset")
        else:
            list_Of_Categories.append("Business Expense")
    new_Statement["Category"] = list_Of_Categories

    return  new_Statement


def vanguard_Investment_Statement_To_Dataframe(statement_Name):
    statement = pd.read_csv("Statements/" + statement_Name, skiprows=8, index_col=False)

    #print(statement)

    statement["Description"] = statement["Investment Name"] + " "  +statement["Transaction Description"]

    statement = statement.drop(["Account Number", "Trade Date", "Investment Name", "Shares", "Share Price",
                                    "Commission Fees", "Net Amount", "Accrued Interest", "Account Type",
                                    "Transaction Description","Symbol", "Investment Name",], axis=1)

    new_Statement = statement[["Settlement Date", "Principal Amount", "Transaction Type", "Description"]]
    print(statement)