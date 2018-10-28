import get_data
import basics
from openpyxl import load_workbook
from datetime import datetime

tickers = ['AAPL', "GOOGL"]
wb = load_workbook('database.xlsx')

for ticker in tickers:
    # title = ["price", "pe_ratio", "volume", "avg_volume", "beta", "market_cap", "eps", "earning_date", "dividend_yield"]
    value_inserted = []
    time = datetime.now()
    value_inserted.append(time.strftime('%Y-%m-%d %H:%M'))

    decoded_item = basics.decode(ticker)
    table = get_data.generate_info_table(decoded_item)

    price = get_data.get_price(decoded_item)
    value_inserted.append(price)

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

    earning_date = get_data.get_info("earning_date", table)
    value_inserted.append(earning_date)

    dividend_yield = get_data.get_info("dividend_yield", table)
    value_inserted.append(dividend_yield)

    wb[ticker].append(value_inserted)
    wb.save('database.xlsx')
    # info = news.get_news(ticker)
    print(value_inserted)


