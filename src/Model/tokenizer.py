from src.Model import readxml
import re
import string
import pathlib


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
    res = []
    for word in tokens:
        if word not in stopwords:
            res.append(word)

    return res


def tokenize(s):
    """
    Tokenizes string s
    """
    res = s
    if isinstance(s, list):
        res = '-'.join(s)

    # get rid of punctuation  , make lower case , tokenize every word
    res = re.sub(r'\W+', ' ', res).lower().split()
    res = removeStopWords(res)

    return res


stopwords = readStopWords()
