from abc import abstractmethod, ABC
from morsa import DORK_FILE_PATH
from morsa.my_yaml import load_yaml


class AbstractSearcher(ABC):
    def __init__(self, search_engine: str) -> None:
        self.url = f'https://www.{search_engine}/search?q='
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
            'Referer': f'https://www.{search_engine}/'
        }
        
    
    @abstractmethod
    def search(self, dominio, dork, limit) -> list:
        # TODO
        return  [{}]
