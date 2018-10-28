import basics

headers = {
              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
           }


# 分析网页，找到type内容

def generate_info_table(decoded_item):

    quote = decoded_item.find(id="quote-summary")

    left_table = quote.find(attrs={"data-test": "left-summary-table"})
    right_table = quote.find(attrs={"data-test": "right-summary-table"})

    left_stream = left_table.find_all(class_="Bxz(bb) Bdbw(1px) Bdbs(s) Bdc($c-fuji-grey-c) H(36px) ")
    left_stream.append(left_table.find(class_="Bxz(bb) Bdbw(1px) Bdbs(s) Bdc($c-fuji-grey-c) H(36px) Bdbw(0)! "))
    right_stream = right_table.find_all(class_="Bxz(bb) Bdbw(1px) Bdbs(s) Bdc($c-fuji-grey-c) H(36px) ")
    right_stream.append(right_table.find(class_="Bxz(bb) Bdbw(1px) Bdbs(s) Bdc($c-fuji-grey-c) H(36px) Bdbw(0)! "))

    tables = [left_stream, right_stream]

    return tables


def get_price(decoded_item):

    tittle = decoded_item.find(id="quote-header-info")

    price = tittle.find(class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)")
    info = price.get_text()

    return info


def get_info(type, info_table):

    if type == 'volume':  # 1,7
        x = 0
        y = 6
    elif type == 'avg_volume':  # 1,8
        x = 0
        y = 7
    elif type == 'price':
        x = None
        y = None
    elif type == 'market_cap':  # 2,1
        x = 1
        y = 0
    elif type == 'beta':  # 2,2
        x = 1
        y = 1
    elif type == 'pe_ratio':  # 2,3
        x = 1
        y = 2
    elif type == 'eps':  # 2,4
        x = 1
        y = 3
    elif type == 'earning_date':  # 2,5
        x = 1
        y = 4
    elif type == 'dividend_yield':  # 2,6
        x = 1
        y = 5
    else:
        raise Exception('fck you')

    info = info_table[x][y].contents[1].get_text()

    return info


if __name__ == '__main__':

    decoded_item = basics.decode('AAPL')
    table = generate_info_table(decoded_item)
    response = get_info('avg_volume', table)
    price = get_price(decoded_item)
    print(response, price)






