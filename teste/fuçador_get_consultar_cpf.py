import requests
import untangle
import xmltodict
# import xml.etree.ElementTree as ET
from xml.etree import ElementTree
from datetime import date, datetime

url = "http://fucador.com/ws2/rFucador.php?u=vendaseirele&s=k13997&k=7173&tipo=CONSULTACPF&doc=16685717572"
payload = {}
headers = {}


def buscar_dados():
    # response = requests.request("GET", url, headers=headers, data=payload)
    r = requests.get(url)
    dict_data = xmltodict.parse(r.content)
    # contatos = dict(dict_data) # Ocorreu tudo bem
    contatos = dict_data['consulta']['dadosPessoais']
    #print(contatos)
    for x in contatos:
        print(x.value())
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
