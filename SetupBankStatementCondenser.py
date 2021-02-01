class SetupTool:
    def __init__(self):
        self.neededDirectories = ['Statements']
        setupFiles()


    def directorySetup(self):  # This will ensure that all required files and directories are present before continuing.
        import os
        print("Initializing setup.\n")
        # Create directories
        for directory in self.neededDirectories:
            try:
                # Create target Directory
                os.mkdir(directory)
                print("Directory " + directory + " Created ")
            except FileExistsError:
                print("Directory " + directory + " already exists")
        print("All directories are present.\n")

def setupFiles():
    import csv
    try:
        with open('Categories.csv', newline='') as csvFile:
            pass
    except FileNotFoundError:
        with open('Categories.csv', 'w', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(["Description","Category"])