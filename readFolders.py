import os

"""
Reads all nxml files in a folder recusrively
"""
def readAllFiles(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            # skip files that are not nxml
            if os.path.join(root, file)[-5:] != '.nxml':
                continue
            print(os.path.join(root, file))

readAllFiles('C:\\Users\\xgoun\\Desktop\\PROGRAMS\\HY463\\project\\HY463-Project\\Data\\MiniCollection')