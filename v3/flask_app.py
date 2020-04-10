#!/usr/bin/env python3

from flask import Flask, render_template, request
import searcher
import pickle
import config

app = Flask(__name__)
rindex = searcher.load_rindex()

with open(config.crawler_obj_path, 'rb') as f:
    cobj = pickle.load(f)
    index = cobj.index

@app.route("/")
def hello():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q')
    results = searcher.search(query, rindex)
    for x in results:
        x.title = x.title[:config.max_title_len] + '...' if len(x.title) > config.max_title_len else x.title
    return render_template('results.html', results=results, count=len(results),query=query)

@app.route('/explore')
def explore():
    results = index
    for x in results:
        x.title = x.title[:config.max_title_len] + '...' if len(x.title) > config.max_title_len else x.title

    return render_template('results.html', results=results, count=len(index), query='[all]')
    
if __name__ == '__main__':
    app.run()
