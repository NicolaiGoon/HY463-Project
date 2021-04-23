from src.Model import readIndex


class DocumentFileEntry:
    """
    class representing an entry to DocumentsFile.txt
    """

    def __init__(self, line_pointer):
        tokens = readIndex.getIndexLineToknized('Documents', line_pointer)
        if tokens == '':
            raise Exception('Invalid line pointer: '+line_pointer)
        self.id = int(tokens[0])
        self.path = tokens[1]
        self.norm = float(tokens[2])

    def display(self):
        print('----- DocumentFile Entry --------')
        print('ID: '+str(self.id)+'\nPath: ' +
              self.path+'\nNorm: '+str(self.norm))
        if(self.score):
            print('Score: '+str(self.score))
        print('---------------------------------')
