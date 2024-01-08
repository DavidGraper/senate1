import SenateDB
import nltk
from nltk import ngrams
from collections import defaultdict
from collections import Counter
import random
import datetime

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')


def generate_ngrams(startingwithspeakerid):

    sdb = SenateDB.SenateData()

    # For each speaker, go through each line of their text compiling unigrams, bigrams, and trigrams
    speakerlist = sdb.getspeakerlist()

    for speaker in speakerlist:

        if speaker['id'] < startingwithspeakerid:
            continue

        starttime = datetime.datetime.now()

        print("Processing {0} starting at {1}".format(speaker['speakername'], starttime))

        speakerunigrams = defaultdict(int)
        speakerbigrams = defaultdict(int)
        speakertrigrams = defaultdict(int)
        speakerquadgrams = defaultdict(int)
        speakerpentagrams = defaultdict(int)

        transcriptlineids = sdb.getspeakertextlineids(speaker["id"])

        transcriptlinecount = len(transcriptlineids)
        counter = 0
        percenttodisplay = 0

        for transcriptlineid in transcriptlineids:

            # Diagnostic
            transcriptlinestarttime = datetime.datetime.now()
            counter += 1
            percent = round((counter / transcriptlinecount) * 100)
            elapsedtime = transcriptlinestarttime - starttime

            # Display only integer percent increases
            if (percenttodisplay != percent):
                percenttodisplay = percent
                print("Speaker = '{0}', percent processed = {1}, "
                      "timeelapsed = {2}".format(speaker['speakername'], str(percenttodisplay),
                                                 elapsedtime))

            transcriptline = sdb.gettranscriptline(transcriptlineid['id'])

            for sentence in nltk.sent_tokenize(transcriptline[0]['text']):
                sentenceunigrams = getngramdictionaries(sentence, 1)
                sentencebigrams = getngramdictionaries(sentence, 2)
                sentencetrigrams = getngramdictionaries(sentence, 3)
                sentencequadgrams = getngramdictionaries(sentence, 4)
                sentencepentagrams = getngramdictionaries(sentence, 5)

                # Load accumulated n-gram listings
                speakerunigrams = dict(Counter(speakerunigrams) + Counter(sentenceunigrams))
                speakerbigrams = dict(Counter(speakerbigrams) + Counter(sentencebigrams))
                speakertrigrams = dict(Counter(speakertrigrams) + Counter(sentencetrigrams))
                speakerquadgrams = dict(Counter(speakerquadgrams) + Counter(sentencequadgrams))
                speakerpentagrams = dict(Counter(speakerpentagrams) + Counter(sentencepentagrams))

        # Once all transcript lines for this speaker have been processed, insert accumulator n-gram lists
        # into database
        sdb.insertspeakerunigram(speaker["id"], speakerunigrams)
        sdb.insertspeakerngrams(speaker["id"], speakerbigrams, 2)
        sdb.insertspeakerngrams(speaker["id"], speakertrigrams, 3)
        sdb.insertspeakerngrams(speaker["id"], speakerquadgrams, 4)
        sdb.insertspeakerngrams(speaker["id"], speakerpentagrams, 5)

            # for speakertrigram in speakertrigrams:
            #     sdb.insertspeakerngrams(speaker["id"], speakertrigrams, 3)
            #
            # for speakerbigram in speakerquadgrams:
            #     sdb.insertspeakerngrams(speaker["id"], speakerquadgrams, 4)
            #
            # for speakertrigram in speakerpentagrams:
            #     sdb.insertspeakerngrams(speaker["id"], speakerpentagrams, 5)


def getngramdictionaries(textline, N):

    # Tokenize the text into words
    words = nltk.word_tokenize(textline)

    # Preprocess the words (convert to lowercase, remove punctuation)
    words = [word.lower() for word in words if word.isalnum()]
    # print(words)

    # Diagnostic - Define the order of the N-gram model
    # N = 4

    # Create N-grams from the tokenized words
    ngrams_list = list(ngrams(words, N, pad_left=True, pad_right=True, left_pad_symbol='<s>', right_pad_symbol='</s>'))

    # Create a defaultdict to store N-grams and their frequency
    ngram_freq = defaultdict(int)
    for ngram in ngrams_list:
        ngram_freq[ngram] += 1

    # Remove all n-grams with multiple start/end padding entries.  This only happens with tri, quad, and pentagrams
    if N == 3:

        # Delete first dictionary entry
        ngram_freq.pop(next(iter(ngram_freq)))

        # Delete last dictionary entry
        ngram_freq.popitem()

    elif N == 4:
        ngram_freq.pop(next(iter(ngram_freq)))
        ngram_freq.pop(next(iter(ngram_freq)))
        ngram_freq.popitem()
        ngram_freq.popitem()
    elif N == 5:
        ngram_freq.pop(next(iter(ngram_freq)))
        ngram_freq.pop(next(iter(ngram_freq)))
        ngram_freq.pop(next(iter(ngram_freq)))
        ngram_freq.popitem()
        ngram_freq.popitem()
        ngram_freq.popitem()

    return ngram_freq


