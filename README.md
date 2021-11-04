# AWS CLOUDFORMATION API GATEWAY MIDWAY AUTHORISER CONFIG RULE

This repo contains an AWS Config rule that enforces cloud infrastructure best practices for any AWS internal deployment of an API Gateway, for Application Security approval purposes.  The associated code repository contains the following:

1.  This README.
    <br>
2.  The source code for two lambda functions. One lambda to check whether a newly deployed CloudFormation template conforms to our AWS Config rule - whether or not the APIs in a given account have a Midway authoriser associated with its resources, and another lambda to remediate the aforementioned non-conformity. Whenever a particular cloud resource (i.e. API Gateway) is non-compliant, it will change the configuration of the CloudFormatin template so that it becomes it compliant. The `remediate_midway_authorizer.py` lamba is an example of an automatic remediation, not a manual one. One folder contains the original python files for the lambdas, the other contains the zipped versions that one should copy over to their chosen S3 bucket (i.e. `<s3-bucket-here>`).
    <br>
3.  A CloudFormation template to create the above lambdas, along with the associated SSM automation document, AWS Config rule, IAM roles and policies.

## Deployment Steps

1. Upload the entire 'Lambdas' Folder into an S3 bucket - which will give you URIs in the format s3://bucket-name/Lambdas/codefile.py.zip - and use this bucket name for each S3 parameter.
   <br>
2. Create a single stack from the CloudFormation template in the CloudFormation folder.
   **[CLI COMMANDS BELOW]**

## Demo Prerequisites

- An AWS account.
- An S3 bucket exists in your AWS account with the same name as `<s3-bucket-here>` (see below).
- An account with one or more APIs residing in API Gateway.
- An instantiated Cognito User Pool configured with Midway specific credentials. Make note of the Cognito User Pool ARN, as this will be passed in as a CloudFormation parameter to the `config_rule_cfn_midway_authorizer.yml` CloudFormation file at deployment time. 


## Deployment CLI Commands

**Upload Lambdas to S3**

> aws s3 cp Lambdas/ s3://<s3-bucket-here>/Lambdas/ --recursive

**CloudFormation Termination Protection Remediation**

> aws cloudformation create-stack --stack-name cfn-midway-authoriser-remediation --template-body file://CloudFormation/config_rule_cfn_midway_authorizer.yml --parameters ParameterKey=S3BucketName,ParameterValue=`<S3_BUCKET_NAME>` ParameterKey=ProviderARNValue, ParameterValue=`<COGNITO_USER_POOL_ARN>` --capabilities CAPABILITY_NAMED_IAM --enable-termination-protection# cfn-midway-authoriser
