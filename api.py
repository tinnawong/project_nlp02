# importing the requests library
import requests
import json
from sentiment_Analysis.sentiment import sentiment

"""
Endpoints
/v2/top-headlines
/v2/everything
/v2/sources

"""
class api :
    Endpoints = '/v2/top-headlines'
    keyword = ''
    apiKey = '104f961263884432b72969f263f2f060'
    country ='th'

    def getAPI(self,keyword="",pageSize="10",page='1',category=''):
        if (category!=''):
            URL = "https://newsapi.org" + self.Endpoints + "?" + "country=" + self.country + "&q=" +\
                  keyword + "&pageSize="+pageSize+"&page="+page+"&category="+category+"&apiKey=" + self.apiKey + ""
        else:
            URL = "https://newsapi.org" + self.Endpoints + "?" + "country=" + self.country + "&q=" + \
                  keyword + "&pageSize=" + pageSize +"&page="+page + "&apiKey=" + self.apiKey + ""
        data = requests.get(url = URL)
        print(URL)
        return data.json()

    # sent = sentiment()
    # sent.tran()
    # sent.analysis("ปลา")
if __name__ == '__main__':
    ss = api()
    da = ss.getAPI("","10",'2',"technology")
    print(json.dumps(da, indent=2,ensure_ascii=False))
