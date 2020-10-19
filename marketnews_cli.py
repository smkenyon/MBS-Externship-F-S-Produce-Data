"""
marketnews_cli.py
Command line interface for USDA MarketNews Specialty Produce Data
Author: Stephen Kenyon, stephen.kenyon@rutgers.edu
Date: 10/16/2020
Copyright 2020, Rutgers MBS, NJBDA, F+S Produce
"""

import argparse
import datetime
from MarketNews import MarketNews

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="Enter the commodity name in all-caps, plural, e.g. POTATOES.",
                        type=str)

    # optional arguments
    parser.add_argument("-s", "--start_date", help="Enter the start date. Defaults to current business day. Form: YYYY/MM/DD.")
    parser.add_argument("-e", "--end_date", help="Enter the end date. Defaults to same as start date. Form: YYYY/MM/DD.")
    parser.add_argument("-sv", "--save_file", help="Enter the filename, e.g. potatoes.xls",
                        type=str)

    args = parser.parse_args()
    commodity_name = args.name
    start_date = args.start_date
    end_date = args.end_date
    save_file = args.save_file
    if start_date is None: start_date = datetime.date.today()
    if end_date is None: end_date = start_date
    if save_file is None:
        save_file = (commodity_name + str(start_date.year) + str(start_date.month)
                    + str(start_date.day) + str(end_date.year) + str(end_date.month)
                    + str(end_date.day) + '.txt')
    if isinstance(start_date, datetime.date): start_date = start_date.strftime("%Y/%m/%d")
    if isinstance(end_date, datetime.date): end_date = end_date.strftime("%Y/%m/%d")
    news = MarketNews()
    file_type = save_file[-4:]
    
    if file_type == '.xls':
        file_type = 'xls'
    elif file_type == '.txt':
        file_type = 'text'
    elif file_type == '.xml':
        file_type = 'xml'
    else:
        raise NotImplementedError  # additional MarketNews files include PDF, not supported at this time
    
    news.get_data_file(commodity_name, start_date, save_file, file_type=file_type, end_date=end_date) 

if __name__ == "__main__":
    main()