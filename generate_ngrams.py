import SenateDB
import nltk
from nltk import ngrams
from collections import defaultdict
from collections import Counter
import random

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')


def generate_ngrams():

    sdb = SenateDB.SenateData()

    # For each speaker, go through each line of their text compiling unigrams, bigrams, and trigrams
    speakerlist = sdb.getspeakerlist()

    for speaker in speakerlist:

        print("Processing {0}".format(speaker['speakername']))

        speakerunigrams = defaultdict(int)
        speakerbigrams = defaultdict(int)
        speakertrigrams = defaultdict(int)
        speakerquadgrams = defaultdict(int)
        speakerpentagrams = defaultdict(int)

        transcriptlineids = sdb.getspeakertextlineids(speaker["id"])

        for transcriptlineid in transcriptlineids:
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

    # Define the order of the N-gram model
    # N = 1

    # Create N-grams from the tokenized words
    ngrams_list = list(ngrams(words, N))

    # Create a defaultdict to store N-grams and their frequency
    ngram_freq = defaultdict(int)
    for ngram in ngrams_list:
        ngram_freq[ngram] += 1

    return ngram_freq


