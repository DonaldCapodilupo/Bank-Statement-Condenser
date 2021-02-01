class OutputFile:
    def __init__(self, date, description, amount, category, expense = True):
        self.date = date
        self.description = description
        self.amount = amount
        self.category = category
        if self.expense:
            self.expense = "Expense"
        else:
            self.expense = "Income"

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

