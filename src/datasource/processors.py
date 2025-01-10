import os 
import logging
from lscsde_workspace_mgmt.models import (
    AnalyticsDataSource
)
from lscsde_workspace_mgmt.datasourceclient import AnalyticsDataSourceClient

from pydantic import TypeAdapter
from uuid import uuid5, NAMESPACE_URL
from urllib.parse import urlparse
from kubernetes_asyncio.client import CoreV1Api, ApiException
from base64 import b64decode
from sys import stdout
from .loggers import setup_logger
from .validator import DataSourceValidator, DataSourceValidationException

class DataSourceProcessor:
    def __init__(self, core_api : CoreV1Api, ads_client : AnalyticsDataSourceClient):
        self.core_api = core_api 
        self.ads_client = ads_client
        self.namespace = os.getenv("NAMESPACE")
        self.log = setup_logger("DataSourceProcessor")

    async def update_status(self, body : AnalyticsDataSource, status_code):
        if body.status.status_text != status_code:
            self.log.info(f"{body.metadata.name} in {body.metadata.namespace} is currently {body.status.status_text} not {status_code}, updating.")
            body.status.status_text = status_code
            await self.ads_client.patch_status(body.metadata.namespace, body.metadata.name, body.status)

    async def process(self, body):
        adaptor = TypeAdapter(AnalyticsDataSource)
        datasource_resource : AnalyticsDataSource = adaptor.validate_python(body)
        self.log.info(f"Crate {datasource_resource.metadata.name} on {datasource_resource.metadata.namespace} has been updated")
        validator = DataSourceValidator(self.core_api, self.ads_client, self.namespace)
        try:
            await validator.validate(datasource_resource)
            status_code = "APPROVED"
            await self.update_status(body = datasource_resource, status_code = status_code)

        except DataSourceValidationException as ex:
            self.log.error(f"{datasource_resource.metadata.name} in {datasource_resource.metadata.namespace} has returned {ex.status_code}: {ex.message}")
            await self.update_status(body = datasource_resource, status_code = ex.status_code)
            
        