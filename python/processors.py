# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from user import UserProcess


class ApiProcessor(object):
    def __init__(self, logger):
        self.logger = logger
        self.methods = {
            # user process
            'sumscope_login': self.method_sumscope_login,
            'refresh_token': self.method_refresh_token,
            'company_users': self.method_all_user,
        }

    def process(self, content=None, correlation_id=None):
        if correlation_id in self.methods:
            method = self.methods.get(correlation_id)
            return method(content)
        else:
            self.logger.warning('No such service: {}'.format(correlation_id))
            return None

    def method_sumscope_login(self, content):
        self.logger.info('message requesting for login admin server')
        self.logger.info('content: {}'.format(content))
        return UserProcess.login(content)

    def method_refresh_token(self, content):
        self.logger.info('message requesting to refresh user token')
        return UserProcess.refresh_token(content)

    def method_all_user(self, content):
        self.logger.info('message requesting to get company users')
        return UserProcess.get_all_users()
