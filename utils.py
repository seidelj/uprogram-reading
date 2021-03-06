import urllib2
import os, json
import website.wsgi
from datetime import datetime, timedelta
from mathtutor.models import Result
from parserclasses import ResponseParser

# ADD ADDITIONAL QUERY PARAM FOR SITE
_API_URL = 'https://uprogram-math.herokuapp.com/results?site=reading'
_USER = os.getenv("USER_ID")
_TOKEN = os.getenv('API_TOKEN')

def get_response():
    print _TOKEN
    req = urllib2.Request(_API_URL)
    req.add_header("Authorization", "Token {}".format(_TOKEN))
    response = urllib2.urlopen(req)
    if response.code == 200:
        return response
    else:
        return False


def main():
    print "Begin: {}".format(datetime.now())
    response = get_response()
    if not response:
        print "Response was not 200"
    else:
        blkUpdateList = []
        parser = ResponseParser()
        data = json.loads(response.read())
        for item in data['results']:
            created, obj = parser.parse_response(item)
            if not created:
                pass
            else:
                blkUpdateList.append(obj)
        Result.objects.bulk_create(blkUpdateList)
    print "Finished updating results: {}".format(datetime.now())

if __name__ == "__main__":
    main()
