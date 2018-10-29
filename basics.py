import urllib.request
from bs4 import BeautifulSoup

headers = {
              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
           }


def https_get(turl):
    request = urllib.request.Request(turl, headers=headers)
    response = urllib.request.urlopen(request)
    response = response.read().decode(encoding='UTF-8').strip()
    return response


def decode(ticker):
    url = 'https://finance.yahoo.com/quote/' + ticker + '?p=' + ticker + '&.tsrc=fin-srch'
    item = https_get(url)
    decoded = BeautifulSoup(item, "html.parser")
    return decoded
