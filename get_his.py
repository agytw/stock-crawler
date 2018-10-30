import basics
import time
import json
from openpyxl import load_workbook


def stamp2date(timestamp):
    time_local = time.localtime(timestamp)
    date = time.strftime("%Y-%m-%d %H:%M", time_local)
    return date


def date2stamp(date):
    time_array = time.strptime(date, "%Y-%m-%d %H:%M")
    timestamp = time.mktime(time_array)
    return timestamp


def get_his(ticker, time_start, time_end):

    interval = '1h'

    unix_time_start = date2stamp(time_start)
    unix_time_end = date2stamp(time_end)

    his_url = 'https://query1.finance.yahoo.com/v8/finance/chart/%s?symbol=%s&period1=%d&period2=%d&interval=%s&region=US' %(ticker, ticker,  unix_time_end, unix_time_start, interval)
    print(his_url)
    item = basics.https_get(his_url)
    stock_dict = json.loads(item)
    time_stamps = stock_dict["chart"]["result"][0]["timestamp"]
    current_price = stock_dict["chart"]["result"][0]["indicators"]["quote"][0]["close"]

    if len(time_stamps) != len(current_price):
        raise Exception("not equal!!")

    list_append = []

    for i in range(len(time_stamps)):
        list_append.append([stamp2date(time_stamps[i]), current_price[i]])

    return list_append


if __name__ == '__main__':
    wb = load_workbook('/Users/eric/PycharmProjects/孙嘉谷傻逼/database_his.xlsx')
    tickers = ["VOD", "YORW", "JVLAGRO"]
    for ticker in tickers:
        print(ticker)
        table = get_his(ticker, "2018-10-27 04:00", "2018-09-27 04:00")
        for history in table:
            wb[ticker].append(history)
        wb.save('/Users/eric/PycharmProjects/孙嘉谷傻逼/database_his.xlsx')
        print("saved")