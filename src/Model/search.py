from src.Model.Vocabulary import Vocabulary
from src.Model.Posting import Posting
from src.Model.DocumentFileEntry import DocumentFileEntry


def search(query):
    vocab = Vocabulary().entries
    pointer = vocab[query].PostingPointer
    
    
    #posts = getPosts(pointer,vocab,query)
    posts = getPostsV2(pointer)


    return getDocs(posts)

def getPosts(pointer,vocab,query):
    posts = []
    n = next_key(vocab,query)
    end_pointer = vocab[n].PostingPointer
    while True:
        if pointer == end_pointer - 1: 
            break
        post = Posting(pointer)
        posts.append(post)
        pointer += 1
    return posts

def getPostsV2(pointer):
    posts = []
    while True:
        post = Posting(pointer)
        if post.stop: 
            break
        posts.append(post)
        pointer += 1
    return posts

def getDocs(posts):
    docs = {}
    for post in posts:
        doc = DocumentFileEntry(post.DocumentPointer)
        docs[doc.id] = doc
    return docs

# see https://stackoverflow.com/questions/61058709/return-next-key-of-a-given-dictionary-key-python-3-6
def next_key(dict, key):
    keys = iter(dict)
    key in keys
    return next(keys, False)
