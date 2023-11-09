import spacy
import os
import pickle

from collections import Counter

import SenateDB


def print_hi(name):
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # print(spacy.load("en_core_web_sm"))

    nlp = spacy.load("en_core_web_sm")

    # nlp.vocab["Thank"].is_stop = True
    # nlp.vocab["President"].is_stop = True
    # nlp.vocab["bill"].is_stop = True
    # nlp.vocab["Mr."].is_stop = True
    # nlp.vocab["sponsor"].is_stop = True
    # nlp.vocab["yield"].is_stop = True
    # nlp.vocab["budget"].is_stop = True
    # nlp.vocab["$"].is_stop = True
    # nlp.vocab["bills"].is_stop = True
    # nlp.vocab["continue"].is_stop = True
    # nlp.vocab["Senator"].is_stop = True
    # nlp.vocab["public"].is_stop = True
    # nlp.vocab["questions"].is_stop = True
    # nlp.vocab["million"].is_stop = True
    # nlp.vocab["committee"].is_stop = True
    # nlp.vocab["year"].is_stop = True
    # nlp.vocab["New"].is_stop = True
    # nlp.vocab["York"].is_stop = True
    # nlp.vocab["floor"].is_stop = True
    # nlp.vocab["believe"].is_stop = True
    # nlp.vocab["billion"].is_stop = True
    # nlp.vocab["process"].is_stop = True
    # nlp.vocab["Senate"].is_stop = True
    # nlp.vocab["record"].is_stop = True
    # nlp.vocab["language"].is_stop = True
    # nlp.vocab["right"].is_stop = True
    # nlp.vocab["going"].is_stop = True
    # nlp.vocab["procedure"].is_stop = True
    # nlp.vocab["State"].is_stop = True
    # nlp.vocab["vote"].is_stop = True
    # nlp.vocab["information"].is_stop = True
    # nlp.vocab["tonight"].is_stop = True
    # nlp.vocab["amendment"].is_stop = True
    # nlp.vocab["appreciate"].is_stop = True
    # nlp.vocab["question"].is_stop = True
    # nlp.vocab["parliamentary"].is_stop = True
    # nlp.vocab["today"].is_stop = True
    # nlp.vocab["know"].is_stop = True
    # nlp.vocab["state"].is_stop = True
    # nlp.vocab["available"].is_stop = True
    # nlp.vocab["actually"].is_stop = True
    # nlp.vocab["colleagues"].is_stop = True
    # nlp.vocab["people"].is_stop = True
    # nlp.vocab["Governor"].is_stop = True
    # nlp.vocab["members"].is_stop = True
    # nlp.vocab["conference"].is_stop = True
    # nlp.vocab["appropriation"].is_stop = True
    # nlp.vocab["development"].is_stop = True
    # nlp.vocab["memo"].is_stop = True
    # nlp.vocab["fact"].is_stop = True
    # nlp.vocab["forward"].is_stop = True
    # nlp.vocab["Majority"].is_stop = True
    # nlp.vocab["debate"].is_stop = True
    # nlp.vocab["years"].is_stop = True
    # nlp.vocab["Minority"].is_stop = True
    # nlp.vocab["proposed"].is_stop = True
    # nlp.vocab["want"].is_stop = True
    # nlp.vocab["new"].is_stop = True
    # nlp.vocab["time"].is_stop = True
    # nlp.vocab["think"].is_stop = True
    # nlp.vocab["General"].is_stop = True

    # introduction_doc = nlp("This tutorial is about Natural Language Processing in spacy.  The"
    #                        " quick brown fox jumped over the lazy dog's back.")

    sdb = SenateDB.SenateData()

    # Get list of speakers
    speakers = sdb.getspeakerlist()


    # Iterate through speakers
    for speaker in speakers:

        print("Processing '{0}'".format(speaker['speaker']))

        speakerwordcounts = Counter()

        transcriptlineids = sdb.getspeakertextlineids(speaker['speaker'])

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
        filename = "/home/dgraper/Documents/Senate Speaker Pickles/{0}.txt".format(speaker['speaker'])
        filename = filename.replace(" ", "_")
        file = open(filename, 'wb')

        # dump information to that file
        pickle.dump(speakerwordcounts, file)

        # close the file
        file.close()

    exit()
    file = 'krueger.txt'
    file_text = open(file).read()

    introduction_doc = nlp(file_text)

    sentences = list(introduction_doc.sents)

    sum1 = Counter()

    for sentence in sentences:
        print(sentence)

        sentence_doc = nlp(sentence.text)

        words = [token.text for token in sentence_doc if not token.is_stop and not token.is_punct]

        temp1 = Counter(words)

        sum1 += temp1

        # for token in sentence_doc:
        #     print(
        #         f"{str(token.text_with_ws):22}"
        #         f"{str(token.is_alpha):15}"
        #         f"{str(token.is_punct):18}"
        #         f"{str(token.is_stop)}"
        #     )

    print(
        f"{'Text with Whitespace':22}"
        f"{'Is Alphanumeric?':15}"
        f"{'Is Punctuation?':18}"
        f"{'Is Stop Word?'}"
    )

    # print(
    #     # f"{"Text with Whitespace":22}"
    #     # f"{"Is Alphanumeric?":15}"
    #     # f"{"Is Punctuation?":18}"
    #     # f"{"Is Stop Word?"}"
    # )

    for token in introduction_doc:
        print(
            f"{str(token.text_with_ws):22}"
            f"{str(token.is_alpha):15}"
            f"{str(token.is_punct):18}"
            f"{str(token.is_stop)}"
        )

    # for token in introduction_doc:
    #     if not token.is_stop:
    #         if not token.is_punct:
    #             if token.is_alpha:
    #                 print(token.text_with_ws)

    words = [token.text for token in introduction_doc if not token.is_stop and not token.is_punct]

    temp1 = Counter(words)

    print(Counter(words).most_common(20))
