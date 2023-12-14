import pickle
import SenateDB
import glob
import re

def gettokensinspeakernamesfromdatabase():

    sdb = SenateDB.SenateData()

    speakerlist = sdb.getspeakerlist()

    returnlist = []

    for speaker in speakerlist:
        tokens = speaker['speakername'].split()
        for token in tokens:
            if not token in returnlist:
                returnlist.append(token)

    return returnlist


def createmostcommonwordpickles():

    # Get wordcounts for all speakers in database
    filename = "/home/dgraper/Documents/Senate_Speaker_Pickles/SPEAKERS_ALL.pkl"
    file = open(filename, 'rb')
    speakerwordcounts = pickle.load(file)

    # Get the 759 most common words used by all speakers
    mostcommonstopwords = speakerwordcounts.most_common(759)
    file.close()

    # Create a "Most Common Word" pickle file for each speaker after removing mostcommonstopwords
    for filename in glob.glob("/home/dgraper/Documents/Senate_Speaker_Pickles/*_wordcount.pkl"):

        result = re.search(r"\/home\/dgraper\/Documents\/Senate_Speaker_Pickles\/(.*)_wordcount\.pkl", filename)
        speakername = "{0}".format(result.group(1))

        print("Processing most common words for '{0}'".format(speakername))

        file = open(filename, 'rb')
        speakerwordcounts = pickle.load(file)
        file.close()

        # Remove most common words used by all speakers -- done to reveal words more unique to each speaker
        for commonword in mostcommonstopwords:
            commonword = commonword[0]
            del speakerwordcounts[commonword]

        # Select only the top 50 most common words
        speakermostcommonwords = speakerwordcounts.most_common(50)

        # Open a file and store this data as a pickle
        filename = "/home/dgraper/Documents/Senate_Speaker_Pickles/{0}_mostcommonwords.pkl".format(speakername)
        file = open(filename, 'wb')

        # dump information to that file
        pickle.dump(speakermostcommonwords, file)

        # close the file
        file.close()
