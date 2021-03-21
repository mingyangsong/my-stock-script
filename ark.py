#!/usr/bin/env python3
# ark.py

import sys
sys.path.append("./modules")

from webio import get_web_content
from datetime import date

class ArkItem:
    """ARK """

    def __init__(self, fund, company, ticker, weight):
        self.fund = fund
        self.company = company
        self.ticker = ticker
        self.weight = weight

    def print_str():
        return "\t{0}\t{:d}%".format(self.ticker, self.weight)


def get_ark_fund_filepath(type = "ARKK"):
    switcher = {
        "ARKK": "ARK_INNOVATION_ETF_ARKK_HOLDINGS",
        "ARKQ": "ARK_AUTONOMOUS_TECHNOLOGY_&_ROBOTICS_ETF_ARKQ_HOLDINGS",
        "ARKW": "ARK_NEXT_GENERATION_INTERNET_ETF_ARKW_HOLDINGS",
        "ARKG": "ARK_GENOMIC_REVOLUTION_MULTISECTOR_ETF_ARKG_HOLDINGS",
        "ARKF": "ARK_FINTECH_INNOVATION_ETF_ARKF_HOLDINGS",
        "PRNT": "THE_3D_PRINTING_ETF_PRNT_HOLDINGS"
    }
    return switcher.get(type, "ARK_FINTECH_INNOVATION_ETF_ARKF_HOLDINGS")


def ark_holdings_clean(content, ark_fund_type):
    item_list = []

    for line in content.split('\n'):
        item = line.split(',')
        if len(item) > 1 and item[1] == ark_fund_type:
            item_list.append(ArkItem(item[1], item[2].strip('"'), item[3].strip('"'), item[7]))

    return item_list

def main():
    ark_fund_type = "ARKF"
    if len(sys.argv) > 1: ark_fund_type = sys.argv[1]

    ark_url = "https://ark-funds.com/wp-content/fundsiteliterature/csv/{:s}.csv".format(get_ark_fund_filepath(ark_fund_type))
    result = get_web_content(ark_url)
    ark_holdings_list = ark_holdings_clean(result, ark_fund_type)

    print("Date: {}\tFund: {}\n".format(date.today().strftime("%Y-%m-%d"), ark_fund_type))
    print("{:s}\t{:35s}\t{:8s}\t{:s}".format("No", "Company", "Ticker", "Weight"))
    count = 1
    for item in ark_holdings_list:
        print("{:d}\t{:35s}\t{:8s}\t{:s}%".format(count, item.company, item.ticker, item.weight))
        count += 1

    print("\n---- UPDATE COMPLETED ----\n")
    return

if __name__ == "__main__":
    main()
