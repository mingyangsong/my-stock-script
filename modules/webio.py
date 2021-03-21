#!/usr/bin/env python3
#webio.py

import cloudscraper

def get_web_content(url):
    print("---- START DOWNLOADING ----")
    scraper = cloudscraper.create_scraper()
    result = scraper.get(url).text
    print("---- END DOWNLOADING ----\n")

    return result
