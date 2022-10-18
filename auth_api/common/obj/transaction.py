from django.db import transaction

from common_modules.logger import logger


class Transaction:
    def __init__(self, response):
        self.response = response

    def __enter__(self):
        try:
            self.tid = transaction.savepoint()
        except Exception as e:
            logger.debug("回滚事物", e)
            transaction.savepoint_rollback(self.tid)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """"""
        if exc_tb:
            transaction.savepoint_rollback(self.tid)
            logger.debug("回滚事务", str(exc_type(exc_val)))
            raise exc_type(exc_val)
        transaction.savepoint_commit(self.tid)
        return self.response
