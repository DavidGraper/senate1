import datetime

from SQLBase import SqlBase


class SenateData(SqlBase):

    def __init__(self):
        SqlBase.__init__(self, "localhost", "root", "", "senate")

    # Get list of speakers
    def getspeakerlist(self):
        query = "select distinct(speaker) from transcriptlines order by speaker"
        return self.select_all(query)


    #  Get ids of textlines for specific speaker
    def getspeakertextlineids(self, speaker):

        speakername = self.preprocess_singlequotes(speaker)
        query = "select id from transcriptlines where speaker='{0}' order by id".format(speakername)
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
