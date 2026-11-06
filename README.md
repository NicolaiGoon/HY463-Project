# HY463-Project

ΗΥ463 – Συστήματα Ανάκτησης Πληροφοριών, Άνοιξη 2021 Project (University of Crete, CSD)

An information retrieval system for biomedical articles (PubMed Central NXML files), written in Python.
It builds an inverted index, answers natural-language queries with the vector space model,
and evaluates its effectiveness on the 30 medical topics of the TREC 2014 Clinical Decision Support track.

## Features

- **Indexing** of NXML articles (title, abstract, body, journal, publisher, authors, categories):
  tokenization, Greek and English stopword removal, English stemming (NLTK Porter stemmer),
  positions of every term per tag.
- **Two indexing modes**:
  - `-index`: all documents in memory, then written to disk.
  - `-pindex`: documents are read in batches; each batch is written as a sorted run, and the runs
    are combined with a streaming k-way merge. Memory depends on the batch size, not on the
    collection size, so collections larger than the available RAM can be indexed.
- **Inverted index on disk with byte offsets**: queries `seek()` directly to the postings of a term
  and to the document entries; only the vocabulary is loaded into memory.
- **Search** with the vector space model (tf·idf weights, cosine similarity).
- **Evaluation** (IRQualityEvaluator): runs all topics, writes `results.txt` in TREC format and
  computes **bpref**, **AveP′** and **nDCG′** (measures for incomplete relevance judgments),
  verified against `trec_eval`.

## Setup

Python 3.8 or newer (tested with 3.15).

```bash
python -m venv .venv
source .venv/bin/activate          # fish: source .venv/bin/activate.fish, Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Optional: the folder picker window (used when `-index`/`-pindex` get no folder) needs `PySimpleGUI`.

### Data

- `Data/MiniCollection`: small collection (54 articles) for testing, included.
- MedicalCollection (~1 GB, or the full 733,138 articles):
  see `Resources/Resources Corpus/MEDICAL-COLLECTION-HowToDownload.txt`.
- Topics and relevance judgments: `Resources/Resources Corpus/topics.xml`, `qrels.txt`.

## Usage

Run every command from the project folder (paths are relative to it).

```bash
# 1. build the index (CollectionIndex/)
python app.py -index Data/MiniCollection                 # in memory, fast, for small collections
python app.py -pindex /path/to/MedicalCollection 2000    # limited memory; optional documents per run (default 1000)

# 2. search interactively (Ctrl+C to exit)
python app.py

# 3. evaluate on the 30 topics
python app.py -eval
```

`-eval` evaluates the collection that was indexed last. It queries with each topic's **summary**;
to use the description instead, swap the two `search.search(...)` lines in `evaluate()` in `app.py`
(TREC rules allow one or the other, not both).

Lower the documents per run of `-pindex` if memory is tight. A run is also written early if system
memory usage goes above 90%.

## Index format

All files are UTF-8 text, tab separated, in `CollectionIndex/`. Every pointer is a **byte offset**.

| File | Line format |
|---|---|
| `VocabularyFile.txt` | `term  df  offset of the term's first posting in PostingFile.txt` (sorted by term) |
| `PostingFile.txt` | `doc_id  tf  appearances  offset of the document in DocumentsFile.txt`; an empty line follows the postings of each term |
| `DocumentsFile.txt` | `doc_id  path  norm` (sorted by id) |
| `size.txt` | number of documents |

`appearances` holds the positions of the term in each tag, e.g. `{'abstract': [89, 94], 'body': [624]}`.

## Retrieval model

- Weight: `w = tf · log(N / df)`, where `tf = freq / max_freq` of the document.
- Score: cosine similarity between the query and the document vectors.
  Document norms are computed at indexing time from the global df and N.
- The query goes through the same processing as the documents (tokenizer, stopwords, stemming).

## Evaluation

`python app.py -eval` writes:

- `Results/results.txt`: `TOPIC_NO  Q0  PMCID  RANK  SCORE  RUN_NAME`, top 1000 per topic.
- `Results/eval_results.txt`: `TOPIC_NO  BPREF  AVEP'  NDCG'` (TSV).

and prints mean, median, min and max of every measure.

| Measure | Definition |
|---|---|
| bpref | Buckley & Voorhees (2004): `1/R · Σ (1 − min(R, n) / min(R, N))` over the retrieved relevant documents; n = judged non relevant ranked above, N = all judged non relevant |
| AveP′ | Average Precision on the condensed list (unjudged documents removed), divided by R (Sakai 2007) |
| nDCG′ | nDCG on the condensed list; the ideal ranking uses all judged relevant documents; gain `2^rel − 1`, cutoff 1000 |

Only judgments of documents that exist in the indexed collection are used, so a subset of the
collection can be evaluated. Topics with no relevant document in it are reported but excluded
from the statistics.

Results on the MiniCollection (13 topics with relevant documents, summary queries):

| | mean | median | min | max |
|---|---|---|---|---|
| bpref | 0.750 | 0.875 | 0.000 | 1.000 |
| AveP′ | 0.834 | 0.888 | 0.478 | 1.000 |
| nDCG′ | 0.871 | 0.920 | 0.528 | 1.000 |

The MiniCollection is too small for meaningful numbers; use the MedicalCollection for real evaluation.

## Project structure

```
app.py                  command line entry point (indexing, search, evaluation)
src/Model/
  readxml.py            NXML articles, topics.xml and qrels.txt parsing
  tokenizer.py          tokenization and stopword removal
  Document.py           a document: stemming, positions per tag, tf
  Term.py               a term and the documents it appears in
  analyzer.py           reads a folder of documents (whole or in batches)
  indexer.py            sorted runs, streaming merge, index files, document norms
  readIndex.py          random access to the index files with byte offsets
  Vocabulary.py         VocabularyFile.txt loaded in memory
  Posting.py            a PostingFile.txt entry
  DocumentFileEntry.py  a DocumentsFile.txt entry
  search.py             vector space model search
  Utilities.py          weights, cosine similarity, evaluation measures
  Topic.py              a medical topic
src/View/Menu.py        folder picker window (PySimpleGUI)
Doc/report.md           project report (Greek)
Resources/              stopword lists, topics, qrels
```

## Known limitations

- Only English stemming; Greek words are not stemmed.
- The topic type (diagnosis / test / treatment) is not used for retrieval.
- Text of neighbouring XML elements is joined without a space, so some words are merged
  (e.g. the index contains the term `abscesscceaeprocess`).
- Only the vector space model; no BM25 or query expansion.
- `-test-index` is outdated and does not run.

## References

- C. Buckley, E. M. Voorhees, *Retrieval evaluation with incomplete information*, SIGIR 2004.
- T. Sakai, *Alternatives to bpref*, SIGIR 2007.
- M. S. Simpson, E. M. Voorhees, W. Hersh, *Overview of the TREC 2014 Clinical Decision Support Track*.
- [Atigeo at TREC 2014 Clinical Decision Support Task](https://trec.nist.gov/pubs/trec23/papers/pro-atigeo_clinical.pdf)
