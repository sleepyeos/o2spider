#!/usr/bin/env python3

import config
import pickle
from main import *

if __name__ == '__main__':
    print('[i] attempting load')
    with open(config.crawler_obj_path, 'rb') as f:
        cobj = pickle.load(f)

    print('[i] loaded crawler...')
    queue_item_one = cobj.queue[0]
    cobj.queue = [x for x in cobj.queue if '.epub' not in x]
    print('[+ ]First queue item removed: %s' % queue_item_one)

    with open(config.crawler_obj_path, 'wb') as f:
        pickle.dump(cobj, f)

    print('[i] saved')
