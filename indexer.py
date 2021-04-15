import pathlib


def index(analyzed):
    exportVocabulary(analyzed)
    exportDocuments(analyzed)


def exportVocabulary(analyzed):
    """
    exports `VocabularyFile.txt` in `CollectionIndex` Folder that
    contains all different words in increasing lexicographic order and their document frequency
    """
    rel_path = pathlib.Path().absolute()
    with open(rel_path.joinpath('CollectionIndex\\Vocabulary.txt'), 'w', encoding='utf-8') as VocabularyFile:
        for word in sorted(analyzed.keys()):
            df = len(analyzed[word].keys())
            VocabularyFile.write(word+" "+str(df)+"\n")


def exportDocuments(analyzed):
    def getDocIds(analyzed):
        ids_n_path = []
        for word in analyzed:
            for doc in analyzed[word]:
                # split path and get last element
                id = doc.split('\\')[-1].replace('.nxml', '')
                row = {"id": id, "path": doc}
                if row not in ids_n_path:
                    ids_n_path.append(row)
        return ids_n_path
    ids_n_path = getDocIds(analyzed)

    rel_path = pathlib.Path().absolute()
    with open(rel_path.joinpath('CollectionIndex\\DocumentsFile.txt'), 'w', encoding='utf-8') as DocumentFile:
        for entry in ids_n_path:
            DocumentFile.write(entry["id"]+" "+entry["path"]+"\n")
    print("Total Documents: "+str(len(ids_n_path)))
    return
