import ast


class Posting:
    """
    represents a posting entry from PostingFile.txt:
    doc_id \t tf \t appearances \t byte offset of the document in DocumentsFile.txt
    """

    def __init__(self, tokens):
        self.doc_id = int(tokens[0])
        self.tf = float(tokens[1])
        self._appearances = tokens[2]
        self.DocumentPointer = int(tokens[3])

    @property
    def appearances(self):
        # parsed only when needed, scoring uses just tf
        if isinstance(self._appearances, str):
            self._appearances = ast.literal_eval(self._appearances)
        return self._appearances

    def display(self):
        print('---------- Posting Entry --------')
        print('Doc id: '+str(self.doc_id)+'\nTF: '+str(self.tf)+'\nAppearances: ' +
              str(self.appearances)+'\nDocument Pointer: '+str(self.DocumentPointer))
        print('---------------------------------')
