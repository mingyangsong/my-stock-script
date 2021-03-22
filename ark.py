#!/usr/bin/env python3
# ark.py
### USE Eastern Standard Time

import os
import sys
import datetime
from datetime import date

sys.path.append("./modules")

from webio import get_web_content
from fileio import get_csv_file, write_csv_file

class ArkItem:
    """ARK """

    def __init__(self, fund, ticker, company, weight):
        self.fund = fund
        self.ticker = ticker
        self.company = company
        self.weight = float(weight)

    def print_str():
        return "\t{0}\t{:f}%".format(self.ticker, self.weight)


def get_ark_fund_fullname(type = "ARKK"):

    switcher = {
        "ARKK": "ARK_INNOVATION_ETF_ARKK_HOLDINGS",
        "ARKQ": "ARK_AUTONOMOUS_TECHNOLOGY_&_ROBOTICS_ETF_ARKQ_HOLDINGS",
        "ARKW": "ARK_NEXT_GENERATION_INTERNET_ETF_ARKW_HOLDINGS",
        "ARKG": "ARK_GENOMIC_REVOLUTION_MULTISECTOR_ETF_ARKG_HOLDINGS",
        "ARKF": "ARK_FINTECH_INNOVATION_ETF_ARKF_HOLDINGS",
        "PRNT": "THE_3D_PRINTING_ETF_PRNT_HOLDINGS"
    }
    return switcher.get(type, "ARK_FINTECH_INNOVATION_ETF_ARKF_HOLDINGS")


def list_to_ark_dict(item_list):
    ark_dict = {}
    for item in item_list:
        print(item)
        ark_dict[item[2]] = ArkItem(item[1], item[2], item[3], item[4])

    return ark_dict


def ark_holdings_clean(file_path, content, ark_fund_type, today_date):
    item_list = []

    for line in content.split('\n'):
        item = line.split(',')
        if len(item) > 1 and item[1] == ark_fund_type:
            fund = item[1]
            company = item[2].strip('"')
            ticker = item[3].strip('"')
            weight = item[7]
            item_list.append([today_date, fund, ticker, company, weight])

    write_csv_file(file_path, item_list)
    print("\n---- UPDATE COMPLETED ----\n")

    return item_list


def get_date_holdings(ark_fund_type, date, today_date):
    item_list = []
    file_path = "./results/{:s}_{:s}.csv".format(date, ark_fund_type)

    if os.path.isfile(file_path):
        item_list = get_csv_file(file_path)
    elif date == today_date:
        ark_url = "https://ark-funds.com/wp-content/fundsiteliterature/csv/{:s}.csv".format(get_ark_fund_fullname(ark_fund_type))
        item_list = ark_holdings_clean(file_path, get_web_content(ark_url), ark_fund_type, today_date)

    return list_to_ark_dict(item_list)


def main():
    ark_fund_type = "ARKF"
    if len(sys.argv) > 1: ark_fund_type = sys.argv[1].upper()
    today_date = (date.today() + datetime.timedelta(hours = -5)).strftime("%Y-%m-%d")

    ark_today_holdings = get_date_holdings(ark_fund_type, today_date, today_date)

    compare_days = 0
    if len(sys.argv) > 2: compare_days = int(sys.argv[2])


    if compare_days > 0:
        pre_date = (date.today() - datetime.timedelta(days = compare_days) + datetime.timedelta(hours = -5)).strftime("%Y-%m-%d")
        ark_pre_holdings = get_date_holdings(ark_fund_type, pre_date, today_date)
        print("----------------------------------------------------------------------------------------")
        print("Date: {}\tFund: {}\tCompare with: {}".format(today_date, get_ark_fund_fullname(ark_fund_type), pre_date))
        print("----------------------------------------------------------------------------------------")
        print("{:s}\t{:35s}\t{:8s}\t{:s}\t{:s}".format("No", "Company", "Ticker", "Weight" , "Weight Change"))
        count = 1
        liquidation_list = []
        for ticker in ark_today_holdings:
            item = ark_today_holdings[ticker]
            if ticker in ark_pre_holdings:
                print("{:d}\t{:35s}\t{:8s}\t{:.2f}%\t{:.2f}%".format(count, item.company, item.ticker, item.weight, item.weight - ark_pre_holdings[ticker].weight))
                count += 1
            elif not ark_pre_holdings:
                print("{:d}\t{:35s}\t{:8s}\t{:.2f}%\tNULL".format(count, item.company, item.ticker, item.weight))
                count += 1
            else:
                liquidation_list.append(item)

        for item in liquidation_list:
            print("{:d}\t{:35s}\t{:8s}\t{:.2f}%\tlIQUIDATION".format(count, item.company, item.ticker, item.weight))
            count += 1
    else:
        print("----------------------------------------------------------------------------------------")
        print("Date: {}\tFund: {}\n".format(today_date, get_ark_fund_fullname(ark_fund_type)))
        print("----------------------------------------------------------------------------------------")
        print("{:s}\t{:35s}\t{:8s}\t{:s}".format("No",  "Ticker", "Company", "Weight"))
        count = 1
        for ticker in ark_today_holdings:
            item = ark_today_holdings[ticker]
            print("{:d}\t{:35s}\t{:8s}\t{:.2f}%".format(count, item.company, item.ticker, item.weight))
            count += 1

    print()

    return

if __name__ == "__main__":
    main()
