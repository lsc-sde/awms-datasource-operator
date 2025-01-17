from lscsde_workspace_mgmt.models import AnalyticsDataSourceSecret
from ...datasource.validator import DataSourceValidator, DataSourceValidationException, AnalyticsDataSource
from .mocker import mock_datasource_with_databricks_connection_but_no_secret as mock_datasource
import pytest

class TestValidation:
    @pytest.mark.asyncio
    async def test_valid_approvals_databricks_connection_service_principle_no_secret(self):
        body = mock_datasource()
        body.spec.connections[0].databricks_connection.service_principle = AnalyticsDataSourceSecret()
        with pytest.raises(DataSourceValidationException) as ex:
            validator = DataSourceValidator(None, None, "test-namespace")
            await validator.validate(body)
        assert "MISSING_SERVICE_PRINCIPLE_SECRET_NAME" == ex.value.status_code
