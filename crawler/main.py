import get_data
import basics
from openpyxl import load_workbook
from datetime import datetime, timedelta
import sched, time
import config

## Sched for periodically fetching stock data
schedule = sched.scheduler(time.time, time.sleep)

# Check if database.xlsx exists
from pathlib import Path
my_file = Path('datas/database.xlsx')
if my_file.is_file():
    print('database.xlsx exists, using it.')
else:
    print('database.xlsx does NOT exists')
    import initialization
    initialization.init()
    print('Auto generated')

# Generate flags for fetching non-price stats
global flag_fetch_info, flag_fetch_divided
flag_fetch_info = False
flag_fetch_divided = False

# 启动时先进行一次所有搜索
# 整体思路是：半小时爬一次股价，再爬股价的时候检查时间有没有到 一天/三天，如果到了的话顺便分析一下剩下的


def set_cycle(times):
    for x in range(times):
        # runs every three day
        schedule.enter(86400 * 3 * x, 1, trigger_fetch_divided)
    for x in range(3 * times):
        # runs daily
        schedule.enter(86400*x, 2, trigger_fetch_info)
    for x in range(times * 24 * 2 * 3):
        # runs every 30 min
        schedule.enter(1800*x, 3, main_action)

def trigger_fetch_info():
    global flag_fetch_info
    flag_fetch_info = True

def trigger_fetch_divided():
    global flag_fetch_divided
    flag_fetch_divided = True

def decode_ticker(ticker):
    print("Fetching " + ticker)
    for retry in range(5):
        try:
            decoded_item = basics.decode(ticker)
            break
        except UnicodeDecodeError as err:
            if retry < 4:
                print('Network error, retrying', retry+1)
            else:
                print('Unable to fetch', ticker, '\n', err)
                raise NameError('Program Aborting')
    return decoded_item

def fetch_ticker_price(decoded_item):
    value_inserted = []
    time = datetime.now()
    value_inserted.append(time.strftime('%Y-%m-%d %H:%M'))
    price = get_data.get_price(decoded_item)
    value_inserted.append(price)
    return value_inserted

def main_action():
    global flag_fetch_info, flag_fetch_divided
    wb = load_workbook('datas/database.xlsx')

    if flag_fetch_info:
        for ticker in config.tickers:
            decoded_item = decode_ticker(ticker)
            value_inserted = fetch_ticker_price(decoded_item)

            # Structurize fetched non-price data
            table = get_data.generate_info_table(decoded_item)

            pe_ratio = get_data.get_info("pe_ratio", table)
            value_inserted.append(pe_ratio)
            volume = get_data.get_info("volume", table)
            value_inserted.append(volume)
            avg_volume = get_data.get_info("avg_volume", table)
            value_inserted.append(avg_volume)
            beta = get_data.get_info("beta", table)
            value_inserted.append(beta)
            market_cap = get_data.get_info("market_cap", table)
            value_inserted.append(market_cap)
            eps = get_data.get_info("eps", table)
            value_inserted.append(eps)
            if flag_fetch_divided:
                earning_date = get_data.get_info("earning_date", table)
                value_inserted.append(earning_date)
                dividend_yield = get_data.get_info("dividend_yield", table)
                value_inserted.append(dividend_yield)

            wb[ticker].append(value_inserted)
            print(value_inserted)
            wb.save('datas/database.xlsx')
            print('Workbook saved')

        flag_fetch_info = False
        flag_fetch_divided = False
    else:
        for ticker in config.tickers:
            decoded_item = decode_ticker(ticker)
            value_inserted = fetch_ticker_price(decoded_item)

            wb[ticker].append(value_inserted)
            print(value_inserted)
            wb.save('datas/database.xlsx')
            print('Workbook saved')
        # info = news.get_news(ticker)


if __name__ == '__main__':
    set_cycle(10)  # The program will run for 10 * 3 = 30 days
    schedule.run()
