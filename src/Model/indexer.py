import pathlib
from src.Model import Utilities
from alive_progress import alive_bar
from src.Model import readIndex
from src.Model.Vocabulary import Vocabulary
from src.Model.DocumentFileEntry import DocumentFileEntry
from src.Model.Posting import Posting
import os


def index(docs, terms, sorted_terms, names={}):
    # pdl  = previous document line in DocumentsFile
    exportCollectionSize(len(docs))
    if len(names) == 3:
        doc_map = exportDocuments(docs, terms, names['doc'])
        post_map = exportPosting(
            docs, terms, sorted_terms, doc_map, names['post'])
        exportVocabulary(terms, sorted_terms, post_map, names['vocab'])
    elif len(names) == 0:
        doc_map = exportDocuments(docs, terms)
        post_map = exportPosting(docs, terms, sorted_terms, doc_map)
        exportVocabulary(terms, sorted_terms, post_map)
    else:
        raise Exception("array names was: "+str(names))


def exportCollectionSize(size):
    '''
    exports collection size in `size.txt`
    '''
    rel_path = pathlib.Path().absolute()
    with open(rel_path.joinpath('CollectionIndex\\size.txt'), 'w', encoding='utf-8') as sizeFile:
        sizeFile.write(str(size))


def exportPosting(docs, terms, sorted_terms, doc_map, name='PostingFile', pdl=0):
    """
    exports `PostingFile.txt` in `CollectionIndex` Folder that contains the apperances of terms in documents
    """
    # post mapping
    post_map = {}
    counter = 1

    rel_path = pathlib.Path().absolute()
    with alive_bar(len(terms), title=name+':', bar='smooth') as bar:
        with open(rel_path.joinpath('CollectionIndex\\'+name+'.txt'), 'w', encoding='utf-8') as PostingFile:
            for term in sorted_terms:
                post_map[term] = counter
                for doc in terms[term].appearances:
                    counter += 1
                    s = str(docs[doc].id) + '\t' + str(docs[doc].tf(term)) + \
                        '\t' + str(terms[term].appearances[docs[doc].id]) + \
                        '\t' + str(doc_map[docs[doc].id]+pdl) + '\n'
                    PostingFile.write(s)
                bar()
                PostingFile.write('\n')
                counter += 1
    return post_map


def exportVocabulary(terms, sorted_terms, post_map, name='VocabularyFile'):
    """
    exports `VocabularyFile.txt` in `CollectionIndex` Folder that
    contains all different words in increasing lexicographic order and their document frequency
    """
    rel_path = pathlib.Path().absolute()
    with alive_bar(len(terms), title=name+':', bar='smooth') as bar:
        with open(rel_path.joinpath('CollectionIndex\\'+name+'.txt'), 'w', encoding='utf-8') as VocabularyFile:
            for term in sorted_terms:
                s = terms[term].id+'\t' + \
                    str(terms[term].df)+'\t'+str(post_map[term])+'\n'
                VocabularyFile.write(s)
                bar()


def exportDocuments(docs, terms, name='DocumentsFile'):
    # maps a document with the line in the file
    doc_map = {}
    counter = 1

    # sort by id
    sorted_docs = sorted(docs.keys())

    rel_path = pathlib.Path().absolute()
    with alive_bar(len(docs), title=name+':', bar='smooth') as bar:
        with open(rel_path.joinpath('CollectionIndex\\'+name+'.txt'), 'w', encoding='utf-8') as DocumentFile:
            for doc in sorted_docs:
                # mapping
                doc_map[docs[doc].id] = counter
                counter += 1

                d = Utilities.norm(docs[doc], terms, len(docs))
                DocumentFile.write(docs[doc].id+"\t" +
                                   docs[doc].path+"\t"+str(d)+"\n")
                bar()
    return doc_map


