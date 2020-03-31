from datetime import datetime
import time


def get_time():
    time_str=datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S")
    return time_str


# def insert_hotsearch():


if __name__== '__main__':
    print(get_time())