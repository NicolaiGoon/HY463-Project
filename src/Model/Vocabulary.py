from src.Model.readIndex import INDEX_DIR
from alive_progress import alive_bar


class Vocabulary:
    """
    class representing the vocabulary read from VocabularyFile.txt
    """

    def __init__(self):
        self.entries = {}
        with open(INDEX_DIR / 'VocabularyFile.txt', encoding='utf-8') as f, \
                alive_bar(title='Loading Vocabulary:', unknown="classic") as bar:
            for line in f:
                line = line.rstrip('\n')
                if line == '':
                    continue
                entry = self.VocabularyEntry(line.split('\t'))
                self.entries[entry.id] = entry
                bar()

    class VocabularyEntry:
        """
        class representing a Vocabulary entry:
        term \t df \t byte offset of the term's postings in PostingFile.txt
        """

        def __init__(self, tokenized_line):
            self.id = tokenized_line[0]
            self.df = int(tokenized_line[1])
            self.PostingPointer = int(tokenized_line[2])

        def display(self):
            print('------ Vocabulary Entry ---------')
            print('ID: '+str(self.id)+'\nDF: '+str(self.df) +
                  '\nPostingPointer: '+str(self.PostingPointer))
            print('---------------------------------')
