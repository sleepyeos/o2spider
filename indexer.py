#!/usr/bin/env python3

import pickle
import math
from CrawlResult import CrawlResult

index_path = 'index.dat'
reverse_index_path = 'rev_index.dat'

def load_index() -> dict:
    with open(index_path, 'rb') as f:
        index = pickle.load(f)
    return index

def write_rev_index(rindex):
    with open(reverse_index_path, 'wb') as f:
        pickle.dump(rindex, f)

def rev_index():
    index = load_index()
    rindex = {}
    count = 1;
    
    for k,v in index.items():
        print('[%d of %d] indexing %s' % (count, len(index.items()), k))

        for token in set(v.tokens):
            if token in rindex:
                rindex[token].append((1 + math.log(v.tokens.count(token)), v))
            else:
                rindex[token] = [(1 + math.log(v.tokens.count(token)), v)]
        count += 1
    write_rev_index(rindex)
    print('\n\n[+] DONE\n  [+] indexed %d keywords' % len(rindex.items()))

if __name__ == '__main__':
    rev_index()
