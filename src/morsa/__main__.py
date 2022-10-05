from morsa.bing_searcher import BingSearcher
import sys
from openpyxl import load_workbook
from openpyxl import Workbook
from morsa.excel_dominio import read_excel
from morsa.hash import getmd5file
from morsa import NEW_EXCEL_FILE
from morsa import EXCEL_FILE
from morsa import DORK_FILE_PATH
import logging
from morsa.my_yaml import load_yaml
import click
import requests
from pathlib import Path

@click.command()
@click.option('--output_file',default=NEW_EXCEL_FILE, help='Archivo donde mostrar los resultados')
@click.option('--assets_file',default=EXCEL_FILE,help='Archivo excel con los activos')
@click.option('--dorks_file',default=DORK_FILE_PATH,help='Archivo YML con los dorks')
@click.option('--num_pages',default=None, type=int, help='Límite de páginas donde buscar')
@click.option('--domain',default=[],multiple=True,help='Dominio por el que filtrar al coger los activos')
def main(output_file, assets_file, dorks_file,num_pages, domain):
    logger = logging.getLogger("morsa")
    logging.basicConfig(filename='morsa_debug.log', filemode='w', format='%(asctime)s|%(levelname)s|%(name)s|%(message)s')
    handler  = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s|%(levelname)s|%(name)s|%(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    links={}
    aux_domain={}
    perros_links=[]
    PRUEBA_PDF = Path(__file__).parents[2] / 'prueba.pdf'
    response=None
    count_number_requests=0
    excel_data=read_excel(assets_file)
    file_dorks = load_yaml(dorks_file)
    my_searcher=BingSearcher()
    wb=Workbook()
    #wb.save(NEW_EXCEL_FILE)
    #wb2=load_workbook(NEW_EXCEL_FILE)
    ws=wb.active
    logger.debug("Excel to store results created")
    ws['A1'].value='País'
    ws['B1'].value='Entidad'
    ws['C1'].value='Dominio'
    ws['D1'].value='id_dork'
    ws['E1'].value='riesgo_dork'
    ws['F1'].value='url_resultado'
    ws['G1'].value='hash'
    wb.save(output_file)
    i=2
    if domain:
        for dominios in domain:
            if dominios in excel_data:
                aux_domain[dominios]=excel_data[dominios]
            else:
                logger.warning("No hay ningun activo con el dominio indicado %s", dominios)
    else:
        aux_domain=excel_data
    
    for dominio in aux_domain.values():
        for yml_dork in file_dorks['BING']:
            count_number_requests+=1
            dork=yml_dork['dorks']['dork']
            id_dork=yml_dork['dorks']['id_dork']
            riesgo_dork=yml_dork['dorks']['riesgo']
            country=dominio['pais']
            entidad=dominio['entidad']
            limit=num_pages
            aux_links = my_searcher.search(dominio['activo'],dork,limit)
            if count_number_requests>600:
                perros_links = my_searcher.search('google.com','perros',1)
                if len(perros_links)==0:
                    raise Exception(count_number_requests)
            if len(aux_links)>0:
                for url in aux_links:
                    if '.pdf' in url:
                        response=requests.get(url)
                        #Usar temp library python para crear archivs temporales
                        with open('prueba.pdf','wb') as pdf:
                            pdf.write(response.content) 
                        hash_value=getmd5file(PRUEBA_PDF)
                        ws['G'+str(i)].value=hash_value
                    ws['A'+str(i)].value=country
                    ws['B'+str(i)].value=entidad
                    ws['C'+str(i)].value=dominio['activo']
                    ws['D'+str(i)].value=dork
                    ws['E'+str(i)].value=riesgo_dork
                    ws['F'+str(i)].value=url
                    logger.debug("New results added to the excel")
                    i+=1
            wb.save(output_file)
           


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Exiting..')
        sys.exit()