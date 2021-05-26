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


def sort_answer(answer):
    sorted_ids = sorted(answer, key=lambda x: (
        answer[x]['relevance']), reverse=True)
    result = {}
    for doc in sorted_ids:
        result[doc] = answer[doc]
    return result


def calc_relevant(quirels, docs):
    res = {}
    for doc in quirels:
        if int(quirels[doc]) > 0 and int(doc) in docs:
            res[doc] = {'relevance': int(quirels[doc])}
    return res


def read_results(topic_num, qrels):
    file = pathlib.Path().absolute().joinpath(
        'Results\\results.txt')
    res = {}
    line_no = 1
    flag = 0
    while True:
        line = linecache.getline(str(file), line_no)
        line = line.split()
        if line == []:
            # EOF
            break
        if(topic_num == line[0]):
            # found topic _number
            flag = 1
            doc_id = line[2]
            try:
                res[doc_id] = {'relevance': int(qrels[doc_id])}
            except KeyError:
                # not judged
                res[doc_id] = {'relevance': -1}
        elif (topic_num != line[0] and flag):
            break
        line_no += 1
    return res


def avep(answer, relevant):
    judged_in_answer = 0
    # counts the number of relevant documents
    total_rel = 0
    # counts the index in answer ignoring the non judged documents
    counter = 0
    # sum of all precisions
    sum = 0
    for doc in answer:
        if doc in relevant:
            counter += 1
            total_rel += 1
            sum += total_rel / counter
        elif answer[doc]['relevance'] == 0:
            counter += 1

    if total_rel != 0:
        return sum / total_rel
    else:
        return 0


def bpref(answer, relevant):
    R = len(relevant)
    N = len(answer) - R
    not_judged = 0
    # n irellevant ranked higher
    n = 0
    sum = 0
    for doc in answer:
        if doc in relevant:
            sum += 1 - (n/min(R, N))
        elif answer[doc]['relevance'] == 0:
            n += 1
    if R == 0 or sum < 0:
        return 0
    return sum / R


def DCG(answer):
    # scale: 2 =  very relevant , 1 = relevant , 0  = irrelevant , -1 not judged
    dcg = 0
    i = 1
    for d in answer:
        if answer[d]['relevance'] != -1:
            dcg += (2**(answer[d]['relevance'])-1)/(math.log2(i+1))
            i += 1
    return dcg


def NDCG(answer):
    dcg = DCG(answer)
    ideal_dcg = DCG(sort_answer(answer))
    if ideal_dcg != 0:
        return dcg/ideal_dcg
    else:
        return 0
