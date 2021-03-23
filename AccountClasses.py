class Account_Item:
    def __init__(self, date, description, amount, expense=True):
        self.date = date
        self.description = description
        self.amount = amount
        self.category = self.get_Category()




    def get_Category(self):
        def getCategoryInformation():
            import csv
            with open('Categories.csv', 'r', newline='') as inFile:
                reader = csv.reader(inFile)
                categories = {rows[0]: rows[1] for rows in reader}
            return categories

        current_Categories = getCategoryInformation()

        for key, value in current_Categories.items():
            if key ==self.description:
                return value

        print("Category not found for " + self.description + ".")
        print("Please provide a new category.")
        new_Category = input(">")

        with open('Categories.csv', 'a') as document:
            document.write(self.description + "," + new_Category + '\n')

        return new_Category

    def addToOutputCSV(self):
        pass





















class LineItem:
    def __init__(self, date, description, amount, category, expense = True):
        self.date = date
        self.description = description
        self.amount = amount
        self.category = category
        if self.expense:
            self.expense = "Expense"
        else:
            self.expense = "Income"

