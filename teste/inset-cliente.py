import xmlrpc.client

db = "erp_blue6"
login = "diego@blueconnect.com.br"
password = "**Blu3connect**"
url = "http://www.blueconnect.com.br:8069"

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
version = common.version()
print("detalhes...", version)

uid = common.authenticate(db, login, password, {})
print("UID", uid)

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

#Listar parceiros apenas parceiros do tipo, empresa como verdadeiro
parceiros = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['is_company', '=', True]]])
print("Parceiros...", parceiros)

#Mostrar total de registros no modelo
total_parceiros = models.execute_kw(db, uid, password, 'res.partner', 'search_count', [[]])
print("Parceiros...", total_parceiros)

####
ids = models.execute_kw(db, uid, password,'res.partner', 'search',[[['is_company', '=', True]]],{'limit': 1})

[record] = models.execute_kw(db, uid, password, 'res.partner', 'read', [ids])
# conte o número de campos buscados por padrão
len(record)

#id = models.execute_kw(db, uid, password, 'res.partner', 'create')


# Referencias: https://www.odoo.com/documentation/14.0/developer/misc/api/odoo.html
