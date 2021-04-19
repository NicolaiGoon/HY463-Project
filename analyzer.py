import collections
import tokenizer
import readxml
import os


def analyzeAllDocs(folder):
    """
    Reads all docs in a folder and for each word calculates its appearance in each tag of a document
    """
    unique_words = []
    docs = []

    # read all files in folder
    for root, dirs, files in os.walk(folder):
        for file in files:
            path = os.path.join(root, file)
            # skip files that are not nxml
            if path[-5:] != '.nxml':
                continue
            doc = readxml.readFileXML(path)
            docs.append(doc)
            return

    return docs


def getNumberOfUniqueWords(analyzed):
    """
    returns the number of keys (words) in the `analyzed` dictionary
    """
    return len(analyzed.keys())
