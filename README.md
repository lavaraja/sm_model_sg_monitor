# SageMaker Security Group Validation Lambda

This Lambda function checks for the existence of security groups used by Amazon SageMaker models and sends notifications via Amazon SNS in case of missing security groups.

## Overview

The `lambda_function.py` script contains the Python code for the Lambda function. It uses the Boto3 library to interact with the Amazon SageMaker and Amazon EC2 services to validate the existence of security groups and send SNS notifications.

## Prerequisites

Before using this Lambda function, ensure that you have:

- An AWS account with appropriate permissions to create and manage Lambda functions, Amazon SageMaker, and Amazon SNS.
- Installed the Boto3 library for Python.

# Permissions required for Lambda Role 

> Narrow down the permissions if you are looking to monitor only specific models.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Lambda_permissions",
            "Effect": "Allow",
            "Action": "ec2:DescribeSecurityGroups",
            "Resource": "*"
        },
        {
            "Sid": "Statement1",
            "Effect": "Allow",
            "Action": [
                "sagemaker:ListModels",
                "sagemaker:DescribeModel",
                "sns:Publish"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}
```

## Configuration

1. Replace `YOUR_SNS_TOPIC_ARN` with the actual ARN of your Amazon SNS topic in the `lambda_function.py` script. Also update the region to your AWS region.
2. Ensure that the Lambda function's execution role has the necessary permissions to publish messages to the specified SNS topic.

## Usage

1. Deploy the `lambda_function.py` script as a Lambda function in your AWS account.
2. Set up the necessary event triggers or schedule for the Lambda function to run at the desired intervals.
3. Monitor the SNS notifications for any missing security groups used by Amazon SageMaker models.

## Scheduling 

1. You can use AWS Event Bridge for scheduling this script to run using Lambda function. For more steps please (refer)[https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-run-lambda-schedule.html]

## Acknowledgments

- This Lambda function was created to address the need for validating security groups used by Amazon SageMaker models. Over period of time the underlying securtiy groups get deleted which will cause issues with Sagemaker Endpoint Auto Scaling. This may lead downtime aswell if not addressed timely. 

