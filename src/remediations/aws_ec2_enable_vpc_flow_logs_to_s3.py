from typing import Any, Dict

from boto3 import Session

from app import Remediation
from app.remediation_base import RemediationBase


@Remediation
class AwsEc2EnableVpcFlowLogsToS3(RemediationBase):
    """Remediation that enables VPC Flow logs to S3 bucket"""

    @classmethod
    def _id(cls) -> str:
        return 'EC2.EnableVpcFlowLogsToS3'

    @classmethod
    def _parameters(cls) -> Dict[str, str]:
        return {'TargetBucketName': '', 'TargetPrefix': '', 'TrafficType': 'ALL'}

    @classmethod
    def _fix(cls, session: Session, resource: Dict[str, Any], parameters: Dict[str, str]) -> None:
        response = session.client('ec2').create_flow_logs(
            ResourceIds=[
                resource['Id'],
            ],
            ResourceType='VPC',
            TrafficType=parameters['TrafficType'],
            LogDestinationType='s3',
            LogDestination='arn:aws:s3:::{}/{}'.format(
                parameters['TargetBucketName'], parameters['TargetPrefix']
            )
        )
        if 'Unsuccessful' in response:
            raise Exception(response['Unsuccessful'][0])
