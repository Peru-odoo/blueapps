import json
from odoo.http import JsonRequest, Response
from odoo.tools import date_utils

def _json_response(self, result=None, error=None):
    if isinstance(result, Response):
        return result
    response = {
        'jsonrpc': '2.0',
        'id': self.jsonrequest.get('id')
    }
    if error is not None:
        response['error'] = error
    if result is not None:
        response['result'] = result

    mime = 'application/json'
    body = json.dumps(response, default=date_utils.json_default)
    return Response(
        body, status=error and error.pop('http_status', 200) or 200,
        headers=[('Content-Type', mime), ('Content-Length', len(body))]
    )


def __init__(self, *args):
    super(JsonRequest, self).__init__(*args)
    self.params = {}

    args = self.httprequest.args
    request = None
    request_id = args.get('id')

    # regular jsonrpc2
    request = self.httprequest.get_data().decode(self.httprequest.charset)

    # Read POST content or POST Form Data named "request"
    try:
        self.jsonrequest = json.loads(request)
    except ValueError:
        self.jsonrequest = {}

    self.params = dict(self.jsonrequest.get("params", {}))
    self.context = self.params.pop('context', dict(self.session.context))


JsonRequest.__init__ = __init__
JsonRequest._json_response = _json_response