def merge(queue):
    last = False
    if len(queue) == 1:
        rel_path = pathlib.Path().absolute()
        # rename files
        os.rename(rel_path.joinpath('CollectionIndex\\DocumentsFile1.txt'),
                  rel_path.joinpath('CollectionIndex\\DocumentsFile.txt'))
        os.rename(rel_path.joinpath('CollectionIndex\\VocabularyFile1.txt'),
                  rel_path.joinpath('CollectionIndex\\VocabularyFile.txt'))
        os.rename(rel_path.joinpath('CollectionIndex\\PostingFile1.txt'),
                  rel_path.joinpath('CollectionIndex\\PostingFile.txt'))
    while len(queue) != 1:
        a = queue.pop(0)
        b = queue.pop(0)
        doc_map = mergeDocuments(a, b, last)
        mergeVocPost(a, b, doc_map, last)
        queue.append(a+'&'+b)
        if len(queue) == 2:
            last = True


def mergeVocPost(a, b, doc_map, last=False):
    vocab_a_line = 1
    vocab_b_line = 1
    posting_pointer = [1]
    if last:
        merged_voc_name = 'VocabularyFile.txt'
        merged_post_name = 'PostingFile.txt'
    else:
        merged_voc_name = 'VocabularyFile' + a + '&' + b + '.txt'
        merged_post_name = 'PostingFile' + a + '&' + b + '.txt'
    with open(pathlib.Path().absolute().joinpath('CollectionIndex\\'+merged_voc_name), 'w', encoding='utf-8') as VocabularyFile, open(pathlib.Path().absolute().joinpath('CollectionIndex\\'+merged_post_name), 'w', encoding='utf-8') as PostingFile:
        while True:
            try:
                term_a = Vocabulary.VocabularyEntry(readIndex.getIndexLineToknized(
                    'VocabularyFile'+a+'.txt', vocab_a_line))
            except:
                term_a = None
            try:
                term_b = Vocabulary.VocabularyEntry(readIndex.getIndexLineToknized(
                    'VocabularyFile'+b+'.txt', vocab_b_line))
            except:
                term_b = None
            # end
            if term_a == None and term_b == None:
                break
            # write term a to vocab and its appearnces in posting
            elif term_a != None and term_b == None:
                VocabularyFile.write(
                    str(term_a.id) + '\t' + str(term_a.df)+'\t'+str(posting_pointer[0])+'\n')
                vocab_a_line += 1
                mergePosts(term_a, a, PostingFile, posting_pointer, doc_map)
            # write term b in vocab and its apperances on posting
            elif term_b != None and term_a == None:
                VocabularyFile.write(
                    str(term_b.id) + '\t' + str(term_b.df)+'\t'+str(posting_pointer[0])+'\n')
                vocab_b_line += 1
                mergePosts(term_b, b, PostingFile, posting_pointer, doc_map)
            # both are not none
            else:
                # merge the term and write it to vocab and write its appearances to posting
                if term_a.id == term_b.id:
                    # write posts
                    VocabularyFile.write(
                        str(term_a.id) + '\t' + str(term_a.df+term_b.df)+'\t'+str(posting_pointer[0])+'\n')
                    mergePosts(term_a, a, PostingFile,
                               posting_pointer, doc_map, term_b, b)
                    vocab_a_line += 1
                    vocab_b_line += 1
                # determine wich term to write first
                else:
                    # write smaller alphabetically
                    if term_a.id < term_b.id:
                        VocabularyFile.write(
                            str(term_a.id) + '\t' + str(term_a.df)+'\t'+str(posting_pointer[0])+'\n')
                        mergePosts(term_a, a, PostingFile,
                                   posting_pointer, doc_map)
                        vocab_a_line += 1
                    else:
                        VocabularyFile.write(
                            str(term_b.id) + '\t' + str(term_b.df)+'\t'+str(posting_pointer[0])+'\n')
                        mergePosts(term_b, b, PostingFile,
                                   posting_pointer, doc_map)
                        vocab_b_line += 1

    # delete previous files
    os.remove(pathlib.Path().absolute().joinpath(
        'CollectionIndex\\VocabularyFile'+a+'.txt'))
    os.remove(pathlib.Path().absolute().joinpath(
        'CollectionIndex\\VocabularyFile'+b+'.txt'))
    os.remove(pathlib.Path().absolute().joinpath(
        'CollectionIndex\\PostingFile'+a+'.txt'))
    os.remove(pathlib.Path().absolute().joinpath(
        'CollectionIndex\\PostingFile'+b+'.txt'))


