import urllib2
import os, json
import website.wsgi
from datetime import datetime, timedelta
from mathtutor.models import Result, ParentFormResult
from parserclasses import ResponseParser, ParentFormParser

# ADD ADDITIONAL QUERY PARAM FOR SITE
_API_URL = 'https://uprogram-math.herokuapp.com/results?site=reading'
_PARENT_FORM_URL ='https://uprogram-math.herokuapp.com/parentforms/'
_USER = os.getenv("USER_ID")
_TOKEN = os.getenv('API_TOKEN')

def get_response(URL):
    req = urllib2.Request(URL)
    req.add_header("Authorization", "Token {}".format(_TOKEN))
    response = urllib2.urlopen(req)
    if response.code == 200:
        return response
    else:
        return False

def main():
    print "Begin: {}".format(datetime.now())
    response = get_response(_API_URL)
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

def parentforms():
    response = get_response(_PARENT_FORM_URL)
    if not response:
        print "Repsonse for parent forms was not 200"
    else:
        blkUpdateList = []
        parser = ParentFormParser()
        data = json.loads(response.read())
        for item in data['results']:
            created, obj = parser.parse_response(item)
            if not created:
                pass
            else:
                blkUpdateList.append(obj)
        ParentFormResult.objects.bulk_create(blkUpdateList)
    print "Finished updated parent forms: {}".format(datetime.now())

if __name__ == "__main__":
    parentforms()
    main()
