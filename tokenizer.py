import readxml
import re
import string
import pathlib
import numpy as np


def stemmer():
    return


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

    for i in gr_stop_words:
        stop_words.append(i)
    for i in en_stop_words:
        stop_words.append(i)

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

    print(res)
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


doc = readxml.readFileXML(
    "C:\\Users\\xgoun\\Desktop\\PROGRAMS\\HY463\\project\\HY463-Project\\Data\\MiniCollection\\diagnosis\\Topic_1\\0\\1852545.nxml")

s = 'The???!@#$$%^&*()_ ? και ο η το ελλαδα www.oof.com post-procedural course was uneventful; takotsubo cardiomyopathy was the final diagnosis and the patient was, thus, discharged with a therapy consisting of aspirin, diltiazem, ramipril and atorvastatin.Figure 1Twelve-lead electrocardiogram on admission.'
tokenize(s)

# tokens = doc["body"].split()
# unique_tokens = list(set(tokens))
# print(unique_tokens)
# print(len(tokens), len(unique_tokens))
