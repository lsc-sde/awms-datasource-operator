from ..loggers import setup_logger
from lscsde_workspace_mgmt.models import AnalyticsDataSourceDataBricksConnection
from kubernetes_asyncio.client.models import (
    V1Job,
    V1JobSpec,
    V1PodSpec,
    V1PodTemplateSpec,
    V1Container,
    V1ObjectMeta,
    V1EnvVar,
    V1EnvVarSource,
    V1SecretKeySelector
)
from uuid import uuid4
from os import getenv

class DatabricksJobConverter:
    def __init__(self):
        self.image = getenv("DATABRICKS_XFER_IMG", "k3d-devcontainer-registry.local:5000/xfer-databricks:latest")

    def convert(self, namespace : str, name : str, connection : AnalyticsDataSourceDataBricksConnection):
        job = V1Job(
            metadata = V1ObjectMeta(
                name = f"job-{name}{uuid4().hex}",
                namespace = namespace
            ),
            spec = V1JobSpec(
                template = V1PodTemplateSpec(
                    spec = V1PodSpec(
                        containers = [
                            V1Container(
                                name = "dataxfer",
                                image = self.image,
                                env = [
                                    V1EnvVar(
                                        name = "SERVER_HOSTNAME",
                                        value = connection.host_name
                                    ),
                                    V1EnvVar(
                                        name = "SERVER_HTTPPATH",
                                        value = connection.http_path
                                    ),
                                    V1EnvVar(
                                        name = "CLIENT_ID",
                                        value_from = V1EnvVarSource(
                                            secret_key_ref = V1SecretKeySelector(
                                                name = connection.service_principle.secret_name,
                                                key = "CLIENTID"
                                            )
                                        )
                                    ),
                                    V1EnvVar(
                                        name = "CLIENT_SECRET",
                                        value_from = V1EnvVarSource(
                                            secret_key_ref = V1SecretKeySelector(
                                                name = connection.service_principle.secret_name,
                                                key = "CLIENTSECRET"
                                            )
                                        )
                                    )
                                ]
                            )
                        ]
                    )
                )
            )
        )
        return job
        