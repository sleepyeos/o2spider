#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup as BS
from typing import Dict, List, Set
import config
from CrawlResult import Result
import os.path
import re
import pickle

class Spider:

    def __init__(self, seed: str):

        # initialize fields
        self.seed: str = seed
        self.queue: List[str] = [seed]
        self.history: Set[str] = set()
        self.index: List[Result] = []


    @staticmethod
    def fix_link(base_url: str, link_url: str) -> str:
        base_url = re.search(config.base_url_regex, base_url).group(0)
        fixed_url = link_url
        if base_url not in link_url and 'http' not in link_url:
            if base_url[-1] != '/' and link_url[0] != '/':
                base_url = base_url + '/'
            fixed_url = base_url + link_url
        if '?' in fixed_url:
            fixed_url = fixed_url.split('?')[0]
        if '#' in fixed_url:
            fixed_url = fixed_url.split('#')[0]
        if 'irc://' in fixed_url or 'gopher://' in fixed_url:
            fixed_url = ''
        return fixed_url

    @staticmethod
    def get_links(soup: BS) -> List[str]:
        anchors = soup.findAll('a')
        links = []
        for a in anchors:
            if 'href' in a.attrs:
                links.append(a.attrs['href'])
        return links

    @staticmethod
    def normalize_tokens(tokens: str) -> List[str]:
        return tokens\
        .replace(',',' ')\
        .replace('.',' ')\
        .replace('!',' ')\
        .replace('?',' ')\
        .replace('(',' ')\
        .replace(')',' ')\
        .replace(':',' ')\
        .replace(';',' ')\
        .replace('*',' ')\
        .lower()\
        .split()

    @staticmethod
    def freq_table(tokens: List[str]) -> Dict[str, int]:
        ft = {}
        for t in tokens:
            if t in ft:
                ft[t] += 1
            else:
                ft[t] = 1
        return ft

    @staticmethod
    def get_instance(seed: str):
        path: str = config.crawler_obj_path
        
        if os.path.isfile(path):
            with open(path, 'rb') as f:
                return pickle.load(f)
        else:
            return Spider(seed)


    def save_instance(self) -> None:
        path: str = config.crawler_obj_path

        with open(path, 'wb') as f:
            pickle.dump(self, f)

    def print_status(self) -> None:
        print('[history]: %d pages' % (len(self.history)))
        print('[queue]: %d urls' % (len(self.queue)))
        print('[index]: %d entries' % (len(self.index)))
        print('\n')
        
    def crawl(self) -> None:
        self.print_status()
        while len(self.queue) > 0:
            
            current_url = self.queue[0]
#            self.queue.remove(current_url)

            try:
                if current_url not in self.history:
#                    self.history.add(current_url)
                    res = requests.get(current_url,\
                                       headers=config.headers,\
                                       timeout=config.timeout)

                    soup: BS = BS(res.content, 'lxml')
                    title: str = soup.title.text
                    print('[+] ' + current_url + ' | ' + title)
                    tokens: List[str] = Spider.normalize_tokens(soup.get_text() +\
                                                                ' ' + title)
                    ft: Dict[str,int] = Spider.freq_table(tokens)
                    r: Result = Result(res.url, title, ft)
                    self.index.append(r)
                    
                    links = Spider.get_links(soup)
                    links = [Spider.fix_link(res.url, l) for l in links]
                    links = [l for l in links if 'onion' in l]
                    links = [l for l in links if '.m3u' not in l]
                    links = [l for l in links if '.xspf' not in l]
                    self.queue.extend(links)
                else:
                    print('[ i ] Skipping duplicate URL: %s' % (current_url))

            except Exception as e:
                print('[-] ' + current_url)
                print(e)
                print('\n')

            except KeyboardInterrupt:
                print("[ info ] keyboard interrupt, exiting after save")
                self.save_instance()
                exit()
                
            self.queue.remove(current_url)
            self.history.add(current_url)
            self.print_status()
            print('\n')
        
if __name__== '__main__':
    c: Spider = Spider.get_instance(config.seed)
    c.crawl()
    c.save_instance()
    print('[+] done' )
