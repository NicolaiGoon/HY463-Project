import functools
import math
import pathlib
import psutil


@functools.lru_cache(maxsize=None)
def getCollectionSize():
    try:
        with open(pathlib.Path('CollectionIndex/size.txt'), encoding='utf-8') as f:
            return int(f.read().strip())
    except (OSError, ValueError):
        raise Exception('Please Perform Indexing')


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

        # try:
        #     sum += len(posts[doc.id][word].appearances['title']+posts[doc.id][word].appearances['abstract'])*VspaceWeight(q.tf(word), df) * \
        #         VspaceWeight(posts[doc.id][word].tf, df)
        # except KeyError:
        #     sum += VspaceWeight(q.tf(word), df) * \
        #         VspaceWeight(posts[doc.id][word].tf, df)

    score = sum / (norm(q, vocab)*doc.norm)
    doc.score = score


def availableMemory():
    stats = psutil.virtual_memory()
    return stats.percent


# ---------------------------------------------------------------------------
# Evaluation measures for incomplete judgments
#   bpref  : Buckley & Voorhees 2004 (Sakai 2007, Eq. 9)
#   AveP'  : Average Precision on the condensed list (Sakai 2007, Eq. 20)
#   nDCG'  : nDCG on the condensed list (Sakai 2007, Sec. 4.2)
# The condensed list is the ranking with all unjudged documents removed.
# `judgments` = {doc_id: relevance} (0 = non relevant, 1 = relevant, 2 = very relevant)
# with only the judged documents that exist in the indexed collection.
# ---------------------------------------------------------------------------


def judged_in_collection(topic_qrels, docs):
    """keeps the judgments of documents that are in the indexed collection (docs: set of int ids)"""
    return {doc: int(rel) for doc, rel in topic_qrels.items() if int(doc) in docs}


def read_results(file='Results/results.txt'):
    """returns {topic: [doc ids in rank order]} from results.txt"""
    res = {}
    with open(file, encoding='utf-8') as f:
        for line in f:
            tokens = line.split()
            if len(tokens) < 4:
                continue
            res.setdefault(tokens[0], []).append((int(tokens[3]), tokens[2]))
    return {t: [doc for _, doc in sorted(docs)] for t, docs in res.items()}


def condensed(ranking, judgments):
    """the ranking without unjudged documents"""
    return [doc for doc in ranking if doc in judgments]


def bpref(ranking, judgments):
    """
    1/R * sum over retrieved relevant r of (1 - min(R, n_r) / min(R, N))
    n_r: judged non relevant documents ranked above r, R / N: relevant / judged non relevant in total
    """
    R = sum(1 for rel in judgments.values() if rel > 0)
    N = len(judgments) - R
    if R == 0:
        return 0.0
    total = 0.0
    nonrel = 0
    for doc in condensed(ranking, judgments):
        if judgments[doc] > 0:
            # with no non relevant above (or none judged at all) there is no penalty
            if nonrel > 0:
                total += 1 - min(R, nonrel) / min(R, N)
            else:
                total += 1
        else:
            nonrel += 1
    return total / R


def avep(ranking, judgments):
    """AveP': precision at every relevant document of the condensed list, divided by R"""
    R = sum(1 for rel in judgments.values() if rel > 0)
    if R == 0:
        return 0.0
    total = 0.0
    found = 0
    for rank, doc in enumerate(condensed(ranking, judgments), 1):
        if judgments[doc] > 0:
            found += 1
            total += found / rank
    return total / R


def gain(rel):
    return 2 ** rel - 1


def DCG(relevances):
    return sum(gain(rel) / math.log2(rank + 1) for rank, rel in enumerate(relevances, 1))


def NDCG(ranking, judgments, cutoff=1000):
    """nDCG': DCG of the condensed list / DCG of the ideal ranking of all judged relevant documents"""
    ideal = DCG(sorted((rel for rel in judgments.values() if rel > 0), reverse=True)[:cutoff])
    if ideal == 0:
        return 0.0
    actual = DCG([judgments[doc] for doc in condensed(ranking, judgments)[:cutoff]])
    return actual / ideal
