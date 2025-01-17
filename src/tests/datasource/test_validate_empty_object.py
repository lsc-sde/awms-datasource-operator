from ...datasource.validator import DataSourceValidator, DataSourceValidationException, AnalyticsDataSource
from .mocker import mock_data_source as mock_datasource
import pytest

class TestValidation:
    @pytest.mark.asyncio
    async def test_validate_empty_object(self):
        body = mock_datasource()
        with pytest.raises(DataSourceValidationException) as ex:
            validator = DataSourceValidator(None, None, "test-namespace")
            await validator.validate(body)
        assert "AWAITING_APPROVAL" == ex.value.status_code