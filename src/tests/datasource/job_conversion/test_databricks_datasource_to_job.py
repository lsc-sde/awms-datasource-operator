from lscsde_workspace_mgmt.models import AnalyticsDataSourceSecret
from ....datasource.validator import DataSourceValidator
from ....datasource.converters.jobconverter import JobConverter
from ..mocker import mock_datasource_with_databricks_connection_with_service_principle as mock_datasource
import pytest

class TestValidation:
    @pytest.mark.asyncio
    async def test_databricks_datasource_to_job(self):
        body = mock_datasource()
        validator = DataSourceValidator(None, None, "test-namespace")
        await validator.validate(body)
        converter = JobConverter()
        
        # override the image name to ensure consistency no matter what environment variables are set
        converter.databricks.image = "test:5000/xfer-databricks:latest" 

        jobs = converter.convert(body)
        assert 1 == len(jobs)
        job = jobs[0]
        assert body.metadata.namespace == job.metadata.namespace
        assert None != job.spec
        assert None != job.spec.template
        assert None != job.spec.template.spec
        assert None != job.spec.template.spec.containers
        assert 1 == len(job.spec.template.spec.containers)
        
        container = job.spec.template.spec.containers[0]
        assert "dataxfer" == container.name
        assert "test:5000/xfer-databricks:latest" == container.image
        
