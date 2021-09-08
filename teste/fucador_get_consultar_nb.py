import requests
import untangle
import xmltodict
# import xml.etree.ElementTree as ET
from xml.etree import ElementTree
from datetime import date, datetime

url = "http://fucador.com/ws2/rFucador.php?u=vendaseirele&s=k13997&k=7173&tipo=CONSULTANB&doc=5162815965"

def buscar_dados():
    # response = requests.request("GET", url, headers=headers, data=payload)
    r = requests.get(url)
    dict_data = xmltodict.parse(r.content)
    dadoscadastrais = dict_data['consultaws']
    ['dados_cadastrais']
    rubricas = dict_data['consultaws']['rubrica']
    # print(rubricas)
    for x in rubricas:
        print("Código:", x['codigo'], "-", x['desrub'], "Valor:", x['sinal'], x['vlrub'])
    #    print(type(x))
    # print(contatos['consultaws']['dados_cadastrais']['beneficio'])
    # print(contatos.get('dados_cadastrais','Erro'))
    # info = info.infCons
    # tree = ElementTree.fromstring(r.content)
    # print(tree)
    # print(dict_data)
    # for child in root.iter('*'):
    #    print(child.tag)
    # print(r.content)
    # todos = response.text
    # doc = xml.dom.minidom.parse(todos);
    # mydoc = minidom.parse(todos)
    # items = mydoc.getElementsByTagName('dados_cadastrais')
    # dados = response.json()
    # todos = json.loads(response.content)
    #    print(todos)
    # print(doc)
    # print(doc.nodeName)
    # print(doc.firstChild.tagName)
    # one specific item attribute
    # print('Item #2 attribute:')
    # print(items[1].attributes['name'].value)
if url:
    buscar_dados()
