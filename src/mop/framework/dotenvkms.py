import os
from mop.framework.kmsbase import KMSBase


class DotEnvKMS(KMSBase):
    def __init__(self):
        super().__init__()
        self.load()

    def load(self):
        if 'PRISMA_USERNAME' in os.environ and 'PRISMA_PASSWORD' in os.environ:
            prisma_username = os.environ['PRISMA_USERNAME']
            prisma_password = os.environ['PRISMA_PASSWORD']
            prisma_customerName = os.environ['PRISMA_CUSTOMERNAME']

            self.credentials['prisma_username'] = prisma_username
            self.credentials['prisma_password'] = prisma_password
            self.credentials['prisma_customerName'] = prisma_customerName
        else:
            raise KeyError
