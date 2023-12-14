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

        transcriptlineids = sdb.getspeakertextlineids(speaker["id"])

        for transcriptlineid in transcriptlineids:
            transcriptline = sdb.gettranscriptline(transcriptlineid['id'])

    #         Get dictionary collection for this transcriptline
            transcriptlineunigrams = getunigramdictionaries(transcriptline[0]['text'])

            temp = dict(Counter(speakerunigrams) + Counter(transcriptlineunigrams))

            speakerunigrams = temp

    # Clear all n-gram entries for this user from database and write out new values
        for speakerunigram in speakerunigrams:
            sdb.insertspeakerunigram(speaker["id"], speakerunigram[0], speakerunigrams[speakerunigram])

def getunigramdictionaries(textline):

    # Tokenize the text into words
    words = nltk.word_tokenize(textline)

    # Preprocess the words (convert to lowercase, remove punctuation)
    words = [word.lower() for word in words if word.isalnum()]
    # print(words)

    # Define the order of the N-gram model
    N = 1

    # Create N-grams from the tokenized words
    ngrams_list = list(ngrams(words, N))

    # Create a defaultdict to store N-grams and their frequency
    ngram_freq = defaultdict(int)
    for ngram in ngrams_list:
        ngram_freq[ngram] += 1

    return ngram_freq
