import datetime

from SQLBase import SqlBase


class SenateData(SqlBase):

    def __init__(self):
        SqlBase.__init__(self, "localhost", "root", "", "senate")

    # Get list of speakers
    def getspeakerlist(self):
        query = "select id, speakername from code_speakernames order by speakername"
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

        query = "select id from code_speakernames where speakername='{0}'".format(speakername)
        return self.select_one(query)


    def insertspeakerunigram(self, speakerid, unigram, frequency):

        query = "insert into data_ngrams (speakerid, token, frequency) values ({0}, '{1}', {2})".format(speakerid,
                                                                                                        unigram,
                                                                                                        frequency)
        return self.execute(query)


