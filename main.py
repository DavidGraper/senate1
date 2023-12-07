import json

import spacy
import os
import pickle
import glob
import re

import createspeakerpickles
import createmostcommonwords
import createspeakerpickles
import createallsenatorspickle

from collections import Counter

import SenateDB


def print_hi(name):
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    nlp = spacy.load("en_core_web_sm")

    # # Create a pickle of each senator's most commonly used words
    # createspeakerpickles.createspeakerpickles()
    #
    # # Create pickle of all senators' most commonly used words
    # createallsenatorspickle.createallsenatorspickle()
    #
    # # Create a list of senators' most commonly used words after
    # # removing the 760 most frequent words used by senators (this was a guesstimate
    # # done by looking at the most frequent words used by all senators and seeing a break point around 760 where
    # # the words were no longer just common conversational words)

    sdb = SenateDB.SenateData()

    for filename in glob.glob("/home/dgraper/Documents/Senate_Speaker_Pickles/mostcommonwords_SENATOR_*.txt"):
        result = re.search(r"SENATOR_(.*)\.txt", filename)

        # Hack for "Senator Craig Johnson"
        temptext = result.group(1).replace("_", " ")

        senatorname = "SENATOR {0}".format(temptext)

        senatorid = sdb.getspeakerid(senatorname)

        print("Processing most common words for '{0}'".format(senatorname))

        # Hack
        senatorname = senatorname.replace(" ","_")

        # Create JSON objects for each senator's most common words pickles and write to database
        filename = "/home/dgraper/Documents/Senate_Speaker_Pickles/mostcommonwords_{0}.txt".format(senatorname)

        file = open(filename, 'rb')
        speakerwordcounts = pickle.load(file)
        file.close()

        jsontext = json.dumps(speakerwordcounts)

        jsontext = jsontext.replace("[", "")
        jsontext = jsontext.replace("]", "")

        sdb = SenateDB.SenateData()

        # Insert pickle data for senator
        sdb.insertsenatormostcommonwords(senatorid["id"], jsontext)

    # exit()

    exit()

