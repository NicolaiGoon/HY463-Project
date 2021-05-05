import math
import linecache
import pathlib
import psutil


def getCollectionSize():
    n = linecache.getline(
        str(pathlib.Path().absolute().joinpath("CollectionIndex\\size.txt")), 1)
    if n == '':
        raise Exception('Please Perform Indexing')
    return int(n)


def norm(doc, terms, n=None):
    """
    returns the eucledian distance from point 0 of the vector that represents the document
    """
    if n == None:
        n = getCollectionSize()
    d = 0
    for term in doc.content:
        # if term not in vocab weight = zero
        if term not in terms:
            continue
        # calculate weight
        w = VspaceWeight(doc.tf(term), terms[term].df, n)
        d += w*w
    d = math.sqrt(d)
    return d


def VspaceWeight(tf, df, n=None):
    '''
    returns the weigth for the Vector Space Model
    '''
    if n == None:
        n = getCollectionSize()
    return tf * math.log(n/df)


def CosSim(doc, q, vocab, posts):
    sum = 0
    for word in q.content:
        # if word is not in document weigth is zero
        if word not in posts[doc.id]:
            continue
        df = vocab[word].df
        sum += VspaceWeight(q.tf(word), df) * \
            VspaceWeight(posts[doc.id][word].tf, df)
    score = sum / (norm(q, vocab)*doc.norm)
    doc.score = score


def availableMemory():
    stats = psutil.virtual_memory()
    return stats.percent
