from src.Model.Vocabulary import Vocabulary
from src.Model.Posting import Posting
from src.Model.DocumentFileEntry import DocumentFileEntry
from src.Model.Document import Document
from src.Model import Utilities
import operator


def search(query):
    '''
    returns the docs that match the query words
    '''
    # load vocabulary
    vocab = Vocabulary().entries

    # query is represented as a document
    query = Document(0, 'Query', {'body': query})
    
    # for every term , contains the posts
    posts = {}

    # holds the docs returned
    results = {}

    # find documents for every word in query
    for word in query.content:
        try:
            term = vocab[word]
        except:
            continue
        posts = getPosts(term, posts)
    
    for doc_id in posts:
        # take the doc pointer from the first term post
        doc_pointer = posts[doc_id][next(iter(posts[doc_id]))].DocumentPointer
        doc = DocumentFileEntry(doc_pointer)
        # add score to doc as attribute
        Utilities.CosSim(doc, query, vocab, posts)
        results[doc_id] = doc

    return sorted(results.values(), key=operator.attrgetter('score'))


def getScore(doc, query, vocab, posts):
    '''
    add scores to the document
    '''
    Utilities.CosSim(doc, query, vocab, posts)
    return doc


def getPosts(term, posts={}):
    pointer = term.PostingPointer
    while True:
        post = Posting(pointer)
        if post.stop:
            break
        if post.doc_id not in posts:
            posts[post.doc_id] = {}
        posts[post.doc_id][term.id] = post
        pointer += 1
    return posts
