"""
Index construction with sorted runs and a streaming k-way merge.

The index is never held in memory as a whole:
  1. Documents are read in batches and every batch is written to disk as a sorted
     *run* (CollectionIndex/tmp/run_NNNNN.post and run_NNNNN.docs).
  2. The runs are merged with heapq.merge, which keeps only one line per run in memory.
     With more than MERGE_FAN_IN runs, groups of runs are merged first (several passes),
     so the number of files open at the same time stays bounded.
  3. Document norms need the global df and N, so they are computed while the final
     PostingFile is written and then written into DocumentsFile.txt.

Run formats (sorted):
  .post : term \t doc_id \t tf \t appearances      sorted by (term, doc_id)
  .docs : doc_id \t path                            sorted by doc_id

Final formats (utf-8; every pointer is a BYTE OFFSET to use with seek()):
  VocabularyFile.txt : term \t df \t offset of the term's first posting in PostingFile.txt
  PostingFile.txt    : doc_id \t tf \t appearances \t offset of the doc's line in DocumentsFile.txt
                       (an empty line follows the postings of every term)
  DocumentsFile.txt  : doc_id \t path \t norm
  size.txt           : number of documents

Memory during the final merge: one line per run, the postings of the current term,
and two numbers per document (offset and norm). Nothing grows with the number of terms.
"""
import heapq
import itertools
import math
import os
import shutil
from pathlib import Path

from alive_progress import alive_bar

INDEX_DIR = Path('CollectionIndex')
TMP_DIR = INDEX_DIR / 'tmp'
# maximum number of runs merged at once (= files open at the same time)
MERGE_FAN_IN = 64
# fixed width, so writing the real norm does not move any byte offset
NORM_FMT = '{:.12e}'


def _post(run):
    return run.with_name(run.name + '.post')


def _docs(run):
    return run.with_name(run.name + '.docs')


def _postKey(line):
    term, doc_id, _ = line.split('\t', 2)
    return term, int(doc_id)


def _docKey(line):
    return int(line.split('\t', 1)[0])


def resetTmp():
    """removes runs left over from an interrupted indexing"""
    shutil.rmtree(TMP_DIR, ignore_errors=True)
    TMP_DIR.mkdir(parents=True)


def writeRun(docs, terms, run_id):
    """
    writes the documents of one batch as a sorted run and returns the run path (without extension)

    docs:  {doc_id: Document}
    terms: {term: Term} as returned by analyzer.analyzeTerms(docs)
    """
    run = TMP_DIR / ('run_%05d' % run_id)
    with open(_post(run), 'w', encoding='utf-8', newline='\n') as post:
        for term in sorted(terms):
            appearances = terms[term].appearances
            for doc_id in sorted(appearances, key=int):
                post.write('%s\t%s\t%s\t%s\n' % (
                    term, doc_id, docs[doc_id].tf(term), appearances[doc_id]))
    with open(_docs(run), 'w', encoding='utf-8', newline='\n') as out:
        for doc_id in sorted(docs, key=int):
            out.write('%s\t%s\n' % (doc_id, docs[doc_id].path))
    return run


def index(docs, terms, sorted_terms=None):
    """indexes documents that fit in memory: a single run, then the same merge"""
    resetTmp()
    merge([writeRun(docs, terms, 1)])


def merge(runs):
    """merges the runs into the final index files and deletes the runs"""
    level = 0
    while len(runs) > MERGE_FAN_IN:
        merged = []
        for i in range(0, len(runs), MERGE_FAN_IN):
            group = runs[i:i + MERGE_FAN_IN]
            out = TMP_DIR / ('merge_%d_%05d' % (level, len(merged)))
            _mergeFiles([_post(r) for r in group], _post(out), _postKey)
            _mergeFiles([_docs(r) for r in group], _docs(out), _docKey)
            merged.append(out)
        runs = merged
        level += 1
    _writeFinal(runs)
    shutil.rmtree(TMP_DIR, ignore_errors=True)


