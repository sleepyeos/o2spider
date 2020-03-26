#!/usr/bin/env python3

import re
import sys
import time
import pickle
import os.path
import requests
from typing import List
from CrawlResult import CrawlResult
from bs4 import BeautifulSoup as BS


class Crawler:
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0'}
    base_url_pattern = r'((https://|http://).\w+\.\w+)'
    index_path = 'index.dat'

    def __init__(self, seed):
        self.seed = seed
        self.index = Crawler.load_index()
        print('[+] Total pages indexed: %d' % len(self.index.items()))

    @staticmethod
    def normalize_tokens(tokens: str):
        return tokens\
        .replace(',','')\
        .replace('.','')\
        .replace('!','')\
        .replace('?','')\
        .replace('(','')\
        .replace(')','')\
        .lower()\
        .split()

    @staticmethod
    def save_index(index):
        with open(Crawler.index_path, 'wb') as f:
            pickle.dump(index, f)

    @staticmethod
    def load_index():
        if not os.path.isfile(Crawler.index_path):
            return {}
        else:
            with open(Crawler.index_path, 'rb') as f:
                return pickle.load(f)

    @staticmethod
    def fix_relative_link(base_url: str, link_url: str) -> str:
        base_url = re.search(Crawler.base_url_pattern, base_url).group(0)
        fixed_url = link_url
        if base_url not in link_url and 'http' not in link_url:
            if base_url[-1] != '/' and link_url[0] != '/':
                base_url = base_url + '/'
            fixed_url = base_url + link_url
        return fixed_url

    @staticmethod
    def get_links(soup: BS, url: str) -> List[str]:
        anchors = soup.findAll('a')
        links = []
        for a in anchors:
            if 'href' in a.attrs:
                links.append(a.attrs['href'])
        return links

    def crawl(self):
        to_visit = [self.seed]
        visited = []

        while len(to_visit) > 0:
            current_url = to_visit[0]
            to_visit.remove(current_url)

            try:
                if current_url not in visited:
                    visited.append(current_url)
                    res = requests.get(current_url, headers=Crawler.headers, timeout=10)
                    soup = BS(res.content, 'lxml')
                    title = soup.title.text
                    print('[+] ' + current_url + ' | ' + title)

                    tokens: List[str] = Crawler.normalize_tokens(soup.get_text() + ' ' + title)

                    result = CrawlResult(res.url, tokens, title)
                    self.index[res.url] = result
                    Crawler.save_index(self.index)

                    links = Crawler.get_links(soup, res.url)
                    links = [Crawler.fix_relative_link(res.url, l) \
                             for l in links if '#' not in l]

                    #Only crawl darknet sites
                    links = [l for l in links if 'onion' in l]

                    to_visit.extend(links)
                    
            except Exception as e:
                print('[-] ' + current_url)
                print(e)

if __name__ == '__main__':
    c = Crawler(sys.argv[1])
    c.crawl()
