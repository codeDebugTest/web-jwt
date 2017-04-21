# coding=utf-8
import logging
from authorization import Authorization

logger = logging.getLogger()


class AdminUser(object):
    def __init__(self, user_id, user_name, password):
        self.user_id = user_id
        self.user_name = user_name
        self.password = password

    def to_json(self):
        return {
            'user_name': self.user_name
        }


class UserProcess(object):
    users = [
        AdminUser('000001', 'super_admin', '123456'),
        AdminUser('000002', 'ias_admin', 'ias_group123456')
    ]
    user_map = {user.user_name: user for user in users}

    @classmethod
    def login(cls, content):
        account_name = content.get('account_name', None)
        password = content.get('password', None)

        user = UserProcess.user_map.get(account_name, None)
        if not user or user.password != password:
            return {'message': '账户或密码不正确！'}

        return {
            'message': 'success',
            'super': '1' if account_name == 'ias_admin' else '0',
            'access_token': Authorization.generate_access_token(user.user_id),
            'refresh_token': Authorization.generate_refresh_token(user.user_name)
        }

    @classmethod
    def refresh_token(cls, content):
        token = content.get('token', None)
        result, msg = Authorization.verify_refresh_token(token)
        if result:
            user = UserProcess.user_map.get(msg, None)
            if user:
                token = Authorization.generate_access_token(user.user_id)
                return {'access_token': token}
        return None

    @classmethod
    def get_all_users(cls):
        result = []
        for usr in cls.users:
            result.append(usr.to_json())
        return result