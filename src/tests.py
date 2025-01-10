from lscsde_workspace_mgmt.models import AnalyticsApproval
from .datasource.validator import DataSourceValidator, DataSourceValidationException, AnalyticsDataSource
import asyncio
import pytest

class TestValidation:
    def mock_data_source(self) -> AnalyticsDataSource:
        body = AnalyticsDataSource()       
        body.metadata.name = "test"
        body.metadata.namespace = "test-namespace"
        return body
    
    def mock_data_source_with_valid_approvals(self) -> AnalyticsDataSource:
        body = self.mock_data_source()
        body.spec.approvals = [
            AnalyticsApproval(type = "information_governance", email = "john@some.org"),
            AnalyticsApproval(type = "data_engineer", email = "jane@some.org")
        ]
        return body
    


    @pytest.mark.asyncio
    async def test_validate_empty_object(self):
        body = self.mock_data_source()
        with pytest.raises(DataSourceValidationException) as ex:
            validator = DataSourceValidator(None, None, "test-namespace")
            await validator.validate(body)
        assert "AWAITING_APPROVAL" == ex.value.status_code

    @pytest.mark.asyncio
    async def test_valid_approvals_no_connections(self):
        body = self.mock_data_source_with_valid_approvals()
        with pytest.raises(DataSourceValidationException) as ex:
            validator = DataSourceValidator(None, None, "test-namespace")
            await validator.validate(body)
        assert "NO_CONNECTIONS" == ex.value.status_code

    @pytest.mark.asyncio
    async def test_missing_approvals(self):
        body = self.mock_data_source()
        body.spec.approvals = [
            AnalyticsApproval(type = "information_governance", email = "john@some.org"),
        ]
        with pytest.raises(DataSourceValidationException) as ex:
            validator = DataSourceValidator(None, None, "test-namespace")
            await validator.validate(body)
        assert "MISSING_APPROVALS" == ex.value.status_code

    @pytest.mark.asyncio
    async def test_dupe_approvals(self):
        body = self.mock_data_source()
        body.spec.approvals = [
            AnalyticsApproval(type = "information_governance", email = "john@some.org"),
            AnalyticsApproval(type = "data_engineer", email = "john@some.org"),
        ]
        with pytest.raises(DataSourceValidationException) as ex:
            validator = DataSourceValidator(None, None, "test-namespace")
            await validator.validate(body)
        assert "DUPLICATE_APPROVER" == ex.value.status_code
