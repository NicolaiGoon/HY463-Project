import collections
import tokenizer
import readFolders
import nltk

en_stemmer = nltk.stem.PorterStemmer()

def analyzeAllDocs(folder):
    """
    Reads all docs in a folder and for each word calculates its appearance in each tag of a document
    """
    unique_words = []
    results = {}
    readFolders.readAllFiles(folder,analyzeDoc,results)

    return results


def analyzeDoc(doc, doc_name, results):
    """
    Calculates how many times a word is displayed in a doc and in wich tag and append it to `results`
    """
    tag_tokenized = {}
    for tag in doc:
        tokens = []
        if isinstance(doc[tag], str):
            tokens = tokenizer.tokenize(doc[tag])
        elif isinstance(doc[tag], list):
            for s in doc[tag]:
                tokens += tokenizer.tokenize(s)
        else:
            raise Exception(
                'Doc object must have values of string or array of strings')
        tag_tokenized[tag] = tokens

    # calculate frequencies of words in each tag
    for tag in doc:
        counter = collections.Counter(tag_tokenized[tag])
        for word in counter:
            # english stemming
            word = en_stemmer.stem(word)
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


def getNumberOfUniqueWords(analyzed):
    """
    returns the number of keys in the `analyzed` dictionary
    """
    return len(analyzed.keys())
