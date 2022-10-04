from abstract_searcher import AbstractSearcher

class GoogleSearcher(AbstractSearcher):
    def __init__(self):
        super().__init__('google.com')
    
    def search(self, dominio, dork, limit):
        parent_search = super().search(dominio, dork, limit)
        a = self._paginator()
        return parent_search.func(a)
    
    def _paginator(self):
        pass