from ...datasource.validator import DataSourceValidator, DataSourceValidationException, AnalyticsDataSource
from .mocker import mock_data_source_with_empty_databricks_connection as mock_datasource
import pytest

class TestValidation:
    @pytest.mark.asyncio
    async def test_valid_approvals_empty_databricks_connection(self):
        body = mock_datasource()
        with pytest.raises(DataSourceValidationException) as ex:
            validator = DataSourceValidator(None, None, "test-namespace")
            await validator.validate(body)
        assert "INVALID_DATABRICKS_CONNECTION" == ex.value.status_code
