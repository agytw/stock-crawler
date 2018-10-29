from openpyxl import Workbook


def init(): # 创建一个新的excel，用tickers，当"数据库"

    wb = Workbook()
    first_time = True

    for ticker in tickers:

        if first_time:
            ws = wb.active
            ws.title = ticker
            first_time = False
        else:
            ws = wb.create_sheet(ticker)

        title = [" ", "price", "pe_ratio", "volume", "avg_volume", "beta", "market_cap", "eps", "earning_date", "dividend_yield"]
        ws.append(title)

    print(wb.sheetnames)
    wb.save('database.xlsx')


if __name__ == '__main__':
    tickers = ["AAPL", "GOOGL"]
    init()