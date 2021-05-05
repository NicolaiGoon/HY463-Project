from src.Model import readIndex
import ast


class Posting:
    """
    represents a posting entry from PostingFile.txt
    """

    def __init__(self, line_pointer, file='Posting'):
        tokens = readIndex.getIndexLineToknized(file, line_pointer)
        if tokens == '':
            self.stop = True
            return
        self.stop = False
        self.doc_id = int(tokens[0])
        self.tf = float(tokens[1])
        self.appearances = ast.literal_eval(tokens[2])
        self.DocumentPointer = int(tokens[3])

    def display(self):
        print('---------- Posting Entry --------')
        print('Doc id: '+str(self.doc_id)+'\nTF: '+str(self.tf)+'\nAppearances: ' +
              str(self.appearances)+'\nDocument Pointer: '+str(self.DocumentPointer))
        print('---------------------------------')
