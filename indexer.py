import pathlib


def index(docs, terms):
    exportVocabulary(terms)
    exportDocuments(docs)


def exportVocabulary(terms):
    """
    exports `VocabularyFile.txt` in `CollectionIndex` Folder that
    contains all different words in increasing lexicographic order and their document frequency
    """
    rel_path = pathlib.Path().absolute()
    with open(rel_path.joinpath('CollectionIndex\\Vocabulary.txt'), 'w', encoding='utf-8') as VocabularyFile:
        for term in sorted(terms.keys()):
            VocabularyFile.write(terms[term].id+" "+str(terms[term].df)+"\n")


def exportDocuments(docs):

    def custom_sort(doc):
        return doc.id

    # sort by id
    docs.sort(key=custom_sort)
    rel_path = pathlib.Path().absolute()
    with open(rel_path.joinpath('CollectionIndex\\DocumentsFile.txt'), 'w', encoding='utf-8') as DocumentFile:
        for doc in docs:
            DocumentFile.write(doc.id+" "+doc.path+"\n")
    return
