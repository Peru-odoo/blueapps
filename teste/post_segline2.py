import requests
# import json
# import jsonpickle
# import io
# import pickle
import xml.dom.minidom

try:
    to_unicode = unicode
except NameError:
    to_unicode = str

url = "http://162.214.190.43/~buscador/ws2/rFucador.php?u=vendaseirele&s=k13997&k=2053&tipo=CONSULTANB&doc=5162815965"
payload = {}
headers = {}


def buscar_dados():
    response = requests.request("GET", url, headers=headers, data=payload)
    todos = response.text
    doc = xml.dom.minidom.parse(todos);
    # dados = response.json()
    # todos = json.loads(response.content)
    #    print(todos)
    # print(doc)
    print(doc.nodeName)
    print(doc.firstChild.tagName)
if url:
    buscar_dados()
