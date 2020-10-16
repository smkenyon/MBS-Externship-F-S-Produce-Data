"""
MarketNews.py
Data handling class and methods for USDA Market News Specialty Crop Data: https://www.marketnews.usda.gov/mnp/fv-home
Author: Stephen Kenyon
Date: 10/15/2020
Copyright 2020, Rutgers MBS, NJBDA, F+S Produce
"""

import csv
import datetime
import requests
import shutil

class MarketNews:
    def __init__(self):
        self.__baselink = "https://www.marketnews.usda.gov/mnp/fv-report-top-filters?"
        self.__repType = "&repType=termPriceDaily"
        self.__navType = "&navType=byComm"
        self.__locName = "&locName="
        self.__type = "&type=termPrice"
        self.__rebuild = "&rebuild=false"
        self.fruit_dict = {}
        self.veg_dict = {}
        with open('fruits.txt', 'r') as fruit_lookup:
            csvreader = csv.reader(fruit_lookup, delimiter=',')
            for line in csvreader:
                self.fruit_dict[line[0]] = line[1].strip()
        with open('vegetables.txt', 'r') as veg_lookup:
            csvreader = csv.reader(veg_lookup, delimiter=',')
            for line in csvreader:
                self.veg_dict[line[0]] = line[1].strip()
                
    def _download_xml(self, url, path="test.xml"):
        try:
            with requests.get(url, stream=True) as r:
                with open(path, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
        except:
            print("File not downloaded")
            raise TimeoutError
    
    def _download_txt(self, url, path="test.txt"):
        try:
            with requests.get(url, stream=True) as r:
                with open(path, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
        except:
            print("File not downloaded")
            raise TimeoutError
    
    def _download_excel(self, url, path="test.xls"):
        try:
            with requests.get(url, stream=True) as r:
                with open(path, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
        except:
            print("File not downloaded")
            raise TimeoutError

    def _stream_xml(self):
        pass

    def _stream_txt(self):
        pass

    def _stream_excel(self):
        pass
         
    def get_data_file(self, name, date, path, file_type="text", **kwargs):
        """
        name: uppercase name of fruit or vegetable
        date: start date of query
        file_type: string: xml, excel, or text
        end_date: end date of query
        returns url: string: formatted url to generate query
        """
        abr = None
        food_type = None
        formatted_date = datetime.datetime.strptime(date, '%Y/%m/%d')
        end_date = formatted_date
        # check to see if name in dicts
        for fruit in self.fruit_dict:
            if name in self.fruit_dict[fruit]:
                abr = fruit
                food_type = "FRUITS"
                break
        for veg in self.veg_dict:
            if name in self.veg_dict[veg]:
                abr = veg
                food_type = "VEGETABLES"
                break
        if abr is None:
            print("Name not found.")
            raise ValueError
        
        # Market News only supports weekday for data pulls
        try:    
            weeknumber = formatted_date.weekday()
        except:
            print("Date not formatted correctly / Invalid Date.")
            raise ValueError
            
        if weeknumber > 4: 
            print("Entered date is a weekend. Using previous non-weekend date.")
            if weeknumber == 6:
                formatted_date = formatted_date - datetime.timedelta(days=2)
                end_date = end_date - datetime.timedelta(days=2)
            else:
                formatted_date = formatted_date - datetime.timedelta(days=1)
                end_date = end_date - datetime.timedelta(days=1)
                
        for k in kwargs:
            if k == "end_date":
                end_date = datetime.datetime.strptime(kwargs[k], '%Y/%m/%d')
                weeknumber = end_date.weekday()
                if weeknumber > 4:
                    print("Entered end date is a weekend. Using previous non-weekend date.")
                    if weeknumber == 6:
                        end_date = end_date - datetime.timedelta(days=2)
                    else:
                        end_date = end_date - datetime.timedelta(days=1)
                        
        start_year = str(formatted_date.year)
        start_month = str(formatted_date.month)
        start_day = str(formatted_date.day)
        start = start_month + "%2F" + start_day + "%2F" + start_year
        end_year = str(end_date.year)
        end_month = str(end_date.month)
        end_day = str(end_date.day)
        end = end_month + "%2F" + end_day + "%2F" + end_year
        
        name_list = name.split()
        if len(name_list) > 1:
            name = name_list[0] + "+" + name_list[1]
            
        url_stub = (self.__baselink + '&commAbr=' + abr + self.__repType + self.__navType
                    + '&navClass=' + food_type + '&className='
                    + food_type + '&commName=' + name + self.__type + '&repDate='
                    + start + '&endDate=' + end + self.__rebuild) 
        
        if file_type == "text":
            url = url_stub + '&format=text' + self.__rebuild
            self._download_txt(url, path)
        elif file_type == "xls":
            url = url_stub + '&format=excel' + self.__rebuild
            self._download_excel(url, path)
        elif file_type == "xml":
            url = url_stub + '&format=xml' + self.__rebuild
            self._download_xml(url, path)
        else:
            raise NotImplementedError
        #saved_path = None  # remove once formatting path is implemented
        return url
        
    def stream_datafile(self, name, date, **kwargs):
        """
        name: str name of the fruit or vegetable
        date: str, f%YYYY/%MM/%DD - start date
        end_date: str, f%YYYY/%MM/%DD, defaults to date
        returns: None
        """
        return None