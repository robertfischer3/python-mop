from mop.framework.mopbase import MopBase
from mop.framework.prisma_cloud_connections import request_authenticated_prisma_session


class Compliance(MopBase):

    def list(self, cloud_api):
        api_endpoint = self.config['PRISMACLOUD']['compliance']
        api_endpoint = api_endpoint.format(cloud_api=cloud_api)
        with request_authenticated_prisma_session() as req:
            response = req.get(api_endpoint)

        if response.status_code in range(200, 299):
            return response
