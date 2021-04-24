class Topic:
    '''
    Represetns a topic
    '''
    def __init__(self,type,description,summary):
        self.type = type
        self.description = description
        self.summary = summary

    def display(self):
        print('------ Topic ------')
        print("Type: "+self.type)
        print("Description: "+self.description)
        print("Summary: "+self.summary)
        print('--------------------')