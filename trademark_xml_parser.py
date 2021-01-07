import xml.etree.ElementTree as et
from os import listdir

"""
trademark_xml_parser.py

This module operates on xml files from http://euipo.europa.eu/trademark/data 
xml namespace.
"""

def parse_dir(dirpath):
    """ 
    Parses all trademark xml files in a directory into a list of python 
    tuples 
    """

    trademarks = []
    for entry in listdir(dirpath):
        # If entry's name ends in .xml
        if entry[-4:] == ".xml": 
            # Parse it
            # print("parse_file("+dirpath+"/"+entry+")", flush=True)
            trademark = parse_file(dirpath + "/" + entry)

            if trademark is not None:
                trademarks.append(trademark)
        else:
            raise ParseError("Non .xml file found. Filename: {}".format(entry))

    return trademarks


def parse_file(filepath):
    """ 
    Parses a trademark xml file into a python tuple representing the trademark.
    Returns the tuple object
    Returns None if trademark's MarkFeature is not Word
    """
    # Namespace defined in the source data
    xmlns = "http://euipo.europa.eu/trademark/data"

    tree = et.parse(filepath)

    # If this trademark's MarkFeature is not Word
    # Find using XPath expression
    if next(tree.iterfind(".//{"+xmlns+"}MarkFeature")).text != "Word":
        # print("Non-Word MarkFeature trademark. Ignoring.", flush=True)
        return None

    # Else construct the tuple from it
    else:
        trademark = []
        # Add the interesting subelements
        # The order is not random
        try:
            trademark.append(
                next(tree.iterfind(".//{"+xmlns+"}ApplicationDate")).text)
        except StopIteration:
            # If subelement not found
            trademark.append("UNDEFINED") # max 10 chars in this db column
        trademark.append(
            next(tree.iterfind(".//{"+xmlns+"}ApplicationLanguageCode")).text)
        trademark.append(
            next(tree.iterfind(".//{"+xmlns+"}SecondLanguageCode")).text)
        trademark.append(
            next(tree.iterfind(".//{"+xmlns+"}MarkFeature")).text)
        trademark.append(
            next(tree.iterfind(".//{"+xmlns+"}MarkVerbalElementText")).text)
        trademark = tuple(trademark)

        # print("Returning trademark.", flush=True)
        return trademark

class ParseError(Exception):
    pass

if __name__ == "__main__":
    datafolder = "data/004/"
    filename = "018004927.xml"
    filepath = datafolder + filename

    trademark = parse_file(filepath)
    print("Single trademark:", flush=True)
    print(trademark, flush=True)
    
    trademarks = parse_dir(datafolder)
    print("Trademarks array:", flush=True)
    print(trademarks, flush=True)
