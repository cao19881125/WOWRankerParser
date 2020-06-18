import os
import sys
import json

PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
from webob import Request
from webob import Response

class RestApiHandler(object):

    def __call__(self, environ,start_response):
        start_response("200 OK", [("Content-type", "text/plain")])
        req = Request(environ)
        res = Response()
        res.headers['Content-Type'] = 'application/json;charset=utf-8'
        res.headers['Access-Control-Allow-Origin'] = '*'
        params = self._get_params(req)
        if req.method == 'GET':
            self._get(req,res)
        elif req.method == 'POST':
            if params.has_key('_method') and params['_method'] == 'PUT':
                self._put(req, res)
            elif params.has_key('_method') and params['_method'] == 'DELETE':
                self._delete(req, res)
            else:
                self._post(req,res)
        elif req.method == 'PUT':
            self._put(req,res)
        elif req.method == 'DELETE':
            self._delete(req,res)
        return res(environ, start_response)

    def _get(self,request,response):
        return response

    def _post(self,request,response):
        return response

    def _put(self,request,response):
        return response

    def _delete(self,request,response):
        return response

    def _get_params(self,request):
        parms = {}
        for key,value in request.params.items():
            if type(key) == unicode:
                key = unicode.encode(key)
            if type(value) == unicode:
                value = unicode.encode(value)
            parms[key] = value
        return parms



