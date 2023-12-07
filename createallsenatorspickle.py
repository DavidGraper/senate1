import pickle
import glob

from collections import Counter

def createallsenatorspickle():

    sumspeakerwordcounts = Counter()

    for filename in glob.glob("/home/dgraper/Documents/Senate_Speaker_Pickles/SENATOR_*.txt"):
        print("Processing '{0}".format(filename))

        file = open(filename, 'rb')
        speakerwordcounts = pickle.load(file)
        sumspeakerwordcounts = sumspeakerwordcounts + speakerwordcounts
        file.close()

    filename = "/home/dgraper/Documents/Senate Speaker Pickles/SENATORS_ALL.txt"
    filename = filename.replace(" ", "_")
    file = open(filename, 'wb')

    # dump information to that file
    pickle.dump(sumspeakerwordcounts, file)