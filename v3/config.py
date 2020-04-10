from typing import Dict

rindex_path: str = 'rindex.o2'
crawler_obj_path: str = 'cralwer_obj.o2'
timeout: int = 10
headers: Dict[str, str] = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) \
Gecko/20100101 Firefox/68.0'}
base_url_regex: str = r'((https://|http://).\w+\.\w+)'

seed = 'http://hiddenwikitor.com'
max_title_len = 200
