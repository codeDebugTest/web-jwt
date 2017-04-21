# coding=utf-8
import json
import logging.config
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
import time
import traceback
from gevent.wsgi import WSGIServer
from flask import Flask, make_response, request
from flask_restful import Resource, Api, reqparse, abort
from flask_cors import CORS
from flask_compress import Compress
from processors import ApiProcessor
from authorization import AuthResource


app = Flask(__name__)
api = Api(app)
CORS(app)
Compress(app)

logger = logging.getLogger()
api_processor = ApiProcessor(logger)


class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('account_name')
        parser.add_argument('password')
        args = parser.parse_args()
        account_name = args['account_name']
        password = args['password']
        t = time.time()
        response = api_processor.process(
            content={'account_name': account_name, 'password': password}, correlation_id='sumscope_login')

        logger.info('sumscope login')
        logger.info('account_name: {}, password: {}'.format(account_name, password))
        logger.info('cost time: {}'.format(time.time() - t))
        if response:
            try:
                resp = make_response(json.dumps(response))
                resp.headers['Content-Type'] = 'application/json'
                return resp
            except:
                pass
        abort(404, message="login failed.")


class RefreshToken(Resource):
    def post(self):
        token = request.headers.get('Authorization', None)
        response = api_processor.process(content={'token': token}, correlation_id='refresh_token')
        if response is not None:
            try:
                resp = make_response(json.dumps(response))
                resp.headers['Content-Tpye'] = 'application/json'
                return resp
            except:
                pass

        abort(404, message= 'invalid request')


class CompanyList(AuthResource):
    def get(self):
        t = time.time()
        response = api_processor.process(correlation_id='company_users')

        print 'get cost time: {}'.format(time.time() - t)
        if response is not None:
            try:
                resp = make_response(json.dumps(response))
                resp.headers['Content-Type'] = 'application/json'
                return resp
            except:
                pass
        abort(404, message="fetch company user list failed.")


api.add_resource(Login, '/login')
api.add_resource(RefreshToken, '/refresh_token')
api.add_resource(CompanyList, '/companies')

if __name__ == '__main__':
    try:
        # gevent wsgi
        http_server = WSGIServer(('', 5000), app)
        http_server.serve_forever()
    except:
        logger.error(traceback.format_exc())
