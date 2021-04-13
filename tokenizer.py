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


def analyzeDoc(doc):
    unique_words = []
    total_unique_words = 0
    tag_tokenized = {}
    results = {"total_unique_words": 0}
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
        unique_words += tokens
        tag_tokenized[tag] = tokens

    # make unique
    unique_words = list(set(unique_words))
    results["total_unique_words"] = len(unique_words)

    # calculate frequencies of words in each tag
    for tag in doc:
        counter = collections.Counter(tag_tokenized[tag])
        for word in counter:
            if word not in results.keys():
                results[word] = {}
            if tag in results[word].keys():
                results[word][tag] += counter[word]
            else:
                results[word][tag] = counter[word]

    # print(results)

    return results


doc = readxml.readFileXML(
    "C:\\Users\\xgoun\\Desktop\\PROGRAMS\\HY463\\project\\HY463-Project\\Data\\MiniCollection\\diagnosis\\Topic_1\\0\\1852545.nxml")

s = {
    'authors': ['Νίκος Γουνάκης', 'Αντώνης Γουνάκης'],
    'body': 'The???!@#$$%^&*()_ ? και ο γουνάκης η το Ελλάδα www.oof.com post-procedural course was uneventful; takotsubo cardiomyopathy was the final diagnosis and the patient was, thus, discharged with a therapy consisting of aspirin, diltiazem, ramipril and atorvastatin.Figure 1Twelve-lead electrocardiogram on admission.'
}

print(getTotal(analyzeDoc(doc)))

# tokens = doc["body"].split()
# unique_tokens = list(set(tokens))
# print(unique_tokens)
# print(len(tokens), len(unique_tokens))
