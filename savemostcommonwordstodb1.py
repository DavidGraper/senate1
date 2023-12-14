import pickle
import SenateDB
import glob
import re
import json

def savemostcommonwordstodb():

    sdb = SenateDB.SenateData()

    for filename in glob.glob("/home/dgraper/Documents/Senate_Speaker_Pickles/*_mostcommonwords.pkl"):
        result = re.search(r"\/home\/dgraper\/Documents\/Senate_Speaker_Pickles\/(.*)_mostcommonwords\.pkl", filename)
        speakername = "{0}".format(result.groups(0)[0])

        # Create JSON objects for each speaker's most common words pickles and write to database
        filename = "/home/dgraper/Documents/Senate_Speaker_Pickles/{0}_mostcommonwords.pkl".format(speakername)

        file = open(filename, 'rb')
        speakerwordcounts = pickle.load(file)
        file.close()

        jsontext = json.dumps(speakerwordcounts)

        jsontext = jsontext.replace("[", "")
        jsontext = jsontext.replace("]", "")

        # Reverse text of speaker name from filename to get id from code table
        speakername = speakername.replace("_", " ")
        print("Processing most common words for '{0}'".format(speakername))
        speakerid = sdb.getspeakerid(speakername)


        # Insert pickle data for senator
        sdb.insertspeakermostcommonwords(speakerid["id"], jsontext)
