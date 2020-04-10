#!/usr/bin/env python3

import pickle
from CrawlResult import Result
from typing import List
import math

rindex_path = 'rindex.o2'

def load_rindex() -> dict:
    with open(rindex_path, 'rb') as f:
        rindex = pickle.load(f)
    return rindex

def search(query: str, rindex: dict) -> list:
    query = query.lower()
    terms = query.split()
    results = []
    
    for term in terms:
        try:
            term_results = rindex[term]
            #term_results = [x for x in term_results if not ('hidden' in x.tokens and 'wiki' in x.tokens)]
            term_results = [x for x in term_results if not 'jh32yv' in x.url]
            term_results = [x for x in term_results if not 'wiki' in x.url]
            for t_r in term_results:
                tf = 1 + math.log(t_r.ft[term])
                idf = len(rindex[term]) / rindex.page_count

                if t_r not in results:
                    t_r.tfidf = tf*idf
                    results.append(t_r)
                else:
                    t_r.tfidf += tf*idf
                
                
                
        except:
            pass

    results = list(set(results))
    results.sort(key=lambda x:x.tfidf, reverse=True)
    print('Found %d results:\n\n' % len(results))
    return results


if __name__ == '__main__':
    rindex = load_rindex()
    while(True):
        print('[search] # ', end='')
        q = input()
        print('\n')
        results = search(q, rindex)
        for r in results:
            print('%s\n%s\n[relevance: %f]\n\n' % (r.title, r.url, r.tfidf))

        print('\n')
