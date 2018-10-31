import get_data
import basics
from openpyxl import load_workbook
from datetime import datetime, timedelta

import config

## Check if database.xlsx exists
from pathlib import Path
my_file = Path(config.wbpath + config.wbname)
if not my_file.is_file():
    import initialization
    initialization.init()

one_Day_date = datetime.now()
three_Day_date = datetime.now()
half_Hour_date = datetime.now()  # 启动时先进行一次所有搜索
# 整体思路是：半小时爬一次股价，再爬股价的时候检查时间有没有到 一天/三天，如果到了的话顺便分析一下剩下的


def main_action(one_day_date, three_day_date):

    wb = load_workbook(config.wbpath + config.wbname)
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    str_one = one_day_date.strftime('%Y-%m-%d %H:%M')  # 似乎不变成字符串形式不好抹掉秒后面的时间，不抹不好比
    str_three = three_day_date.strftime('%Y-%m-%d %H:%M')
    reached_one_day = now == str_one  # 是否到一天
    reached_three_day = now == str_three  # 是否到三天
    print(reached_one_day)
    print(reached_three_day)

    for ticker in config.tickers:
        # ["price", "pe_ratio", "volume", "avg_volume", "beta", "market_cap", "eps", "earning_date", "dividend_yield"]
        print("search for " + ticker)
        value_inserted = []  # 看上面注释
        time = datetime.now()
        value_inserted.append(time.strftime('%Y-%m-%d %H:%M'))

        decoded_item = basics.decode(ticker)
        table = get_data.generate_info_table(decoded_item)

        price = get_data.get_price(decoded_item)  # 半小时找price
        value_inserted.append(price)

        if reached_one_day:  # 到一天了

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

            one_day_date = one_day_date + timedelta(days=1)

        if reached_three_day:  # 到三天了

            earning_date = get_data.get_info("earning_date", table)
            value_inserted.append(earning_date)

            dividend_yield = get_data.get_info("dividend_yield", table)
            value_inserted.append(dividend_yield)

            three_day_date = three_day_date + timedelta(days=3)

        wb[ticker].append(value_inserted)
        print(value_inserted)
        wb.save(config.wbname)
        print('saved')
    # info = news.get_news(ticker)

    return one_day_date, three_day_date


while True:  # 一直执行
    current = datetime.now().strftime('%Y-%m-%d %H:%M')
    str_half = half_Hour_date.strftime('%Y-%m-%d %H:%M')
    if current == str_half:
        print(current)
        one_Day_date, three_Day_date = main_action(one_Day_date, three_Day_date)
        half_Hour_date = half_Hour_date + timedelta(minutes=30)
