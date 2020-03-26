#!/usr/bin/env python3

import re
import sys
import time
import pickle
import requests
from typing import List
from bs4 import BeautifulSoup as BS

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0'}
base_url_pattern = r'((https://|http://).\w+\.\w+)'

index = {}

def get_links(soup: BS, url: str) -> List[str]:
    anchors = soup.findAll('a')
    links = []
    for a in anchors:
        if 'href' in a.attrs:
            links.append(a.attrs['href'])
    return links

def fix_relative_link(base_url, link_url) -> str:
    base_url = re.search(base_url_pattern, base_url).group(0)
    fixed_url = link_url
    if base_url not in link_url and 'http' not in link_url:
        if base_url[-1] != '/' and link_url[0] != '/':
            base_url = base_url + '/'
        fixed_url = base_url + link_url
    return fixed_url

def get_title_words(soup: BS) -> set:
    pass

def get_page_words() -> set:
    pass

def add_to_index():
    pass

def save_index():
    pass

def load_index():
    pass

def query_term(term) -> List[str]:
    pass

def query_string(s):
    pass

def crawl(url):
    to_visit = [url]
    visited = []

    while len(to_visit) > 0:
        current_url = to_visit[0]
        to_visit.remove(current_url)

        try:
            if current_url not in visited:
                visited.append(current_url)
                res = requests.get(current_url, headers=headers, timeout=10)
                soup = BS(res.content, 'lxml')
                title = soup.title.text
                print('[+] ' + current_url + ' | ' + title)
                links = get_links(soup, res.url)
                links = [fix_relative_link(res.url, l) for l in links if '#' not in l]
                to_visit.extend(links)

        except Exception as e:
            print('[-] ' + current_url)

if __name__ == '__main__':
    crawl(sys.argv[1])
