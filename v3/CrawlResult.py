from typing import List, Dict

class Result:
    def __init__(self, url: str, title: str, ft: Dict[str, int]):
        self.url: str = url
        self.title: str = title
        self.ft: Dict[str, int] = ft
