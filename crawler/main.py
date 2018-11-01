import get_data
import basics
from openpyxl import load_workbook
from datetime import datetime, timedelta
import sched, time
import config



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


global reached_one_day, reached_three_day
reached_one_day = False
reached_three_day = False

# 启动时先进行一次所有搜索
# 整体思路是：半小时爬一次股价，再爬股价的时候检查时间有没有到 一天/三天，如果到了的话顺便分析一下剩下的


def set_cycle(times):  # 设定一个三天循环周期

    for x in range(times):  # 三天提醒
        schedule.enter(86400 * 3 * x, 1, set_one_date)

    for x in range(3*times):  # 一天提醒
        schedule.enter(86400*x, 2, set_three_date)

    for x in range(times*24*2*3):  # 半小时提醒
        schedule.enter(1800*x, 3, main_action)


def set_one_date():
    global reached_one_day
    reached_one_day = True


def set_three_date():
    global reached_three_day
    reached_three_day = True


def main_action():
    global reached_one_day, reached_three_day, decoded_item
    wb = load_workbook('datas/database.xlsx')

    for ticker in config.tickers:
        # ["price", "pe_ratio", "volume", "avg_volume", "beta", "market_cap", "eps", "earning_date", "dividend_yield"]
        print("download for " + ticker)
        for retires in range(5):  # 重试
            try:
                global decoded_item
                decoded_item = basics.decode(ticker)
                break
            except UnicodeDecodeError as e:
                print('Network error, retrying')

        if retires == 4:
            raise("Network is Fking slow")

        value_inserted = []  # 看上面注释
        time = datetime.now()
        value_inserted.append(time.strftime('%Y-%m-%d %H:%M'))
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

            reached_one_day = False

        if reached_three_day:  # 到三天了

            earning_date = get_data.get_info("earning_date", table)
            value_inserted.append(earning_date)

            dividend_yield = get_data.get_info("dividend_yield", table)
            value_inserted.append(dividend_yield)

            reached_three_day = False

        wb[ticker].append(value_inserted)
        print(value_inserted)
        wb.save('datas/database.xlsx')
        print('saved')
    # info = news.get_news(ticker)


if __name__ == '__main__':
    set_cycle(5)  # 设定15天
    schedule.run()
