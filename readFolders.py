import os
import readxml


def readAllFiles(folder, callback, *extra):
    """
    Reads all nxml files in a folder recusrively and calls the callback function
    """
    for root, dirs, files in os.walk(folder):
        for file in files:
            path = os.path.join(root, file)
            # skip files that are not nxml
            if path[-5:] != '.nxml':
                continue
            doc = readxml.readFileXML(path)
            callback(doc, path, extra[0])
