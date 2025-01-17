from ...datasource.validator import DataSourceValidator, DataSourceValidationException, AnalyticsDataSource
from lscsde_workspace_mgmt.models import AnalyticsApproval
from .mocker import mock_data_source as mock_datasource
import pytest

class TestValidation:
    @pytest.mark.asyncio
    async def test_dupe_approvals(self):
        body = mock_datasource()
        body.spec.approvals = [
            AnalyticsApproval(type = "information_governance", email = "john@some.org"),
            AnalyticsApproval(type = "data_engineer", email = "john@some.org"),
        ]
        with pytest.raises(DataSourceValidationException) as ex:
            validator = DataSourceValidator(None, None, "test-namespace")
            await validator.validate(body)
        assert "DUPLICATE_APPROVER" == ex.value.status_code
