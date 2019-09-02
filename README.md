# AWS Remediations

[![CircleCI](https://circleci.com/gh/panther-labs/aws-remediations.svg?style=svg)](https://circleci.com/gh/panther-labs/aws-remediations)

AWS Serverless Application to instantly remediate common security issues in your accounts. This application provides an event-driven framework for fixing any type of misconfiguration in an account.

![Architecture](docs/AutoRemediate.png)

The full list of available remediations can be found in the [project directory](src/remediations).

Examples include:
- Enable VPC Flow Logs to S3
- Encrypt DynamoDB Tables
- Enable S3 Bucket Encryption
- Enable KMS Key Rotation
- Create Missing CloudTrails

## Deployment

### Serverless Application Repository

This application can easily be installed from the AWS Serverless Application Repository (SAR).

1. Navigate to the [aws-remediations](https://console.aws.amazon.com/lambda/home?region=us-east-1#/create/app?applicationId=arn:aws:serverlessrepo:us-east-1:349240696275:applications/aws-remediations) application page in the AWS Console
1. Scroll down and fill out the application settings on the right side
1. Check box acknowledging that 'this app creates custom IAM roles'
1. Click Deploy, which will create a new CloudFormation stack in the currently logged in region

Alternatively, this can be installed on the command line from this repo with:

```bash
$ make deploy-sar region=<region-name>
```

### Multiple Accounts

To remediate issues in multiple accounts, deploy the application in only one -master- account.
In the other accounts, only setup the IAM role that the Lambda will assume to remediate issues.

The following steps demonstrate this configuration:

1. In your master account, deploy the project from the SAR (above steps)

1. For the satellite accounts, use the following deployment parameters (either in the template or in the Console):

```yaml
PantherAWSRemediations:
  Type: AWS::Serverless::Application
  Properties:
    Location:
      ApplicationId: arn:aws:serverlessrepo:us-east-1:349240696275:applications/aws-remediations
      SemanticVersion: 0.1.0
    Parameters:
      IsMasterAccount: 'false'
      CreateSSMDocument: 'false'
      MasterAccountId: '123456789012'
      LambdaLoggingLevel: 'INFO'
      LambdaLogsRetentionDays: 365
```

Where `MasterAccountId` is the Account Id of the account where the Lambda is deployed.

### Source
To build and deploy the application from source, we recommend using the [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-reference.html#serverless-sam-cli).

1.  Install the AWS CLI, Docker and SAM CLI using the following [instructions](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html).

1. Build the project:

```bash
$ make setup
```

1. Deploy the project in your account. You will need to specify an S3 bucket in your account, where the source code will be uploaded prior to deploying:

```bash
$ make deploy-master bucket=<your-bucket>
```

## Usage

Remediation can be triggered by invoking the `aws-remediate` function with the following input:

```json
{
  "action": "remediate",
  "payload": {
    "remediationId": "AWS.S3.EnableBucketLogging",
    "resource": {
        "Name": "my-bucket",
        "AccountId": "123456789012",
        "Region": "us-west-2"
    },
    "parameters": {
      "TargetBucket": "my-bucket",
      "TargetPrefix": "my-prefix"
    }
  }
}
```

Field | Description
--- | ---
*action* | The action to be performed by the application. It should always be set to `remediate`
*payload.remediationId* | The unique identifier of the remediation that you want to trigger
*payload.resource* | A JSON describing the resource you want to remediate. It needs to have `Region` and `AccountId` fields
*payload.parameters* | A JSON with the additional parameters needed for the remediation

You can also invoke the Lambda using AWS CLI. The following command enables log file validation for an existing CloudTrail trail.

```bash
$ aws lambda invoke --function-name aws-remediation \
                    --payload '{"action":"remediate","payload":{"remediationId":"AWS.CloudTrail.EnableLogValidation","resource":{"AccountId":"123456789012","Region":"us-west-2","Name":"test-bucket"},"parameters":{}}' \
                    output.log
```

### Using AWS Systems Manager (AWS SSM)
The CloudFormation template creates additionally a [SSM Automation Document](https://docs.aws.amazon.com/systems-manager/latest/userguide/automation-documents.html) that can be used to remediate resources using AWS SSM.

## Contributing

Please read the `CONTRIBUTING.md` before submitting pull requests.

### Building

The project requires Python 3.7+.
Build the project locally by running the following command:

```bash
$ make setup install
```

This will setup your Python virtual environment and install dependencies.

### Testing

To run the test suite, including linting and formatting:

```bash
$ make ci
```
