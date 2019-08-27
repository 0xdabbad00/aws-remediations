from typing import Any, Dict

from . import Remediation
from .exceptions import InvalidInput


def lambda_handler(event: Dict[str, Any], unused_context: Any) -> Dict[Any, Any]:
    """Main lambda handler use as the entry point for the application

    Args:
        event: Event object that contains the invocation payload. There are two type of events
        currently supported:
        1. 'listRemediations' event: The Lambda will return the available remediations
        and the parameters used by the remediation.
        2. 'remediate' event: The Lambda invokes the appropriate remediation.

        unused_context: AWS LambdaContext object

    Examples:
        {
          "action": "remediate",
          "payload": {
            "remediationId": "AWS-S3BucketLogging",
            "resource":
              {
                "Name": "my-bucket",
                "AccountId": "123456789012",
                "Region": "us-west-2",
              }
            ,
            "parameters": {
              "TargetBucket": "log-bucket",
              "TargetPrefix": "s3-access"
            }
          }
        }



        {
          "action": "listRemediations"
        }
    """
    if 'action' not in event:
        raise InvalidInput('Input missing "action" parameter')
    if event['action'] == 'listRemediations':
        return Remediation.get_all_remediations()
    if event['action'] == 'remediate':
        Remediation.get(event['payload']['remediationId'])().fix(event['payload'])
        return {}
    raise InvalidInput('Unknown action "{}"'.format(event['action']))
