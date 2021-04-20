import pathlib
from src.Model import readIndex


class Vocabulary:
    """
    class representing the vocabulary read from VocabularyFile.txt
    """

    def __init__(self):
        self.entries = {}
        # path to VocabularyFile.txt
        file = pathlib.Path().absolute().joinpath(
            "CollectionIndex\\VocabularyFile.txt")
        # linecache needs str filename
        file = str(file)

        line_number = 1
        while True:
            line = readIndex.getIndexLineToknized('Vocabulary', line_number)
            line_number += 1
            if line == '':
                break

            entry = self.VocabularyEntry(line)
            self.entries[entry.id] = entry

    class VocabularyEntry:
        """
        class representing a Vocabulary entry
        """

        def __init__(self, tokenized_line):
            self.id = tokenized_line[0]
            self.df = int(tokenized_line[1])
            self.PostingPointer = int(tokenized_line[2])
