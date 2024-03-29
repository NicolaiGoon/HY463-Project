import xml.etree.ElementTree as ET
from src.Model.Document import Document
import pathlib
from src.Model.Topic import Topic
from src.Model import tokenizer


def readFileXML(file):
    """
    Opens an nxml file , reads XML content and returns and object representing that file

    Parameters
    ----------
        file: the file path to read
    """

    with open(file, 'r', encoding='utf-8') as xml_file:
        xml_tree = ET.parse(xml_file)
        root = xml_tree.getroot()

        # find id
        ids = root.findall('./front/article-meta/article-id')
        for id in ids:
            if id.attrib["pub-id-type"] == 'pmc':
                pmc_id = id.text
        #print("Pmcid: "+pmc_id)

        # find title
        title = root.find('.//article-title')
        if hasattr(title, "text"):
            if title.text:
                title = title.text
            else:
                title = ''
        else:
            title = ''
        # print("Title: "+title)

        # find abstract
        abstr = root.find('.//abstract')
        abstract = getDescendantsText(abstr)
        if abstract == None:
            abstract = ''
        # print("Abstract: "+abstract)

        # find body
        body = root.find('.//body')
        body = getDescendantsText(body)
        if body == None:
            body = ''
        # print('Body: '+body)

        # find journal
        journal = root.find('.//journal-title')
        journal = getDescendantsText(journal)
        if journal == None:
            journal = ''
        # print('journal: '+journal)

        # find publisher
        publisher = root.find('.//publisher-name')
        publisher = getDescendantsText(publisher)
        if publisher == None:
            publisher = ''
        # print('publisher: '+publisher)

        # find authors
        authors = root.find('.//contrib-group')
        authors_list = []
        # if no authors
        if authors != None:
            for author in authors:
                if author.tag == 'contrib' and author.attrib['contrib-type'] == 'author':
                    author_item = ''
                    for elem in author.iter():
                        if elem.tag == 'name':
                            # get name and surname
                            name = ''
                            surname = ''
                            if len(elem) > 0 and isinstance(elem[0].text, str):
                                name = elem[0].text.strip()
                            if len(elem) > 1 and isinstance(elem[1].text, str):
                                surname = elem[1].text.strip()
                            author_item += name + ' ' + surname
                    authors_list.append(author_item)
        # print("authors: "+str(authors_list))

        # find categories
        categories = root.find('.//article-categories')
        categories_list = []
        for category in categories:
            if category == None:
                categories_list.append('')
            else:
                categories_list.append(getDescendantsText(category).strip())
        # print('categories: '+str(categories_list))

        obj = {
            "title": tokenizer.tokenize(title),
            "abstract": tokenizer.tokenize(abstract),
            "body": tokenizer.tokenize(body),
            "journal": tokenizer.tokenize(journal),
            "publisher": tokenizer.tokenize(publisher),
            "authors": tokenizer.tokenize(authors_list),
            "categories": tokenizer.tokenize(categories_list)
        }

        doc = Document(pmc_id, file, obj)

        return doc


def readTopic():
    '''
    read all topics from topics.xml and returns them as an array of topic objects
    '''
    file = pathlib.Path().absolute().joinpath(
        'Resources\\Resources Corpus\\topics.xml')
    with open(file, 'r', encoding='utf-8') as topicfile:
        xml_tree = ET.parse(topicfile)
        root = xml_tree.getroot()

        topics = root.findall('.//topic')
        topic_array = []
        for topic in topics:
            description = topic.find('./description')
            summary = topic.find('./summary')
            topic_type = topic.attrib['type']
            topic_num = topic.attrib['number']
            t = Topic(topic_type, description.text, summary.text, topic_num)
            topic_array.append(t)
    return topic_array


def getDescendantsText(node):
    '''
    returns all node descendants text area

    Parameters:
    ----------
        node: node of xml tree
    '''
    res = ''
    try:
        for d in node.itertext():
            res += d.strip()
    except:
        res = ''
    return res


def readQrels():
    '''
    returns a dictionary with the qrels for the evaluation
    '''
    res = {}
    file = pathlib.Path().absolute().joinpath(
        'Resources\\Resources Corpus\\qrels.txt')
    with open(file, 'r', encoding='utf-8') as qrels:
        lines = qrels.readlines()
        for line in lines:
            q = line.split()
            topic_number = q[0]
            doc_id = q[2]
            relevance = q[3]
            if topic_number not in res:
                res[topic_number] = {}
            res[topic_number][doc_id] = relevance
    
    return res
