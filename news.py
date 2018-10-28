import basics
from datetime import datetime, timedelta


def get_news(ticker):

    decoded_item = basics.decode(ticker)
    stream = decoded_item.find("div", id="quoteNewsStream-0-Stream")
    news = stream.find_all(class_="js-stream-content Pos(r)")
    output = []
    now = datetime.now()

    for new in news:
        # 寻找主题以及超链接
        tittle = new.find(
            class_="Fw(b) Fz(20px) Lh(23px) LineClamp(2,46px) Fz(17px)--sm1024 Lh(19px)--sm1024 LineClamp(2,38px)--sm1024 Td(n) C(#0078ff):h C(#000)")
        tittle_link = tittle['href']

        # 改写超链接
        if tittle_link[0] != 'h':
            tittle_link = 'https://finance.yahoo.com' + tittle_link

        # 寻找时间
        time_ago = new.find(class_="C(#959595) Fz(11px) D(ib) Mb(6px)")
        if time_ago is None:
            print('adv:' + tittle.get_text())
            continue

        # 根据经过的时间推算出以前的时间
        time_ago = time_ago.contents[-1].get_text()
        interval = time_ago.split(' ')
        pub_time = 0

        if interval[0] == 'yesterday':
            ago = now + timedelta(days=(-1))
            pub_time = ago.strftime('%Y-%m-%d')
        elif interval[1] == 'minutes':
            ago = now + timedelta(minutes=(-int(interval[0])))
            pub_time = ago.strftime('%Y-%m-%d %H:%M')
        elif interval[1] == 'hours':
            ago = now + timedelta(hours=(-int(interval[0])))
            pub_time = ago.strftime('%Y-%m-%d %H')
        elif interval[1] == 'days':
            ago = now + timedelta(days=(-int(interval[0])))
            pub_time = ago.strftime('%Y-%m-%d')

        # 最终输出

        output.append([tittle.get_text(), tittle_link, pub_time])

    return output


if __name__ == '__main__':
    a = get_news("AAPL")
    print(a)





