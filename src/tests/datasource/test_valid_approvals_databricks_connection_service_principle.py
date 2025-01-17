from lscsde_workspace_mgmt.models import AnalyticsDataSourceSecret
from ...datasource.validator import DataSourceValidator, DataSourceValidationException, AnalyticsDataSource
from .mocker import mock_datasource_with_databricks_connection_with_service_principle as mock_datasource
import pytest

class TestValidation:
    @pytest.mark.asyncio
    async def test_valid_approvals_databricks_connection_service_principle(self):
        body = mock_datasource()
        validator = DataSourceValidator(None, None, "test-namespace")
        await validator.validate(body)
