#!/usr/bin/env python3

import pickle
import math
from CrawlResult import Result
from Rindex import Rindex
from typing import List
import config
from main import Spider

def load_index() -> List[Result]:
    with open(config.crawler_obj_path, 'rb') as f:
        crawlerobj = pickle.load(f)
        index = crawlerobj.index
    return index


def write_rev_index(rindex) -> None:
    with open(config.rindex_path, 'wb') as f:
        pickle.dump(rindex, f)

def rev_index():
    index = load_index()
    rindex = Rindex()

    for i, v in enumerate(index):
        print('[%d of %d] indexing %s' % (i, len(index), v.url))

        for token in set(v.ft.keys()):
            if token in rindex:
                rindex[token].append(v)
                
            else:
                rindex[token] = [v]
        
    rindex.page_count = len(index)
    write_rev_index(rindex)
    print('\n\n[+] DONE\n  [+] indexed %d keywords' % len(rindex.items()))

if __name__ == '__main__':
    rev_index()
