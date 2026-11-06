"""
MAIN APP
@author Nikos Gounakis
@description Information Retrival System
"""

from src.Model import readxml
from src.Model import analyzer
from src.Model import indexer
import time
import statistics
from src.Model.Document import Document
import sys
import pathlib
from src.Model import search
from src.Model import readIndex
from src.Model.Vocabulary import Vocabulary
import operator
from src.Model import Utilities as u
from src.Model.DocumentFileEntry import DocumentFileEntry

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


def startPartialIndexing(folder, docs_per_run=analyzer.DOCS_PER_RUN):
    print("**********************")
    # time
    start = time.time()
    tmp_time = time.time()
    # check memory usage when a document is read
    print("Starting Doc analysis ...")
    runs, total = analyzer.analyzeAllDocsPartial(folder, docs_per_run)
    print("Doc analysis finised\tTime: "+str(time.time()-start))
    print("Starting merging of "+str(len(runs))+" runs ...")
    tmp_time = time.time()
    indexer.merge(runs)
    print("Merging finished\tTime: "+str(time.time()-tmp_time))
    print("----------------------")
    print("Total docs: "+str(total)+"\nTotal Time: "+str(time.time()-start))
    print("**********************")


def startIndexing(folder):
    print("**********************")
    # measudoc_type
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
    print("Term analysis finished\tTime: "+str(time.time()-tmp_time))
    print("----------------------")
    # indexing
    tmp_time = time.time()
    print("Start Indexing ...")
    indexer.index(docs, terms)
    print("Indexing finished\tTime: "+str(time.time()-tmp_time))
    print("----------------------")
    print("Total docs: "+str(len(docs))+"\nTotal terms: " +
          str(len(terms))+"\nTotal Time: "+str(time.time()-start))
    print("**********************")


def evaluate(vocab, documents):
    print('********** START EVALUATION ***********')
    results_file = pathlib.Path().absolute().joinpath(
        'Results/results.txt')
    res_list = []
    topics = readxml.readTopic()
    with open(results_file, 'w', encoding='utf-8') as results:
        for q in topics:
            # CHOOSE DESCRIPTION OR SUMMARY

            #docs = search.search(vocab, q.description)[:1000]
            docs = search.search(vocab, q.summary)[:1000]

            print('Topic: '+q.number)
            rank = 1
            for doc in docs:
                results.write(str(q.number)+'\t0\t'+str(doc.id) +
                              '\t'+str(rank)+'\t'+str(doc.score)+'\t'+'ng_v1\n')
                rank += 1
    scoreResults(documents)


def scoreResults(documents):
    """computes bpref, AveP' and nDCG' of Results/results.txt and writes Results/eval_results.txt"""
    qrels = readxml.readQrels()
    answers = u.read_results('Results/results.txt')
    scores = {}
    with open('Results/eval_results.txt', 'w', encoding='utf-8') as eval_res:
        for topic in sorted(qrels, key=int):
            judgments = u.judged_in_collection(qrels[topic], documents)
            ranking = answers.get(topic, [])
            bpref = u.bpref(ranking, judgments)
            avep = u.avep(ranking, judgments)
            ndcg = u.NDCG(ranking, judgments)
            eval_res.write(topic+'\t'+str(bpref)+'\t' +
                           str(avep)+'\t'+str(ndcg)+'\n')
            print('Topic: '+topic+'\tbpref: %.4f\tAveP\': %.4f\tnDCG\': %.4f' % (bpref, avep, ndcg))
            # topics without relevant documents in the collection can not be evaluated
            if any(rel > 0 for rel in judgments.values()):
                scores[topic] = (bpref, avep, ndcg)
            else:
                print('\t(no relevant documents in the collection, excluded from the statistics)')
    if not scores:
        print('No topic has relevant documents in the indexed collection')
        return
    print('---------------------------------')
    print('Evaluated topics: %d' % len(scores))
    print('%-8s %8s %8s %8s %8s' % ('', 'mean', 'median', 'min', 'max'))
    columns = list(zip(*scores.values())) + [[sum(v) / 3 for v in scores.values()]]
    for name, values in zip(['bpref', "AveP'", "nDCG'", 'mean(3)'], columns):
        print('%-8s %8.4f %8.4f %8.4f %8.4f' % (
            name, statistics.mean(values), statistics.median(values), min(values), max(values)))


def selectFolder():
    """folder from the command line (python app.py -index <folder>), else the GUI picker"""
    if len(sys.argv) > 2:
        return sys.argv[2]
    from src.View import Menu
    return Menu.selectIndexingFolder()


arg = ''
if len(sys.argv) > 1:
    arg = sys.argv[1]

# folder = pathlib.Path().absolute().joinpath("Data\\MiniCollection")
# folder = 'D:\\MedicalCollection\\00'

# normal indexing , really fast , requires lots of ram
if arg == '-index':
    folder = selectFolder()
    if folder == '':
        print('No folder selected for indexing\nexiting ...')
        exit(-1)
    startIndexing(folder)
# partial indexing , slow , requires a lot less ram
elif arg == '-pindex':
    folder = selectFolder()
    if folder == '':
        print('No folder selected for indexing\nexiting ...')
        exit(-1)
    # optional: python app.py -pindex <folder> <documents per run>
    if len(sys.argv) > 3:
        startPartialIndexing(folder, int(sys.argv[3]))
    else:
        startPartialIndexing(folder)
elif arg == '-test-index':
    testIndexing()
# run evaluation
elif arg == '-eval':
    # load vocabulary
    vocab = Vocabulary().entries
    docs = readIndex.allDocumentIds()
    evaluate(vocab, docs)
else:

    # load vocabulary
    vocab = Vocabulary().entries
    try:
        while True:
            print('********** START EVALUATION ***********')
            query = str(input("Write a summary or a description:\n"))

            # measure time
            start = time.time()

            docs = search.search(vocab, query)[:10]
            end = time.time() - start

            # display results
            print('\n---------- Query Results ------------\n')
            for doc in docs:
                doc.display()
                print()
            print('Total docs: '+str(len(docs)))
            print('Query time: '+str(end))
            print('---------------------------------\n')
    except KeyboardInterrupt:
        print('Exiting ...')
        exit(0)
