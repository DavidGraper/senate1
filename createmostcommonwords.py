import SenateDB;


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
    filename = "/home/dgraper/Documents/Senate_Speaker_Pickles/SENATORS_ALL.txt"
    file = open(filename, 'rb')
    speakerwordcounts = pickle.load(file)
    mostcommon = speakerwordcounts.most_common(759)
    file.close()

    # Create a "Most Common Word" pickle file for each speaker

    for filename in glob.glob("/home/dgraper/Documents/Senate_Speaker_Pickles/*.txt"):

        result = re.search(r"SENATOR_(.*)\.txt", filename)
        senatorname = "SENATOR_{0}".format(result.group(1))

        print("Processing most common words for '{0}'".format(senatorname))

        file = open(filename, 'rb')
        senatorwordcounts = pickle.load(file)
        file.close()

        for mostcommonword in mostcommon:
            commonword = mostcommonword[0]
            del senatorwordcounts[commonword]

        # This is probably where I want to delete all names from code_speakernames

        senatormostcommonwords = senatorwordcounts.most_common(50)

        # open a file, where you want to store the data
        filename = "/home/dgraper/Documents/Senate_Speaker_Pickles/mostcommonwords_{0}.txt".format(senatorname)
        file = open(filename, 'wb')

        # dump information to that file
        pickle.dump(senatormostcommonwords, file)

        # close the file
        file.close()
