from .databricks import DatabricksJobConverter
from lscsde_workspace_mgmt.models import (
    AnalyticsDataSource,
    AnalyticsDataSourceConnection,
    AnalyticsDataSourceDataBricksConnection
)
from kubernetes_asyncio.client.models import V1Job

class JobConverter:
    def __init__(self):
        self.databricks = DatabricksJobConverter()
    
    def convert(self, body : AnalyticsDataSource) -> list[V1Job]:
        results = []
        for connection in body.spec.connections:
            if connection.type.casefold() == "databricks" and connection.databricks_connection != None:
                results.append(
                    self.databricks.convert(
                        namespace = body.metadata.namespace, 
                        name = body.metadata.name, 
                        connection = connection.databricks_connection
                    )
                )
        return results