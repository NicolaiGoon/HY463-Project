import readxml
import re
import string
import pathlib
import collections


def readStopWords():
    """
    reads stopwords files and returns them as an array
    """
    rel_path = pathlib.Path().absolute()
    gr_path = pathlib.Path().absolute().joinpath(
        'Resources\\Resources Stoplists\\stopwordsGr.txt')
    en_path = pathlib.Path().absolute().joinpath(
        'Resources\\Resources Stoplists\\stopwordsEn.txt')

    stopwordsGr = open(gr_path, 'r', encoding='utf-8')
    stopwordsEn = open(en_path, 'r', encoding='utf-8')

    stop_words = []
    gr_stop_words = stopwordsGr.read().strip().split()
    en_stop_words = stopwordsEn.read().strip().split()
    # manual fix
    gr_stop_words[0] = 'και'
    en_stop_words[0] = 'a'

    stop_words = gr_stop_words + en_stop_words

    return stop_words


def removeStopWords(tokens):
    """
    removes greek or english stop words from the array
    """
    stopwords = readStopWords()
    res = []
    for word in tokens:
        if word not in stopwords:
            res.append(word)

    return res


def tokenize(str):
    """
    Tokenizes string s
    """
    res = str
    # get rid of punctuation  , make lower case , tokenize every word
    res = res.translate(str.maketrans(string.punctuation,
                                      ' '*len(string.punctuation))).lower().split()
    res = removeStopWords(res)

    return res


def getTotal(words):
    results = {}
    for word in words:
        if word == 'total_unique_words':
            continue
        total = 0
        for tag in words[word]:
            total += words[word][tag]
        results[word] = total
    return results

def getNumberOfUniqueWords(analyzed):
    """
    returns the number of keys in the `analyzed` dictionary
    """
    return len(analyzedObj.keys()) 

def analyzeAllDocs(docs):
    """
    Reads all docs in a folder and for each word calculates its appearance in each tag of a document
    """
    unique_words = []
    results = {}
    i = 0
    for doc in docs:
        i += 1
        analyzeDoc(doc, 'doc'+str(i), results)

    print()
    print(results)
    results["__UNIQUE_WORDS__"] = len(results.keys())


def analyzeDoc(doc, doc_name, results):
    """
    Calculates how many times a word is displayed in a doc and in wich tag and append it to `results`
    """
    tag_tokenized = {}
    for tag in doc:
        tokens = []
        if isinstance(doc[tag], str):
            tokens = tokenize(doc[tag])
        elif isinstance(doc[tag], list):
            for s in doc[tag]:
                tokens += tokenize(s)
        else:
            raise Exception(
                'Doc object must have values of string or array of strings')
        tag_tokenized[tag] = tokens

    # calculate frequencies of words in each tag
    for tag in doc:
        counter = collections.Counter(tag_tokenized[tag])
        for word in counter:
            # add new word
            if word not in results.keys():
                results[word] = {}
            # add a word appears in a doc for the first time
            if doc_name not in results[word].keys():
                results[word][doc_name] = {}
            # a word appears in a doc tag for the first time
            if tag not in results[word][doc_name].keys():
                results[word][doc_name][tag] = counter[word]
            else:
                results[word][doc_name][tag] += counter[word]


doc = readxml.readFileXML(
    "C:\\Users\\xgoun\\Desktop\\PROGRAMS\\HY463\\project\\HY463-Project\\Data\\MiniCollection\\diagnosis\\Topic_1\\0\\1852545.nxml")

s = {
    'authors': ['Νίκος Γουνάκης', 'Αντώνης Γουνάκης'],
    'body': 'The???!@#$$%^&*()_ ? και ο γουνάκης η το Ελλάδα www.oof.com post-procedural παιζει course was uneventful; takotsubo cardiomyopathy was the final diagnosis and the patient was, thus, discharged with a therapy consisting of aspirin, diltiazem, ramipril and atorvastatin.Figure 1Twelve-lead electrocardiogram on admission.'
}

f = {
    'body': 'ο Νίκος Γουνάκης σπουδάζει στο τμήμα επιστήμης υπολογιστών , όμως και ο Αντώνης σπουδάζει εκεί. ο Νίκος παίζει κιθάρα',
    'authors': ['Νίκος Γουνάκης']
}

analyzeAllDocs([s, f])
# print(results)

# tokens = doc["body"].split()
# unique_tokens = list(set(tokens))
# print(unique_tokens)
# print(len(tokens), len(unique_tokens))
