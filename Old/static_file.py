import pickle
import os
import datetime

current_path = os.path.dirname(__file__)
name = "variables.txt"


def initialize(fname):
    file = open("datas/" + name, "wb")
    data = {
        "half_hour_date": datetime.datetime.now(),
        "one_day_date": datetime.datetime.now(),
        "three_day_date": datetime.datetime.now(),
        "finished": [],
        "tickers": []
    }
    print(data)
    pickle.dump(data, file)


def set_var(var, value):
    file = open("/datas/" + name, "rb+")
    data = pickle.load(file)
    data[var] = value
    print(data)
    pickle.dump(data, file)


def get_var(var):
    file = open("/datas/" + name, "rb+")
    data = pickle.load(file)
    return data[var]


if __name__ == '__main__':
    initialize(name)