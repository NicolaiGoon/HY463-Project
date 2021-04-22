from src.Model.Vocabulary import Vocabulary
from src.Model.Posting import Posting
from src.Model.DocumentFileEntry import DocumentFileEntry
from src.Model.Document import Document

def search(query):
    # load vocabulary
    vocab = Vocabulary().entries
    # query is represented as a document
    query = Document(0,'Query',{'body' : query})
    docs = {}
    # find documents for every word
    for word in query.content:
        try:
            term = vocab[word]
        except:
            continue
        docs = getDocsOfTerm(docs,term)
    
    return docs

# def getPosts(pointer,vocab,query):
#     posts = []
#     n = next_key(vocab,query)
#     end_pointer = vocab[n].PostingPointer
#     while True:
#         if pointer == end_pointer - 1: 
#             break
#         post = Posting(pointer)
#         posts.append(post)
#         pointer += 1
#     return posts

def getPosts(pointer):
    posts = []
    while True:
        post = Posting(pointer)
        if post.stop: 
            break
        posts.append(post)
        pointer += 1
    return posts

def getDocsOfTerm(docs,term):
    posts = getPosts(term.PostingPointer)
    for post in posts:
        doc = DocumentFileEntry(post.DocumentPointer)
        docs[doc.id] = doc
    return docs

# see https://stackoverflow.com/questions/61058709/return-next-key-of-a-given-dictionary-key-python-3-6
def next_key(dict, key):
    keys = iter(dict)
    key in keys
    return next(keys, False)
