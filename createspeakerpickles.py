import pickle


def createspeakerpickles():

    sdb = SenateDB.SenateData()

    # Get list of speakers
    speakers = sdb.getspeakerlist()

    # Iterate through speakers
    for speaker in speakers:

        print("Processing '{0}'".format(speaker['speakername']))

        speakerwordcounts = Counter()

        transcriptlineids = sdb.getspeakertextlineids(speaker['id'])

        # Iterate through speaker lines getting sentences
        for lineid in transcriptlineids:
            transcriptline = sdb.gettranscriptline(lineid['id'])

            # Break into sentences
            transcriptlinetext = transcriptline[0]['text']
            speakertext = nlp(transcriptlinetext)

            sentences = speakertext.sents
            for sentence in sentences:
                # print(sentence)

                sentence_txt = nlp(sentence.text)
                words = [token.text for token in sentence_txt if not token.is_stop and not token.is_punct]
                sentence_words = Counter(words)

                speakerwordcounts += sentence_words
                # sentences = list()

        # open a file, where you ant to store the data
        filename = "/home/dgraper/Documents/Senate Speaker Pickles/{0}.txt".format(speaker['speakername'])
        filename = filename.replace(" ", "_")
        file = open(filename, 'wb')

        # dump information to that file
        pickle.dump(speakerwordcounts, file)

        # close the file
        file.close()
