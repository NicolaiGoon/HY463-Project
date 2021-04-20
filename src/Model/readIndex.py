import linecache
import pathlib


def getIndexLineToknized(type, line_number):
    """
    returns a tokenized line from a file in CollectionIndex
    """
    file = pathlib.Path().absolute().joinpath(
        "CollectionIndex\\" + type + "File.txt")
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
