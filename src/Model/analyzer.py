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


def analyzeAllDocsPartial(folder):
    """
    Reads all docs in a folder and writes partially
    """
    docs = {}
    queue = []
    # partial count
    i = 1
    counter = 0
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
                counter += 1
                bar()
                # if 80 is exceeded then write partial index
                if(utils.availableMemory() > 80):
                # if counter % random.randint(5, 10) == 0:
                    partialIndex(docs, i)
                    docs = {}
                    queue.append(str(i))
                    i += 1
        # index the last documents
        if len(docs) > 0:
            partialIndex(docs, i)
            queue.append(str(i))
    indexer.exportCollectionSize(counter)
    return queue, counter


def partialIndex(docs, i):
    terms = analyzeTerms(docs)
    sorted_terms = sorted(terms.keys())
    names = {'vocab': 'VocabularyFile' +
             str(i), 'post': 'PostingFile'+str(i), 'doc': 'DocumentsFile'+str(i)}

    indexer.index(docs, terms, sorted_terms, names)
    docs = {}
    print()


def analyzeTerms(docs):
    terms = {}
    with alive_bar(title='Reading Terms:', unknown='classic') as bar:
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
                bar()

    return terms


def getNumberOfUniqueWords(analyzed):
    """
    returns the number of keys (words) in the `analyzed` dictionary
    """
    return len(analyzed.keys())
