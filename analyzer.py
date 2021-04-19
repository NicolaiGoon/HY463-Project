import collections
import tokenizer
import readxml
import os
from Term import Term


def analyzeAllDocs(folder):
    """
    Reads all docs in a folder and for each word calculates its appearance in each tag of a document
    """
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

    return docs


def getUniqueTerms(docs):
    terms = {}
    for doc in docs:
        for word in doc.content:
            df = doc.termFreqnuency(word)
            # find if term exists
            if word in terms:
                terms[word].setDf(terms[word].df + df)
            else:
                new_term = Term(word)
                new_term.setDf(df)
                terms[word] = new_term

    return terms


def getNumberOfUniqueWords(analyzed):
    """
    returns the number of keys (words) in the `analyzed` dictionary
    """
    return len(analyzed.keys())
