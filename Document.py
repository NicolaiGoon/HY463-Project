import tokenizer
import collections
import nltk


class Document:
    """
    class representing a document in the collection
    """

    # tokenize content and calculate frequencies
    def __init__(self, id, path, content):
        self.id = id
        self.path = path
        self.content = content
        self.tokenizeTags()
        self.calculateFrequencies()

    def tokenizeTags(self):
        """
        tokenizes each tag of the doc
        """
        tag_tokenized = {}
        for tag in self.content:
            tokens = []
            if isinstance(self.content[tag], str):
                tokens = tokenizer.tokenize(self.content[tag])
            elif isinstance(self.content[tag], list):
                for s in self.content[tag]:
                    tokens += tokenizer.tokenize(s)
            else:
                raise Exception(
                    'Doc object must have values of string or array of strings')
            tag_tokenized[tag] = tokens
        self.content = tag_tokenized

    def calculateFrequencies(self):
        """
        Calculates how many times a word is displayed in a doc and in wich tag

        * tags must be tokenized
        """
        max = 0
        results = {}
        stemmer = nltk.stem.PorterStemmer()
        # calculate frequencies of words in each tag
        for tag in self.content:
            counter = collections.Counter(self.content[tag])
            for word in counter:
                # english stemming
                stemmed_word = stemmer.stem(word)
                # add new word
                if stemmed_word not in results.keys():
                    results[stemmed_word] = {}
                # a word appears for the first time in a tag
                if tag not in results[stemmed_word].keys():
                    results[stemmed_word][tag] = counter[word]
                else:
                    results[stemmed_word][tag] += counter[word]
                # find max_freq
                total = 0
                for inner_tag in results[stemmed_word]:
                    total += results[stemmed_word][inner_tag]
                if(total > max):
                    max = total

        self.content = results
        self.max_freq = max

    def termFreqnuency(self, term):
        try:
            total = 0
            for tag in self.content[term]:
                total += self.content[term][tag]
            return total
        except:
            print("The term: \""+term+"\" can not be found in this document")

    def tf(self, term):
        return self.termFreqnuency(term)/self.max_freq
