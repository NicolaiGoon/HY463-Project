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

# doc = readxml.readFileXML(
#     "C:\\Users\\xgoun\\Desktop\\PROGRAMS\\HY463\\project\\HY463-Project\\Data\\MiniCollection\\diagnosis\\Topic_1\\0\\1852545.nxml")


def testIndexing():
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
    terms = analyzer.analyzeTerms([f, s])
    sorted_terms = sorted(terms.keys())
    indexer.index([f, s], terms, sorted_terms)


def startIndexing():
    # measure time
    start = time.time()

    # indexing
    docs = analyzer.analyzeAllDocs(
        "C:\\Users\\xgoun\\Desktop\\PROGRAMS\\HY463\\project\\HY463-Project\\Data\\MiniCollection")
    terms = analyzer.analyzeTerms(docs)
    sorted_terms = sorted(terms.keys())
    indexer.index(docs, terms, sorted_terms)

    print("Total docs: "+str(len(docs))+"\nTotal terms: " +
          str(len(terms))+"\nTotal Time: "+str(time.time()-start))


startIndexing()
# testIndexing()
