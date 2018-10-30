import pickle
import os

current_path = os.path.dirname(__file__)
name = "variables.txt"


def initialize(fname):
    os.mknod(current_path + "/datas/" + fname)
    data = {
        "half_hour_date" : 0,


    }


def change_var(var, value):
    file = open(current_path + "/datas/" + name, "rb+")
