class Term:
    """
    class representing a unique term inside a document collection
    """

    def __init__(self, id):
        self.id = id
        self.df = 0

    def setDf(self, df):
        self.df = df
