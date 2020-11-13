"""
marketnews_db_pull_update.py
Download all commodities as specified in fruits.txt and vegetables.txt
Author: Stephen Kenyon
Date: 11/11/2020
Copyright 2020, Rutgers MBS, NJBDA, F&S Produce
"""

import os
import datetime
import time
import pandas as pd
from MarketNews import MarketNews

def create_data_folder():
    data_folder = "data"
    files = os.listdir()
    if data_folder not in files:
        os.mkdir("data")

def pull_all():
    files = os.listdir("data")
    if not files:
        news = MarketNews()
        start_date = "2020/10/1"  # limit to October 1st for testing, final version use 5 years
        end_date = datetime.date.today()
        end_date_format = str(end_date.year) + "/" + str(end_date.month) + "/" + str(end_date.day)
        str_start_date = "_2010_1_1_"
        str_end_date = str(end_date.year) + "_" + str(end_date.month) + "_" + str(end_date.day)
        for fruit in news.fruit_dict:
            name = news.fruit_dict[fruit]
            path = "data//" + name + str_start_date + str_end_date + ".csv"
            print("Querying Market News server for terminal market data: ", name, "start date = " , start_date, "end date = ", end_date_format)
            try:
                df = news.stream_datafile(name, start_date, end_date=end_date_format)
                print("Saving data to ", path)
                df.to_csv(path, chunksize=100)
                print("Finished saving data.")
            except:
                print("Failed to retrieve data.")
            time.sleep(3)  # wait 3 seconds to prevent server booting connection

        for vegetable in news.veg_dict:
            name = news.veg_dict[vegetable]
            path = "data//" + name + str_start_date + str_end_date + ".csv"
            print("Querying Market News server for terminal market data: ", name, "start date = " , start_date, "end date = ", end_date_format)
            try:
                df = news.stream_datafile(name, start_date, end_date=end_date_format)
                print("Saving data to ", path)
                df.to_csv(path, chunksize=100)
                print("Finished saving data.")
            except:
                print("Failed to retrieve data.")
            time.sleep(3)

def update_all():
    raise NotImplementedError

if __name__ == "__main__":
    create_data_folder()
    pull_all()
