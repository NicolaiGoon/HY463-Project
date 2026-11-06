from src.Model import readIndex


class DocumentFileEntry:
    """
    class representing an entry to DocumentsFile.txt
    """

    def __init__(self, offset, file='Documents'):
        """offset: byte offset of the entry's line"""
        tokens = readIndex.getIndexLineToknized(file, offset)
        if tokens == '':
            raise Exception('Invalid document pointer: ' + str(offset))
        self.id = int(tokens[0])
        self.path = tokens[1]
        self.norm = float(tokens[2])

    def display(self):
        print('----- DocumentFile Entry --------')
        print('ID: '+str(self.id)+'\nPath: ' +
              self.path)
        if(hasattr(self, 'score')):
            print('Score: '+str(self.score))
        else:
            print('Norm: '+str(self.norm))
        print('---------------------------------')
