from morsa.abstract_searcher import AbstractSearcher
from bs4 import BeautifulSoup
import requests
import logging


class BingSearcher(AbstractSearcher):

    __logger= logging.getLogger(__name__)

    def __init__(self):
        super().__init__('bing.com')
    
    def search(self, domain, dork, limit):
        URL=f'{self.url}{dork}+site:{domain}'
        headers=self.headers
        session = requests.session()
        limit_pages=limit
        links= []
        link_pagina_siguiente=[]
        a=None
        all_links=None
        while (limit_pages is None) or (limit_pages>0):
            pagina_siguiente=False
            page = requests.get(URL, headers=headers)
            self.__logger.debug('Requesting the page: %s',URL)
            html=page.text
            soup = BeautifulSoup(html, "html.parser")
            for link in soup.find_all('li'):
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
                            if ('sb_pagN' in hrefs.get('class')) and ('sb_pagN_bp' in hrefs.get('class')):
                                if hrefs.get('href') is not None:
                                    link_pagina_siguiente.append(hrefs.get('href'))
                                    URL="https://www.bing.com"+hrefs.get('href')
                                    pagina_siguiente=True
                            else:
                                pagina_siguiente=False
                                
            if limit_pages is not None:
                limit_pages-=1
            if len(link_pagina_siguiente)>1:
                if link_pagina_siguiente[len(link_pagina_siguiente)-2]==link_pagina_siguiente[len(link_pagina_siguiente)-1]:
                    self.__logger.debug('No more result for this search')
                    break
            if (len(links)==0) or (pagina_siguiente is False):
                break
        if len(links)==0:
            self.__logger.debug("No results found using the dork: "+dork+" and the domain: "+domain)
        else:
            self.__logger.debug("There are "+str(len(links))+" results for the dork: "+dork+" and the domain: "+domain)

        return links