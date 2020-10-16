"""
MarketNewsUnitTest.py
Unit testing for MarketNews class.
Author: Stephen Kenyon
Date: 10/15/2020
Copyright 2020, Rutgers MBS, NJBDA, F+S Produce
"""

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
        lookup_abr_v = 'POTS'
        lookup_name_v = 'POTATOES'
        lokup_abr_f = 'APLCID'
        lookup_name_f = 'APPLE CIDER'
        path_v = 'potatoes.text'
        path_f = 'apple cider.text'
        out = self.news.get_data_file(lookup_name_f, '2020/10/15', path_f)
        out_v = self.news.get_data_file(lookup_name_v, '2020/10/15', path_v)
        print(out)
        print(out_v)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMarketNews)
    unittest.TextTestRunner().run(suite)