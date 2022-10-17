from morsa.abstract_searcher import AbstractSearcher
from bs4 import BeautifulSoup
import requests
import logging
from morsa.exception_capado import CapadoException
from tenacity import retry, retry_if_exception_type, wait_exponential, after_log


class BingSearcher(AbstractSearcher):

    __logger= logging.getLogger(__name__)

    def __init__(self):
        super().__init__('bing.com')
        self.session = requests.session()
    
    def _search_action(self, url, headers=None):
        self.__logger.debug('Requesting the page: %s',url)
        page = requests.get(url, headers=headers)
        return page

    def _parse_urls(self, html):
        soup = BeautifulSoup(html, "html.parser")
        all_links = soup.find_all('li')
        return all_links

    def _get_search_query(self, dominio, dork):
        return f'{self.url}{dork}+site:{dominio}'
    
    @retry(
        retry=retry_if_exception_type(CapadoException),
        wait=wait_exponential(multiplier=1, min=4, max=900), 
    )
    def search(self, dominio, dork, limit):
        URL=self._get_search_query(dominio, dork)
        headers=self.headers
        limit_pages=limit
        links= []
        link_pagina_siguiente=[]
        a=None
        all_links=None
        while (limit_pages is None) or (limit_pages>0):
            pagina_siguiente=False
            page = self._search_action(URL, headers=headers)
            all_links = self._parse_urls(page.text)
            raise Exception(all_links)
            for link in all_links:
                if link.get('class') is not None:
                    if ('b_algo' in link.get('class')):
                        a=link.find('a')
                        try:
                            if 'href' in a.attrs:
                                links.append(a.get('href'))
                        except:
                            pass
                else:
                    all_links=link.find_all('a')
                    for hrefs in all_links:
                        if hrefs.get('class') is not None:
                            if ('sb_pagN' in hrefs.get('class')):
                                if hrefs.get('href') is not None:
                                    link_pagina_siguiente.append(hrefs.get('href'))
                                    URL="https://www.bing.com"+hrefs.get('href')
                                    pagina_siguiente=True
                                
            if limit_pages is not None:
                limit_pages-=1
            if len(link_pagina_siguiente)>1:
                if link_pagina_siguiente[len(link_pagina_siguiente)-2]==link_pagina_siguiente[len(link_pagina_siguiente)-1]:
                    self.__logger.debug('No more result for this search')
                    break
            if (len(links)==0) or (pagina_siguiente is False):
                break
        if len(links)==0:
            self.__logger.debug("No results found using the dork: "+dork+" and the dominio: "+dominio)
    
            self.__logger.debug("Checking for limits")
            url = "https://www.bing.com/search?q=perro+filetype:pdf+site:faada.org"
            page = self._search_action(url, headers=headers)
            all_links = [link for link in self._parse_urls(page.text) if link.get('class') and 'b_algo' in link.get('class')]
            if len(all_links) == 0:
                self.__logger.warning("Alcanzado límite de búsqueda.")
                raise CapadoException("Alcanzado limite de busqueda.")
            #else:
                #self.__logger.debug(f'Debug results N={len(all_links)}, example={all_links[:2]}')
            
        else:
            self.__logger.debug("There are "+str(len(links))+" results for the dork: "+dork+" and the dominio: "+dominio)

        return links
