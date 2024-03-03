import datetime

from SQLBase import SqlBase


class SenateData(SqlBase):

    def __init__(self):
        SqlBase.__init__(self, "localhost", "root", "", "senate")

    # Get list of speakers
    def getspeakerlist(self):
        query = "select id, speakername from code_speakernames1 order by speakername"
        return self.select_all(query)


    #  Get ids of textlines for specific speaker
    def getspeakertextlineids(self, speakerid):

        query = "select id from transcriptlines where speakerid={0} order by id".format(speakerid)
        return self.select_all(query)


    def gettranscriptline(self, id):
        query = "select * from transcriptlines where id={0}".format(str(id))
        return self.select_all(query)


    # String utilities

    def preprocess_singlequotes(self, textin):
        return textin.replace(r"'", r"''")

    # Add data

    def addlogentry(self, logtext):

        logtext = logtext.replace("'", "''")
        query = "insert data_log (loggeddate, logtext) values ('{0}','{1}')".format(
            datetime.datetime.now().strftime("%Y-%m-%d %X"), logtext)
        return self.execute(query)

    def insertspeakermostcommonwords(self, speakerid, jsontext):

        jsontext = jsontext.replace("'", "")

        query = "insert into data_mostcommonwords (speakerid, data) values ({0}, JSON_OBJECT({1}))".format(speakerid, jsontext)
        return self.execute(query)


    def getspeakerid(self, speakername):

        query = "select id from code_speakernames1 where speakername='{0}'".format(speakername)
        return self.select_one(query)


    def insertspeakerunigram(self, speakerid, unigram):

        # Diagnostic
        print("\tProcessing n-gram level 1")

        for entry in unigram:

            dbtoken = entry[0]
            frequency = unigram[entry]

            query = "insert into data_ngrams (speakerid, token, frequency) values ({0}, '{1}', {2})".format(speakerid,
                                                                                                        dbtoken,
                                                                                                        frequency)
            self.execute(query)


    def insertspeakerngrams(self, speakerid, ngram, ngramlevel):

        # Diagnostic
        print("\tProcessing n-gram level {0}".format(str(ngramlevel)))

        # Break n-gram dict into a list
        for entry in ngram:

            dbtoken = ""
            for i in range(0,ngramlevel-1):
                dbtoken += entry[i] + " "
            dbtoken = dbtoken.strip()

            dbnextword = entry[ngramlevel-1]

        # for x in range(1, n-1):
        #     token += " " + ngram[x]
        #
        # nextword = ngram[n-1]

            query = "insert into data_ngrams (speakerid, token, nextword, " \
                    "frequency) values ({0}, '{1}', '{2}', {3})".format(speakerid, dbtoken, dbnextword, ngram[entry])

            self.execute(query)

