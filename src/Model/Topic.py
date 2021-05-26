class Topic:
    '''
    Represetns a topic
    '''
    def __init__(self,type,description,summary,number):
        self.type = type
        self.description = description
        self.summary = summary
        self.number = number

    def display(self):
        print('------ Topic ------')
        print("NUmber: "+self.number)
        print("Type: "+self.type)
        print("Description: "+self.description)
        print("Summary: "+self.summary)
        print('--------------------')