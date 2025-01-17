from ...datasource.validator import DataSourceValidator, DataSourceValidationException, AnalyticsDataSource
from .mocker import mock_data_source_with_valid_approvals as mock_datasource
import pytest

class TestValidation:
    @pytest.mark.asyncio
    async def test_valid_approvals_no_connections(self):
        body = mock_datasource()
        with pytest.raises(DataSourceValidationException) as ex:
            validator = DataSourceValidator(None, None, "test-namespace")
            await validator.validate(body)
        assert "NO_CONNECTIONS" == ex.value.status_code
