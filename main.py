#!/usr/bin/env python3

import sys
import time
import requests
from bs4 import BeautifulSoup as BS

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0'}

def get_links(soup, url):
    anchors = soup.findAll('a')
    links = []
    for a in anchors:
        if 'href' in a.attrs:
            links.append(a.attrs['href'])

    links = [fix_relative_links(url, l) for l in links]
    return links

def fix_relative_links(base_url, link_url):
    fixed_url = link_url
    if base_url not in link_url and 'http' not in link_url:
        fixed_url = base_url + '/' + link_url
    return fixed_url
        
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
                links = [fix_relative_links(url, l) for l in links if '#' not in l]
                to_visit.extend(links)

        except Exception as e:
            print('[-] ' + current_url)

if __name__ == '__main__':
    crawl(sys.argv[1])
