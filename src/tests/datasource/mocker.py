from lscsde_workspace_mgmt.models import (
    AnalyticsDataSource,
    AnalyticsApproval, 
    AnalyticsDataSourceConnection, 
    AnalyticsDataSourceDataBricksConnection,
    AnalyticsDataSourceSecret
)

def mock_data_source() -> AnalyticsDataSource:
    body = AnalyticsDataSource()       
    body.metadata.name = "test"
    body.metadata.namespace = "test-namespace"
    return body

def mock_data_source_with_valid_approvals() -> AnalyticsDataSource:
    body = mock_data_source()
    body.spec.approvals = [
        AnalyticsApproval(type = "information_governance", email = "john@some.org"),
        AnalyticsApproval(type = "data_engineer", email = "jane@some.org")
    ]
    return body

def mock_data_source_with_empty_databricks_connection() -> AnalyticsDataSource:
    body = mock_data_source_with_valid_approvals()
    body.spec.connections = [
        AnalyticsDataSourceConnection(type = "databricks")
    ]
    return body

def mock_datasource_with_databricks_connection_but_no_secret() -> AnalyticsDataSource:
    body = mock_data_source_with_empty_databricks_connection()
    body.spec.connections[0].databricks_connection = AnalyticsDataSourceDataBricksConnection(
        hostName = "127.0.0.1",
        httpPath = "/test"
    )
    return body

def mock_datasource_with_databricks_connection_with_service_principle() -> AnalyticsDataSource:
    body = mock_datasource_with_databricks_connection_but_no_secret()
    body.spec.connections[0].databricks_connection.service_principle = AnalyticsDataSourceSecret(
            secretName = "test-secret"
        )
    return body