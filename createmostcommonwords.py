def createmostcommonwordpickles():

    filename = "/home/dgraper/Documents/Senate_Speaker_Pickles/SENATORS_ALL.txt"

    file = open(filename, 'rb')
    speakerwordcounts = pickle.load(file)
    mostcommon = speakerwordcounts.most_common(759)
    file.close()

    # create most common word pickles for each senator

    for filename in glob.glob("/home/dgraper/Documents/Senate_Speaker_Pickles/SENATOR_*.txt"):

        result = re.search(r"SENATOR_(.*)\.txt", filename)
        senatorname = "SENATOR_{0}".format(result.group(1))

        print("Processing most common words for '{0}'".format(senatorname))

        file = open(filename, 'rb')
        senatorwordcounts = pickle.load(file)
        file.close()

        for mostcommonword in mostcommon:
            commonword = mostcommonword[0]
            del senatorwordcounts[commonword]

        senatormostcommonwords = senatorwordcounts.most_common(50)

        # open a file, where you want to store the data
        filename = "/home/dgraper/Documents/Senate_Speaker_Pickles/mostcommonwords_{0}.txt".format(senatorname)
        file = open(filename, 'wb')

        # dump information to that file
        pickle.dump(senatormostcommonwords, file)

        # close the file
        file.close()
