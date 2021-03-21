#!/usr/bin/env python3
#webio.py

import cloudscraper

def get_web_content(url):
    print("---- Start Downloading ----")
    scraper = cloudscraper.create_scraper()
    result = scraper.get(url).text
    print("---- End Downloading ----\n")

    return result