def _mergeFiles(inputs, output, key):
    files = [open(p, encoding='utf-8', newline='\n') for p in inputs]
    try:
        with open(output, 'w', encoding='utf-8', newline='\n') as out:
            out.writelines(heapq.merge(*files, key=key))
    finally:
        for f in files:
            f.close()
    for p in inputs:
        os.remove(p)


def _writeFinal(runs):
    doc_files = [open(_docs(r), encoding='utf-8', newline='\n') for r in runs]
    post_files = [open(_post(r), encoding='utf-8', newline='\n') for r in runs]
    try:
        doc_offsets = _writeDocuments(heapq.merge(*doc_files, key=_docKey))
        n = len(doc_offsets)
        norms = _writePostingAndVocabulary(
            heapq.merge(*post_files, key=_postKey), doc_offsets, n)
    finally:
        for f in doc_files + post_files:
            f.close()
    _writeNorms(norms)
    exportCollectionSize(n)


def _writeDocuments(lines):
    """writes DocumentsFile.txt with a placeholder norm, returns {doc_id: byte offset}"""
    offsets = {}
    offset = 0
    placeholder = NORM_FMT.format(0.0)
    with open(INDEX_DIR / 'DocumentsFile.txt', 'wb') as out:
        for line in lines:
            doc_id, path = line.rstrip('\n').split('\t', 1)
            if int(doc_id) in offsets:
                print('Duplicate document id skipped: ' + doc_id)
                continue
            data = ('%s\t%s\t%s\n' % (doc_id, path, placeholder)).encode('utf-8')
            offsets[int(doc_id)] = offset
            out.write(data)
            offset += len(data)
    return offsets


def _writePostingAndVocabulary(lines, doc_offsets, n):
    """writes PostingFile.txt and VocabularyFile.txt, returns {doc_id: squared norm}"""
    norms = dict.fromkeys(doc_offsets, 0.0)
    offset = 0
    with open(INDEX_DIR / 'PostingFile.txt', 'wb') as post, \
            open(INDEX_DIR / 'VocabularyFile.txt', 'w', encoding='utf-8', newline='\n') as vocab, \
            alive_bar(title='Writing index:', unknown='classic') as bar:
        for term, group in itertools.groupby(lines, key=lambda l: l.split('\t', 1)[0]):
            start = offset
            tfs = []
            for line in group:
                _, doc_id, tf, appearances = line.rstrip('\n').split('\t', 3)
                d = int(doc_id)
                if d not in doc_offsets:
                    continue
                data = ('%s\t%s\t%s\t%d\n' % (
                    doc_id, tf, appearances, doc_offsets[d])).encode('utf-8')
                post.write(data)
                offset += len(data)
                tfs.append((d, float(tf)))
            post.write(b'\n')
            offset += 1
            # same weight as Utilities.VspaceWeight: tf * log(N / df)
            idf = math.log(n / len(tfs))
            for d, tf in tfs:
                w = tf * idf
                norms[d] += w * w
            vocab.write('%s\t%d\t%d\n' % (term, len(tfs), start))
            bar()
    return norms


def _writeNorms(norms):
    """replaces the placeholder norms; every line keeps its length, so offsets stay valid"""
    path = INDEX_DIR / 'DocumentsFile.txt'
    tmp = INDEX_DIR / 'DocumentsFile.tmp'
    with open(path, 'rb') as src, open(tmp, 'wb') as out:
        for line in src:
            head, old = line.rstrip(b'\n').rsplit(b'\t', 1)
            doc_id = int(head.split(b'\t', 1)[0])
            new = NORM_FMT.format(math.sqrt(norms[doc_id])).encode('ascii')
            assert len(new) == len(old), 'norm width changed'
            out.write(head + b'\t' + new + b'\n')
    os.replace(tmp, path)


def exportCollectionSize(size):
    '''
    exports collection size in `size.txt`
    '''
    with open(INDEX_DIR / 'size.txt', 'w', encoding='utf-8') as sizeFile:
        sizeFile.write(str(size))