def mergePosts(term_a, a, PostingFile, posting_pointer, doc_map, term_b=None, b=None):
    pointer_a = term_a.PostingPointer
    if term_b:
        pointer_b = term_b.PostingPointer
    else:
        pointer_b = -1
    while True:
        post_a = Posting(pointer_a, 'PostingFile'+a+'.txt')
        if b:
            post_b = Posting(pointer_b, 'PostingFile'+b+'.txt')
        else:
            post_b = Posting(pointer_b, 'PostingFile'+a+'.txt')

        if post_a.stop and post_b.stop:
            break
        if not post_a.stop:
            PostingFile.write(str(post_a.doc_id) + '\t' + str(post_a.tf) +
                              '\t' + str(post_a.appearances) +
                              '\t' + str(doc_map[post_a.doc_id]) + '\n')
            posting_pointer[0] += 1
            pointer_a += 1

        if not post_b.stop:
            PostingFile.write(str(post_b.doc_id) + '\t' + str(post_b.tf) +
                              '\t' + str(post_b.appearances) +
                              '\t' + str(doc_map[post_b.doc_id]) + '\n')
            posting_pointer[0] += 1
            pointer_b += 1
    posting_pointer[0] += 1
    PostingFile.write('\n')


def mergeDocuments(a, b, last=False):
    doc_a_line = 1
    doc_b_line = 1
    counter = 1
    doc_map = {}
    if last:
        merged_name = 'DocumentsFile.txt'
    else:
        merged_name = 'DocumentsFile' + a + '&' + b + '.txt'
    with open(pathlib.Path().absolute().joinpath('CollectionIndex\\'+merged_name), 'w', encoding='utf-8') as DocumentFile:
        while True:
            try:
                doc_a = DocumentFileEntry(doc_a_line, 'DocumentsFile'+a+'.txt')
            except:
                doc_a = None
            try:
                doc_b = DocumentFileEntry(doc_b_line, 'DocumentsFile'+b+'.txt')
            except:
                doc_b = None
            # end
            if doc_a == None and doc_b == None:
                break
            elif doc_a != None and doc_b == None:
                DocumentFile.write(str(doc_a.id)+"\t" +
                                   doc_a.path+"\t"+str(doc_a.norm)+"\n")
                doc_map[doc_a.id] = counter
                counter += 1
                doc_a_line += 1
            elif doc_b != None and doc_a == None:
                DocumentFile.write(str(doc_b.id)+"\t" +
                                   doc_b.path+"\t"+str(doc_b.norm)+"\n")
                doc_map[doc_b.id] = counter
                counter += 1
                doc_b_line += 1
            elif doc_a.id < doc_b.id:
                DocumentFile.write(str(doc_a.id)+"\t" +
                                   doc_a.path+"\t"+str(doc_a.norm)+"\n")
                doc_map[doc_a.id] = counter
                counter += 1
                doc_a_line += 1
            else:
                DocumentFile.write(str(doc_b.id)+"\t" +
                                   doc_b.path+"\t"+str(doc_b.norm)+"\n")
                doc_map[doc_b.id] = counter
                counter += 1
                doc_b_line += 1
    # delete previous files
    os.remove(pathlib.Path().absolute().joinpath(
        'CollectionIndex\\DocumentsFile'+a+'.txt'))
    os.remove(pathlib.Path().absolute().joinpath(
        'CollectionIndex\\DocumentsFile'+b+'.txt'))
    return doc_map
