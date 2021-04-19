import pathlib
import math


def index(docs, terms):
    exportVocabulary(terms)
    exportDocuments(docs, terms)


def exportVocabulary(terms):
    """
    exports `VocabularyFile.txt` in `CollectionIndex` Folder that
    contains all different words in increasing lexicographic order and their document frequency
    """
    rel_path = pathlib.Path().absolute()
    with open(rel_path.joinpath('CollectionIndex\\Vocabulary.txt'), 'w', encoding='utf-8') as VocabularyFile:
        for term in sorted(terms.keys()):
            VocabularyFile.write(terms[term].id+" "+str(terms[term].df)+"\n")


def exportDocuments(docs, terms):

    def custom_sort(doc):
        return doc.id

    # sort by id
    docs.sort(key=custom_sort)
    rel_path = pathlib.Path().absolute()
    with open(rel_path.joinpath('CollectionIndex\\DocumentsFile.txt'), 'w', encoding='utf-8') as DocumentFile:
        for doc in docs:
            d = norm(doc, terms, len(docs))
            DocumentFile.write(doc.id+" "+doc.path+" "+str(d)+"\n")
    return


def norm(doc, terms, n):
    """
    returns the eucledian distance from point 0 of the vector that represents the document
    """
    d = 0
    for term in doc.content:
        # calculate weight
        w = doc.tf(term) * math.log(n/terms[term].df)
        d += w*w
    d = math.sqrt(d)
    return d
