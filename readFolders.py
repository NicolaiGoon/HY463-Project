import os


def readAllFiles(folder, callback):
    """
    Reads all nxml files in a folder recusrively and calls the callback function
    """
    for root, dirs, files in os.walk(folder):
        for file in files:
            # skip files that are not nxml
            if os.path.join(root, file)[-5:] != '.nxml':
                continue
            print(os.path.join(root, file))
            callback(os.path.join(root, file))
