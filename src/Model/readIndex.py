"""
Random access to the index files with byte offsets (seek + readline).
Only the requested lines are read; the files are never loaded into memory.
"""
from pathlib import Path

INDEX_DIR = Path('CollectionIndex')
_handles = {}


def _fileName(type):
    if type[-4:] == '.txt':
        return type
    if type in ('Vocabulary', 'Posting', 'Documents'):
        return type + 'File.txt'
    raise Exception('Invalid Prameter type: ' + type)


def _open(type):
    name = _fileName(type)
    f = _handles.get(name)
    if f is None or f.closed:
        f = open(INDEX_DIR / name, 'rb')
        _handles[name] = f
    return f


def readLines(type, offset, count):
    """returns `count` tokenized lines starting at byte `offset`"""
    f = _open(type)
    f.seek(offset)
    return [f.readline().decode('utf-8').rstrip('\n').split('\t') for _ in range(count)]


def getIndexLineToknized(type, offset):
    """
    returns the tokenized line that starts at byte `offset` of a file in CollectionIndex,
    or '' if there is no line there
    """
    if offset < 0:
        return ''
    f = _open(type)
    f.seek(offset)
    line = f.readline().decode('utf-8').rstrip('\n')
    if line == '':
        return ''
    return line.split('\t')


def allDocumentIds():
    """returns the ids of all documents in DocumentsFile.txt (read sequentially)"""
    with open(INDEX_DIR / 'DocumentsFile.txt', encoding='utf-8') as f:
        return {int(line.split('\t', 1)[0]) for line in f if line.strip()}
