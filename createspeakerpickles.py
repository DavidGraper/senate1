import pickle
import SenateDB
import spacy

from collections import Counter


def createspeakerpickles():

    nlp = spacy.load("en_core_web_sm")

    sdb = SenateDB.SenateData()

    # Get list of speakers
    speakers = sdb.getspeakerlist()

    # Iterate through speakers
    for speaker in speakers:

        print("Processing '{0}'".format(speaker['speakername']))

        speakerwordcounts = Counter()

        # Fetch speaker's transcript lines from database
        transcriptlineids = sdb.getspeakertextlineids(speaker['id'])

        for lineid in transcriptlineids:
            transcriptline = sdb.gettranscriptline(lineid['id'])

            # Break each transcript line into sentences
            transcriptlinetext = transcriptline[0]['text']
            speakertext = nlp(transcriptlinetext)

            sentences = speakertext.sents

            # Break each sentence into words
            for sentence in sentences:
                sentence_txt = nlp(sentence.text)
                words = [token.text for token in sentence_txt if not token.is_stop and not token.is_punct]

                # Get wordcount array for sentence
                sentence_words = Counter(words)

                # Add to wordcount array accumulator for speaker
                speakerwordcounts += sentence_words

        # Save wordcounts for this speaker to pickle file
        filename = "/home/dgraper/Documents/Senate Speaker Pickles/{0}_wordcount.pkl".format(speaker['speakername'])
        filename = filename.replace(" ", "_")
        file = open(filename, 'wb')
        pickle.dump(speakerwordcounts, file)
        file.close()
