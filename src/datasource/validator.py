from kubernetes_asyncio.client import CoreV1Api, ApiException
from lscsde_workspace_mgmt.datasourceclient import AnalyticsDataSourceClient
from lscsde_workspace_mgmt.models import AnalyticsDataSource
from .loggers import setup_logger
from os import getenv
from pydantic import TypeAdapter

class DataSourceValidationException(Exception):
    def __init__(self, status_code, message):     
        super().__init__(message)
        self.status_code = status_code
        self.message = message

class DataSourceValidator:
    def __init__(self, core_api : CoreV1Api, ads_client : AnalyticsDataSourceClient, namespace : str):
        self.core_api = core_api 
        self.ads_client = ads_client
        self.namespace = namespace
        self.log = setup_logger("DataSourceValidator")
        self.check_duplicate_email = TypeAdapter(bool).validate_python(getenv("CHECK_DUPLICATE_EMAIL", "true"))
        self.expected_approvers = getenv("REQUIRED_APPROVAL_TYPES", "INFORMATION_GOVERNANCE,DATA_ENGINEER").split(",")

    async def validate_approvers(self, body : AnalyticsDataSource):
        if body.spec.approvals == None or len(body.spec.approvals) == 0:
            raise DataSourceValidationException("AWAITING_APPROVAL", "No approvals have currently been given")
        
        expected_approvers = self.expected_approvers
        approval_types = {}

        for approval in body.spec.approvals:
            if approval.type == None or approval.type == "":
                raise DataSourceValidationException("INVALID_APPROVAL", "Approver has no type")
            
            if approval.email == None or approval.email == "":
                raise DataSourceValidationException("INVALID_APPROVAL", "Approver has no email")
            
            # We need at least one of each type of approval by default
            approval_type = approval.type.casefold()
            if approval_type not in approval_types:
                approval_types[approval_type] = [ approval.email ]
            else:
                approval_types[approval_type].append(approval.email)

        for expected_approver in expected_approvers:
            if expected_approver.casefold() not in approval_types.keys():
                raise DataSourceValidationException("MISSING_APPROVALS", f"Awaiting approval from {expected_approver}")
        
        if self.check_duplicate_email == True:
            for expected_approver in expected_approvers:
                for approver in approval_types[expected_approver.casefold()]:
                    for other_expected_approver in expected_approvers:
                        if expected_approver.casefold() != other_expected_approver.casefold():
                            for other_approver in approval_types[other_expected_approver.casefold()]:
                                if approver.casefold() == other_approver.casefold():
                                    raise DataSourceValidationException("DUPLICATE_APPROVER", f"Approver {approver} is listed as both {expected_approver} and {other_expected_approver}")

    async def validate_connections(self, body : AnalyticsDataSource):
        if body.spec.connections == None or len(body.spec.connections) == 0:
            raise DataSourceValidationException("NO_CONNECTIONS", "The definition currently has no connections defined")
        
        for connection in body.spec.connections:
            if connection.type.casefold() == "databricks":
                databricks_connection = connection.databricks_connection
                if databricks_connection == None:
                    raise DataSourceValidationException("INVALID_DATABRICKS_CONNECTION", "if the type is set to databricks then databricksConnection must be populated.")
                
                if databricks_connection.personal_access_token == None and databricks_connection.oauth2_token == None and databricks_connection.service_principle == None:
                    raise DataSourceValidationException("MISSING_DATABRICKS_AUTH", "One of the fields personalAccessToken, oauth2Token or servicePrinciple must be populated")
                
                auth_type = ""

                if databricks_connection.personal_access_token != None:
                    if auth_type != "":
                        raise DataSourceValidationException("MULTIPLE_DATABRICKS_AUTHS", f"both {auth_type} and personal_access_token are defined but these are mutually exclusive")
                    auth_type = "personal_access_token"

                    raise DataSourceValidationException("DATABRICK_AUTH_NOT_IMPLEMENTED", f"{auth_type} is not implemented")

                    
                if databricks_connection.oauth2_token != None:
                    if auth_type != "":
                        raise DataSourceValidationException("MULTIPLE_DATABRICKS_AUTHS", f"both {auth_type} and oauth2_token are defined but these are mutually exclusive")
                    auth_type = "oauth2_token"

                    raise DataSourceValidationException("DATABRICK_AUTH_NOT_IMPLEMENTED", f"{auth_type} is not implemented")

                if databricks_connection.service_principle != None:
                    if auth_type != "":
                        raise DataSourceValidationException("MULTIPLE_DATABRICKS_AUTHS", f"both {auth_type} and service_principle are defined but these are mutually exclusive")
                    auth_type = "service_principle"
                    
                    if databricks_connection.service_principle.secret_name == None:
                        raise DataSourceValidationException("MISSING_SERVICE_PRINCIPLE_SECRET_NAME", f"secretName is not populated")

            else:
                raise DataSourceValidationException("UNRECOGNISED_CONNECTION_TYPE", f"The connection type '{connection.type.casefold()}' is not recognised")



    async def validate(self, body : AnalyticsDataSource):
        await self.validate_approvers(body)
        await self.validate_connections(body)
