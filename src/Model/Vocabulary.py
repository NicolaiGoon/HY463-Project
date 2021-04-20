import linecache
import pathlib


class Vocabulary:
    """
    class representing the vocabulary read from VocabularyFile.txt
    """

    def __init__(self):
        self.entries = {}
        # path to VocabularyFile.txt
        file = pathlib.Path().absolute().joinpath(
            "CollectionIndex\\VocabularyFile.txt")
        file = "C:\\Users\\xgoun\\Desktop\\PROGRAMS\\HY463\\project\\HY463-Project\\CollectionIndex\\VocabularyFile.txt"

        line_number = 1
        while True:
            line = linecache.getline(file, line_number)
            line_number += 1
            if line == '':
                break
            # remove '\n'
            line = line.replace('\n', '')
            # tokenize
            line = line.split('\t')
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