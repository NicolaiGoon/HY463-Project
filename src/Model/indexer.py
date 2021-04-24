import pathlib
from src.Model import Utilities
from alive_progress import alive_bar


def index(docs, terms, sorted_terms):
    exportCollectionSize(len(docs))
    doc_map = exportDocuments(docs, terms)
    post_map = exportPosting(docs, terms, sorted_terms, doc_map)
    exportVocabulary(terms, sorted_terms, post_map)


def exportCollectionSize(size):
    '''
    exports collection size in `size.txt`
    '''
    rel_path = pathlib.Path().absolute()
    with open(rel_path.joinpath('CollectionIndex\\size.txt'), 'w', encoding='utf-8') as sizeFile:
        sizeFile.write(str(size))


def exportPosting(docs, terms, sorted_terms, doc_map):
    """
    exports `PostingFile.txt` in `CollectionIndex` Folder that contains the apperances of terms in documents
    """
    # post mapping
    post_map = {}
    counter = 1

    rel_path = pathlib.Path().absolute()
    with alive_bar(len(terms), title='PostingFile:', bar='smooth') as bar:
        with open(rel_path.joinpath('CollectionIndex\\PostingFile.txt'), 'w', encoding='utf-8') as PostingFile:
            for term in sorted_terms:
                post_map[term] = counter
                for doc in terms[term].appearances:
                    counter += 1
                    s = str(docs[doc].id) + '\t' + str(docs[doc].tf(term)) + \
                        '\t' + str(terms[term].appearances[docs[doc].id]) + \
                        '\t' + str(doc_map[docs[doc].id]) + '\n'
                    PostingFile.write(s)
                bar()
                PostingFile.write('\n')
                counter += 1
    return post_map


def exportVocabulary(terms, sorted_terms, post_map):
    """
    exports `VocabularyFile.txt` in `CollectionIndex` Folder that
    contains all different words in increasing lexicographic order and their document frequency
    """
    rel_path = pathlib.Path().absolute()
    with alive_bar(len(terms), title='VocabularyFile:', bar='smooth') as bar:
        with open(rel_path.joinpath('CollectionIndex\\VocabularyFile.txt'), 'w', encoding='utf-8') as VocabularyFile:
            for term in sorted_terms:
                s = terms[term].id+'\t' + \
                    str(terms[term].df)+'\t'+str(post_map[term])+'\n'
                VocabularyFile.write(s)
                bar()


def exportDocuments(docs, terms):
    # maps a document with the line in the file
    doc_map = {}
    counter = 1

    # sort by id
    sorted_docs = sorted(docs.keys())

    rel_path = pathlib.Path().absolute()
    with alive_bar(len(docs), title='DocumentFile:', bar='smooth') as bar:
        with open(rel_path.joinpath('CollectionIndex\\DocumentsFile.txt'), 'w', encoding='utf-8') as DocumentFile:
            for doc in sorted_docs:
                # mapping
                doc_map[docs[doc].id] = counter
                counter += 1

                d = Utilities.norm(docs[doc], terms, len(docs))
                DocumentFile.write(docs[doc].id+"\t" +
                                   docs[doc].path+"\t"+str(d)+"\n")
                bar()
    return doc_map
