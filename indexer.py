import pathlib
import math


def index(docs, terms, sorted_terms):
    doc_map = exportDocuments(docs, terms)
    post_map = exportPosting(docs, terms, sorted_terms, doc_map)
    exportVocabulary(terms, sorted_terms, post_map)


def exportPosting(docs, terms, sorted_terms, doc_map):
    """
    exports `PostingFile.txt` in `CollectionIndex` Folder that contains the apperances of terms in documents
    """
    # post mapping
    post_map = {}
    counter = 1

    rel_path = pathlib.Path().absolute()
    with open(rel_path.joinpath('CollectionIndex\\PostingFile.txt'), 'w', encoding='utf-8') as PostingFile:
        for term in sorted_terms:
            post_map[term] = counter
            for doc in docs:
                if terms[term].id in doc.content:
                    counter += 1
                    s = str(doc.id) + '\t' + str(doc.tf(term)) + \
                        '\t' + str(doc_map[doc.id]) + '\n'
                    PostingFile.write(s)
    return post_map


def exportVocabulary(terms, sorted_terms, post_map):
    """
    exports `VocabularyFile.txt` in `CollectionIndex` Folder that
    contains all different words in increasing lexicographic order and their document frequency
    """
    rel_path = pathlib.Path().absolute()
    with open(rel_path.joinpath('CollectionIndex\\Vocabulary.txt'), 'w', encoding='utf-8') as VocabularyFile:
        for term in sorted_terms:
            s = terms[term].id+'\t' + \
                str(terms[term].df)+'\t'+str(post_map[term])+'\n'
            VocabularyFile.write(s)


def exportDocuments(docs, terms):

    def custom_sort(doc):
        return doc.id

    # maps a document with the line in the file
    doc_map = {}
    counter = 1

    # sort by id
    docs.sort(key=custom_sort)
    rel_path = pathlib.Path().absolute()
    with open(rel_path.joinpath('CollectionIndex\\DocumentsFile.txt'), 'w', encoding='utf-8') as DocumentFile:
        for doc in docs:
            # mapping
            doc_map[doc.id] = counter
            counter += 1

            d = norm(doc, terms, len(docs))
            DocumentFile.write(doc.id+"\t"+doc.path+"\t"+str(d)+"\n")
    return doc_map


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
