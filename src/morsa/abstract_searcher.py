from abc import abstractmethod, ABC
from morsa import DORK_FILE_PATH
from morsa.my_yaml import load_yaml


class AbstractSearcher(ABC):
    def __init__(self, search_engine: str) -> None:
        self.url = f'https://www.{search_engine}/search?q='
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
        self.headers = {
            'User-Agent': user_agent,
            'Referer': 'https://www.{search_engine}/'
        }
        
    
    @abstractmethod
    def search(self, dominio, dork, limit) -> list:
        # TODO
        return  [{}]