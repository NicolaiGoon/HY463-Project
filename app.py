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
from src.View import Menu
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


def startPartialIndexing(folder):
    print("**********************")
    # time
    start = time.time()
    tmp_time = time.time()
    # check memory usage when a document is read
    print("Starting Doc analysis ...")
    queue, total = analyzer.analyzeAllDocsPartial(folder)
    print("Doc analysis finised\tTime: "+str(time.time()-start))
    print("Starting merging ...")
    indexer.merge(queue)
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


def evaluate(vocab, documents):
    print('********** START EVALUATION ***********')
    results_file = pathlib.Path().absolute().joinpath(
        'Results\\results.txt')
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
    eval_results_file = pathlib.Path().absolute().joinpath(
        'Results\\eval_results.txt')
    qrels = readxml.readQrels()
    total_scores = 0
    ideal_scores = 0
    max_score = 0
    min_score = 999999999999
    with open(eval_results_file, 'w', encoding='utf-8') as eval_res:
        for topic in qrels.keys():
            relevant = u.calc_relevant(qrels[topic], documents)
            answer = u.read_results(topic, qrels[topic])
            # check for relevant in collection
            valid = 0
            for doc in documents:
                if str(doc) in relevant:
                    valid = 1
                    break
            bpref = u.bpref(answer, relevant)
            avep = u.avep(answer, relevant)
            ndcg = u.NDCG(answer)
            score_sum = bpref + avep + ndcg
            total_scores += score_sum
            if(valid):
                if(score_sum/3 > max_score):
                    max_score = score_sum/3
                if(score_sum/3 < min_score):
                    min_score = score_sum/3
                ideal_scores += 3
            eval_res.write(topic+'\t'+str(bpref)+'\t' +
                           str(avep)+'\t'+str(ndcg)+'\n')
            print('Topic: '+topic+'\tbpref: ' +
                  str(bpref)+'\tAveP: '+str(avep)+'\tNDCG: '+str(ndcg))
    print('Average score: '+str(total_scores/ideal_scores) +
          '\tMax score: '+str(max_score)+'\tMin score: '+str(min_score))


arg = ''
if len(sys.argv) > 1:
    arg = sys.argv[1]

# folder = pathlib.Path().absolute().joinpath("Data\\MiniCollection")
# folder = 'D:\\MedicalCollection\\00'

# normal indexing , really fast , requires lots of ram
if arg == '-index':
    folder = Menu.selectIndexingFolder()
    if folder == '':
        print('No folder selected for indexing\nexiting ...')
        exit(-1)
    startIndexing(folder)
# partial indexing , slow , requires a lot less ram
elif arg == '-pindex':
    folder = Menu.selectIndexingFolder()
    if folder == '':
        print('No folder selected for indexing\nexiting ...')
        exit(-1)
    startPartialIndexing(folder)
elif arg == '-test-index':
    testIndexing()
# run evaluation
elif arg == '-eval':
    # load vocabulary
    vocab = Vocabulary().entries
    docs = []
    line = 1
    while True:
        try:
            doc = DocumentFileEntry(line)
            docs.append(doc.id)
            line += 1
        except:
            break
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
