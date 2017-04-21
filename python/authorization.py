import jwt
import datetime
import logging
from common.config import JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXP_SECONDS, JWT_ALGORITHM, JWT_REFRESH_TOKEN_EXP_SECONDS
from flask_restful import abort
from flask import request
from functools import wraps
from flask_restful import Resource

logger = logging.getLogger()


class Authorization(object):
    @staticmethod
    def generate_access_token(user_id):
        access_token = jwt.encode({
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_ACCESS_TOKEN_EXP_SECONDS),
            'iat': datetime.datetime.utcnow(),
            'user_id': user_id
        }, algorithm=JWT_ALGORITHM, key=JWT_SECRET_KEY)
        return access_token

    @staticmethod
    def verify_access_token(token):
        try:
            play_load = jwt.decode(token, key=JWT_SECRET_KEY)
            return True, play_load['user_id']
        except jwt.ExpiredSignatureError:
            logger.warn('verified access token failed for expired token')
            return False, 'expired token'
        except jwt.InvalidTokenError:
            logger.warn('verified access token failed for invalid token')
            return False, 'invalid token'

    @staticmethod
    def generate_refresh_token(account_name):
        refresh_token = jwt.encode({
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_REFRESH_TOKEN_EXP_SECONDS),
            'iat': datetime.datetime.utcnow(),
            'account_name': account_name
        }, algorithm=JWT_ALGORITHM, key=JWT_SECRET_KEY)
        return refresh_token

    @staticmethod
    def verify_refresh_token(token):
        logger.info('verifying refresh token')
        try:
            play_load = jwt.decode(token, key=JWT_SECRET_KEY)
            account_name = play_load['account_name']
            return True, account_name
        except jwt.ExpiredSignatureError:
            logger.warn('verified refresh token failed for expired token')
            return False, 'expired token'
        except jwt.InvalidTokenError:
            logger.warn('verified refresh token for invalid token')
            return False, 'invalid token'


def authenticate_access_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not getattr(func, 'authenticated', True):
            return func(*args, **kwargs)
        token = request.headers.get('Authorization', None)
        result, msg = Authorization.verify_access_token(token)

        if result:
            return func(*args, **kwargs)

        abort(401, message=msg)
    return wrapper


class AuthResource(Resource):
    method_decorators = [authenticate_access_token]

