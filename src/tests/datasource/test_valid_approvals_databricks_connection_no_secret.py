from ...datasource.validator import DataSourceValidator, DataSourceValidationException, AnalyticsDataSource
from .mocker import mock_datasource_with_databricks_connection_but_no_secret as mock_datasource
import pytest

class TestValidation:
    @pytest.mark.asyncio
    async def test_valid_approvals_databricks_connection_no_secret(self):
        body = mock_datasource()
        with pytest.raises(DataSourceValidationException) as ex:
            validator = DataSourceValidator(None, None, "test-namespace")
            await validator.validate(body)
        assert "MISSING_DATABRICKS_AUTH" == ex.value.status_code
    