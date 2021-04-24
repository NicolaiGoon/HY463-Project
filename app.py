"""
MAIN APP
@author Nikos Gounakis
@description Information Retrival System
"""

from src.Model import readxml
from src.Model import analyzer
from src.Model import indexer
import time
from src.Model.Document import Document
import sys
import pathlib
from src.Model import search
from src.Model.Vocabulary import Vocabulary
import PySimpleGUI as sg

# doc = readxml.readFileXML(
#     "C:\\Users\\xgoun\\Desktop\\PROGRAMS\\HY463\\project\\HY463-Project\\Data\\MiniCollection\\diagnosis\\Topic_1\\0\\1852545.nxml")


def testIndexing():
    # measure time
    start = time.time()
    s = {
        'authors': ['Νίκος Γουνάκης', 'Αντώνης Γουνάκης'],
        'body': 'The???!@#$$%^&*()_ ? και ο γουνάκης η το Ελλάδα www.oof.com post-procedural παιζει course was uneventful; takotsubo cardiomyopathy was the final diagnosis and the patient was, thus, discharged with a therapy consisting of aspirin, diltiazem, ramipril and atorvastatin.Figure 1Twelve-lead electrocardiogram on admission.'
    }

    f = {
        'body': 'ο Νίκος Γουνάκης σπουδάζει στο τμήμα επιστήμης υπολογιστών , όμως και ο Αντώνης σπουδάζει εκεί. ο Νίκος παίζει κιθάρα',
        'authors': ['Νίκος Γουνάκης']
    }
    f = Document('f', 'path to f', f)
    s = Document('s', 'path to s', s)
    docs = [f, s]
    terms = analyzer.analyzeTerms(docs)
    sorted_terms = sorted(terms.keys())
    indexer.index(docs, terms, sorted_terms)
    print("Total docs: "+str(len(docs))+"\nTotal terms: " +
          str(len(terms))+"\nTotal Time: "+str(time.time()-start))


def startIndexing(folder):
    print("**********************")
    # measure time
    start = time.time()
    tmp_time = time.time()
    # analyze docs
    print("Starting Doc analysis ...")
    docs = analyzer.analyzeAllDocs(folder)
    print("Doc analysis finished\tTime: "+str(time.time()-tmp_time))
    print("----------------------")
    # analyze terms
    tmp_time = time.time()
    print("Starting Term analysis ...")
    terms = analyzer.analyzeTerms(docs)
    sorted_terms = sorted(terms.keys())
    print("Term analysis finished\tTime: "+str(time.time()-tmp_time))
    print("----------------------")
    # indexing
    tmp_time = time.time()
    print("Start Indexing ...")
    indexer.index(docs, terms, sorted_terms)
    print("Indexing finished\tTime: "+str(time.time()-tmp_time))
    print("----------------------")
    print("Total docs: "+str(len(docs))+"\nTotal terms: " +
          str(len(terms))+"\nTotal Time: "+str(time.time()-start))
    print("**********************")


if len(sys.argv) < 2:
    print("No arguments given")
    exit(-1)
arg = sys.argv[1]
if arg == '-index':
    folder = pathlib.Path().absolute().joinpath("Data\\MiniCollection")
    #folder = 'D:\\MedicalCollection\\00'
    startIndexing(folder)
elif arg == '-test-index':
    testIndexing()
elif arg == '-query':
    if len(sys.argv) < 3:
        query = str(input("Write a query:\n"))
    else:
        query = sys.argv[2]

    # load vocabulary
    vocab = Vocabulary().entries
    first_time = True
    while True:
        if not first_time:
            query = str(input("Write a query:\n"))
        # measure time
        start = time.time()

        docs = search.search(vocab, query)
        end = time.time() - start

        # display results
        print('\n---------- Query Results ------------\n')
        for doc in docs:
            doc.display()
            print()
        print('Total docs: '+str(len(docs)))
        print('Query time: '+str(end))
        print('---------------------------------\n')
        first_time = False

else:
    print("Invalid arguments")
    exit(-1)
