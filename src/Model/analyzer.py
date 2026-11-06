from src.Model import tokenizer
from src.Model import readxml
from src.Model.Term import Term
import collections
import os
from alive_progress import alive_bar
from src.Model import Utilities as utils
from src.Model import indexer
import pathlib
import random
from src.Model import indexer


def analyzeAllDocs(folder):
    """
    Reads all docs in a folder and for each word calculates its appearance in each tag of a document
    """
    docs = {}

    # read all files in folder
    with alive_bar(title='Reading Documents:', unknown="classic") as bar:
        for root, dirs, files in os.walk(folder):
            for file in files:
                path = os.path.join(root, file)
                # skip files that are not nxml
                if path[-5:] != '.nxml':
                    continue
                doc = readxml.readFileXML(path)
                docs[doc.id] = doc
                bar()
    return docs


# documents kept in memory before they are written as a sorted run
DOCS_PER_RUN = 1000
# write a run earlier if system memory usage goes above this percentage
MEMORY_LIMIT = 90


def analyzeAllDocsPartial(folder, docs_per_run=DOCS_PER_RUN):
    """
    Reads all docs in a folder in batches; every batch is written to disk as a sorted run.
    Returns the runs (to be merged with indexer.merge) and the number of documents read.
    """
    docs = {}
    runs = []
    counter = 0
    indexer.resetTmp()
    with alive_bar(title='Reading Documents:', unknown="classic") as bar:
        for root, dirs, files in os.walk(folder):
            for file in files:
                path = os.path.join(root, file)
                # skip files that are not nxml
                if path[-5:] != '.nxml':
                    continue
                doc = readxml.readFileXML(path)
                docs[doc.id] = doc
                counter += 1
                bar()
                if len(docs) >= docs_per_run or \
                        (len(docs) >= 10 and utils.availableMemory() > MEMORY_LIMIT):
                    runs.append(partialIndex(docs, len(runs) + 1))
                    docs = {}
        # index the last documents
        if len(docs) > 0:
            runs.append(partialIndex(docs, len(runs) + 1))
    return runs, counter


def partialIndex(docs, i):
    """writes the docs as sorted run number i"""
    return indexer.writeRun(docs, analyzeTerms(docs), i)


def analyzeTerms(docs):
    terms = {}
    for doc in docs:
        for word in docs[doc].content:
            # content keys are unique per doc, so every hit is a new document for the term
            if word in terms:
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
