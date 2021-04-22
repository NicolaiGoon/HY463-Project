from src.Model import tokenizer
from src.Model import readxml
from src.Model.Term import Term
import collections
import os


def analyzeAllDocs(folder):
    """
    Reads all docs in a folder and for each word calculates its appearance in each tag of a document
    """
    docs = {}

    # read all files in folder
    for root, dirs, files in os.walk(folder):
        for file in files:
            path = os.path.join(root, file)
            # skip files that are not nxml
            if path[-5:] != '.nxml':
                continue
            doc = readxml.readFileXML(path)
            docs[doc.id] = doc

    return docs


def analyzeTerms(docs):
    terms = {}
    for doc in docs:
        # keep words that df is rised
        set = {}
        for word in docs[doc].content:
            # find if term exists
            if word in terms and word not in set:
                terms[word].setDf(terms[word].df + 1)
            else:
                new_term = Term(word)
                new_term.setDf(1)
                terms[word] = new_term
            terms[word].addAppearance(docs[doc], word)

    return terms

def getNumberOfUniqueWords(analyzed):
    """
    returns the number of keys (words) in the `analyzed` dictionary
    """
    return len(analyzed.keys())
