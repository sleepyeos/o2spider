#!/usr/bin/env python3

import pickle
from CrawlResult import CrawlResult

rindex_path = 'rev_index.dat'

def load_rindex() -> dict:
    with open(rindex_path, 'rb') as f:
        rindex = pickle.load(f)
    return rindex

def search(query: str, rindex: dict) -> list:
    terms = query.split()
    results = []
    
    for term in terms:
        try:
            term_results = rindex[term]
            term_results = [x for x in term_results if 'wiki' not in x[1].tokens]
            results.extend(term_results)
        except:
            pass

    results.sort(key=lambda x: x[0], reverse=True)
    return results

if __name__ == '__main__':
    rindex = load_rindex()
    while(True):
        print('[search] # ', end='')
        q = input()
        results = search(q, rindex)
        for r in results:
            print(r[1].title + '\n' + r[1].url + '\n\n')

        print('\n')
