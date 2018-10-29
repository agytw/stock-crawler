import get_data
import basics
from openpyxl import load_workbook
from datetime import datetime, timedelta

tickers = ['AAPL', "GOOGL"]

one_Day_date = datetime.now()
three_Day_date = datetime.now()
half_Hour_date = datetime.now()


def main_action(one_day_date, three_day_date):

    wb = load_workbook('database.xlsx')
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    str_one = one_day_date.strftime('%Y-%m-%d %H:%M')
    str_three = three_day_date.strftime('%Y-%m-%d %H:%M')
    reached_one_day = now == str_one
    reached_three_day = now == str_three
    print(reached_one_day)
    print(reached_three_day)

    for ticker in tickers:
        # ["price", "pe_ratio", "volume", "avg_volume", "beta", "market_cap", "eps", "earning_date", "dividend_yield"]
        print("search for " + ticker)
        value_inserted = []
        time = datetime.now()
        value_inserted.append(time.strftime('%Y-%m-%d %H:%M'))

        decoded_item = basics.decode(ticker)
        table = get_data.generate_info_table(decoded_item)

        price = get_data.get_price(decoded_item)
        value_inserted.append(price)

        if reached_one_day:

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

        if reached_three_day:

            earning_date = get_data.get_info("earning_date", table)
            value_inserted.append(earning_date)

            dividend_yield = get_data.get_info("dividend_yield", table)
            value_inserted.append(dividend_yield)

            three_day_date = three_day_date + timedelta(days=3)

        wb[ticker].append(value_inserted)
        print(value_inserted)

    wb.save('database.xlsx')
    print('saved')
    # info = news.get_news(ticker)

    return one_day_date, three_day_date


while True:
    current = datetime.now().strftime('%Y-%m-%d %H:%M')
    str_half = half_Hour_date.strftime('%Y-%m-%d %H:%M')
    if current == str_half:
        print(current)
        one_Day_date, three_Day_date = main_action(one_Day_date, three_Day_date)
        half_Hour_date = half_Hour_date + timedelta(minutes=30)