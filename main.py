import spacy
import os
import pickle
import glob
import re

import createmostcommonwords
import createspeakerpickles
import createallspeakerspickle
import generate_ngrams
import savemostcommonwordstodb1

from collections import Counter

import SenateDB

# Start
if __name__ == '__main__':

    print("\n\nType in action you want to perform\n")
    print("(1) To create wordcount pickle files for each speaker in database "
          "(stored in /Documents/Senate_Speaker_Pickles/")
    print("\tunder the name of each speaker using file-naming format '<speakername>.pkl')")
    print("\t(WARNING:  This takes a very long time.)")

    print("(2) To create wordcount pickle file for all speakers in database "
          "(stored in /Documents/Speaker_Pickles/")
    print("\tunder filename 'speakers_all.pkl')")

    print("(3) Generate a list of most common words for speakers in database "
          "(stored in /Documents/Speaker_Pickles/")
    print("\tunder the name of each speaker using file-naming format '<speakername>_mostcommonwords.pkl')")

    print("(4) Create JSON structures of each speaker's most common words and write to database")

    print("(5) Generate unigrams, bigrams, and trigrams for speakers in database ")

    print("(0) To exit\n")

    action = input()

    if action == "1":

        nlp = spacy.load("en_core_web_sm")

        # The names of speakers are tokens we want to ignore when generating speakers most common words (e.g.,
        # an Acting President will rattle off the names of all the senators again and again and aren't what
        # they're actually talking about), so define all of the tokens in the "speakername" table as stop words
        speakernamestopwords = createmostcommonwords.gettokensinspeakernamesfromdatabase()

        for stopword in speakernamestopwords:
            nlp.Defaults.stop_words.add(stopword)

        # Create a pickle of each senator's most commonly used words
        createspeakerpickles.createspeakerpickles()

        exit()

    elif action == "2":

        nlp = spacy.load("en_core_web_sm")

        # Create pickle of all senators' most commonly used words
        createallspeakerspickle.createallspeakerspickle()

        exit()

    elif action == "3":

        nlp = spacy.load("en_core_web_sm")

        # Create most common words for speakers and save as pickles
        createmostcommonwords.createmostcommonwordpickles()

        exit()

    elif action == "4":

        nlp = spacy.load("en_core_web_sm")

        # Create JSON lists from speakers' most-common-words pickles and save to database
        savemostcommonwordstodb1.savemostcommonwordstodb()

        exit()

    elif action == "5":

        # HACK:  Restarting with "WEST POINT SUPERINTENDENT GILLAND" (12/25/23)
        # HACK:  Restarting with first entry (01/08/24)
        # HACK:  Restarting with Adam Denenberg (3)
        generate_ngrams.generate_ngrams(3)

        exit()
    else:
        exit()

    #



