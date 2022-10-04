def main():
    links={}
    
    with open("YML_Dorks.yml") as fichero:
        docs=yaml.safe_load(fichero)

    
    myfile=open('filenamee.txt', 'w')
    for yml_dork in docs['BING']:
        dork=yml_dork['dorks']['dork']
        domain="mapfre.es"
        limit=7
        aux_links=search(domain,dork,limit)
        links['dominio']=domain
        links['riesgo']=yml_dork['dorks']['riesgo']
        links['dork']=dork
        links['resultados']=aux_links
        myfile.write("%s\n" % links + '\n')
    myfile.close()