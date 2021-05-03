import linecache
import pathlib


def getIndexLineToknized(type, line_number):
    """
    returns a tokenized line from a file in CollectionIndex
    """
    if type[-4:] == '.txt':
        file = pathlib.Path().absolute().joinpath(
            "CollectionIndex\\" + type)
    elif type == 'Vocabulary' or type == 'Posting' or type == 'Documents':
        file = pathlib.Path().absolute().joinpath(
            "CollectionIndex\\" + type + "File.txt")
    else:
        raise Exception('Invalid Prameter type: '+type)
    # convert to str
    file = str(file)
    # get line from file
    line = linecache.getline(file, line_number)
    # replace \n
    line = line.replace('\n', '')
    if line == '':
        return line
    #  tokenize
    line = line.split('\t')
    return line
