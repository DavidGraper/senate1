import pickle
import glob

from collections import Counter

def createallspeakerspickle():

    sumspeakerwordcounts = Counter()

    for filename in glob.glob("/home/dgraper/Documents/Senate_Speaker_Pickles/*.pkl"):
        print("Processing '{0}".format(filename))

        file = open(filename, 'rb')
        speakerwordcounts = pickle.load(file)
        sumspeakerwordcounts = sumspeakerwordcounts + speakerwordcounts
        file.close()

    filename = "/home/dgraper/Documents/Senate Speaker Pickles/SPEAKERS_ALL.pkl"
    filename = filename.replace(" ", "_")
    file = open(filename, 'wb')

    # dump information to that file
    pickle.dump(sumspeakerwordcounts, file)
