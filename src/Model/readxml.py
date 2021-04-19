import xml.etree.ElementTree as ET
from src.Model.Document import Document


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
        # print("Pmcid: "+pmc_id)

        # find title
        title = root.find('.//article-title')
        title = title.text
        # print("Title: "+title)

        # find abstract
        abstr = root.find('.//abstract')
        abstract = getDescendantsText(abstr)
        # print("Abstract: "+abstract)

        # find body
        body = root.find('.//body')
        body = getDescendantsText(body)
        # print('Body: '+body)

        # find journal
        journal = root.find('.//journal-title')
        journal = getDescendantsText(journal)
        # print('journal: '+journal)

        # find publisher
        publisher = root.find('.//publisher-name')
        publisher = getDescendantsText(publisher)
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
                            author_item += elem[0].text.strip() + \
                                ' ' + elem[1].text.strip()
                    authors_list.append(author_item)
        # print("authors: "+str(authors_list))

        # find categories
        categories = root.find('.//article-categories')
        categories_list = []
        for category in categories:
            categories_list.append(getDescendantsText(category).strip())
        # print('categories: '+str(categories_list))

        doc = Document(pmc_id, file, {
            "title": title,
            "abstract": abstract,
            "body": body,
            "journal": journal,
            "publisher": publisher,
            "authors": authors_list,
            "categories": categories_list
        })

        return doc


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
