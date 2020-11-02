"""
MarketNewsUnitTest.py
Unit testing for MarketNews class.
Author: Stephen Kenyon
Date: 10/15/2020
Copyright 2020, Rutgers MBS, NJBDA, F+S Produce
"""

import pandas as pd
import unittest
from MarketNews import MarketNews

class TestMarketNews(unittest.TestCase):
    def setUp(self):
        self.news = MarketNews()
    
    def test_MarketNewsInit_fruits(self):
        fruit_dict = {'WMEL': 'WATERMELONS', 'APLCID': 'APPLE CIDER',
                     'CANT': 'CANTALOUPS', 'MANGO': 'MANGOES'}
        self.assertEqual(fruit_dict, self.news.fruit_dict)
    
    def test_MarketNewsInit_veg(self):
        veg_dict = {'POTS': 'POTATOES', 'CAB': 'CABBAGE', 'CHAY': 'CHAYOTE',
                   'CARR': 'CARROTS'}
        self.assertEqual(veg_dict, self.news.veg_dict)
    
    def test_download_xml(self):
        url = "https://www.marketnews.usda.gov/mnp/fv-report-top-filters?&commAbr=CARR&repType=termPriceDaily&navType=byComm&locName=&navClass=VEGETABLES&className=VEGETABLES&commName=CARROTS&type=termPrice&repDate=10%2F15%2F2020&endDate=10%2F15%2F2020&format=xml&rebuild=false"
        self.news._download_xml(url)
    
    def test_download_txt(self):
        url = "https://www.marketnews.usda.gov/mnp/fv-report-top-filters?&commAbr=CARR&repType=termPriceDaily&navType=byComm&locName=&navClass=VEGETABLES&className=VEGETABLES&commName=CARROTS&type=termPrice&repDate=10%2F15%2F2020&endDate=10%2F15%2F2020&format=text&rebuild=false"
        self.news._download_txt(url)
        
    def test_download_excel(self):
        url = "https://www.marketnews.usda.gov/mnp/fv-report-top-filters?&commAbr=CARR&repType=termPriceDaily&navType=byComm&locName=&navClass=VEGETABLES&className=VEGETABLES&commName=CARROTS&type=termPrice&repDate=10%2F15%2F2020&endDate=10%2F15%2F2020&format=excel&rebuild=false"
        self.news._download_excel(url)
        
    def test_get_data_file_abr_lookup(self):
        lookup_name_v = 'POTATOES'
        lookup_name_f = 'APPLE CIDER'
        path_v = 'potatoes.txt'
        path_f = 'apple cider.txt'
        out = self.news.get_data_file(lookup_name_f, '2020/10/15', path_f)
        out_v = self.news.get_data_file(lookup_name_v, '2020/10/15', path_v)
        print(out)
        print(out_v)

    def test_get_data_file_lookup_not_found(self):
        lookup_name = 'potatoes'
        lookup_name2 = 'fries'
        date = '2020/10/15'
        path = 'blank.txt'
        self.assertRaises(ValueError, self.news.get_data_file, lookup_name, date, path)
        self.assertRaises(ValueError, self.news.get_data_file, lookup_name2, date, path)
    
    def test_get_data_file_force_weekday(self):
        weekend_date_sat = '2020/10/10'
        weekend_date_sun = '2020/10/11'
        path = 'sat.txt'
        path = 'sun.txt'
        lookup_name = 'POTATOES'
        url_sat = self.news.get_data_file(lookup_name, weekend_date_sat, path)
        url_sun = self.news.get_data_file(lookup_name, weekend_date_sun, path)
        self.assertEqual(url_sat, url_sun)

    def test_get_data_file_not_implemented(self):
        name = 'POTATOES'
        date = '2020/10/15'
        path = 'blah.txt'
        self.assertRaises(NotImplementedError, self.news.get_data_file, name, date, path, file_type="xlsx")
    
    def test_get_data_file_bad_date(self):
        date = '10/15/2020'
        date2 = '10-15-2020'
        name = 'POTATOES'
        path = 'blah.txt'
        self.assertRaises(ValueError, self.news.get_data_file, name, date, path)
        self.assertRaises(ValueError, self.news.get_data_file, name, date2, path)
    
    def test_get_data_file_one_week(self):
        start_date = '2020/10/5'
        end_date = '2020/10/9'
        name = 'POTATOES'
        path = 'one_week.xls'
        self.news.get_data_file(name, start_date, path, file_type='xls', end_date=end_date)
    
    def test_get_date_file_xml(self):
        date = '2020/10/15'
        name = 'POTATOES'
        self.news.get_data_file(name, date, 'blah.xml', file_type='xml')
    
    def test_stream_xml(self):
        url = "https://www.marketnews.usda.gov/mnp/fv-report-top-filters?&commAbr=CARR&repType=termPriceDaily&navType=byComm&locName=&navClass=VEGETABLES&className=VEGETABLES&commName=CARROTS&type=termPrice&repDate=10%2F15%2F2020&endDate=10%2F15%2F2020&format=xml&rebuild=false"
        self.assertRaises(NotImplementedError, self.news._stream_xml, url)

    def test_stream_txt(self):
        url = "https://www.marketnews.usda.gov/mnp/fv-report-top-filters?&commAbr=CARR&repType=termPriceDaily&navType=byComm&locName=&navClass=VEGETABLES&className=VEGETABLES&commName=CARROTS&type=termPrice&repDate=10%2F15%2F2020&endDate=10%2F15%2F2020&format=text&rebuild=false"
        self.assertRaises(NotImplementedError, self.news._stream_txt, url)

    def test_stream_excel(self):
        url = "https://www.marketnews.usda.gov/mnp/fv-report-top-filters?&commAbr=CARR&repType=termPriceDaily&navType=byComm&locName=&navClass=VEGETABLES&className=VEGETABLES&commName=CARROTS&type=termPrice&repDate=10%2F15%2F2020&endDate=10%2F15%2F2020&format=excel&rebuild=false"
        df = self.news._stream_excel(url)
        self.assertIsInstance(df, pd.DataFrame)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMarketNews)
    unittest.TextTestRunner().run(suite)