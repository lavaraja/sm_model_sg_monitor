import json

import boto3
import time
def lambda_handler(event, context):

    # set region
    region="us-east-1"

    # Create a SageMaker client
    sagemaker_client = boto3.client('sagemaker',region_name=region)

    # Create an SNS client
    sns_client = boto3.client('sns',"us-east-1")
    
    sns_topic_arn = 'YOUR_SNS_TOPIC_ARN'  # Replace with your SNS topic ARN
    
    # Create EC2 client
    ec2_client = boto3.client('ec2',"us-east-1")
    
    ##endpoints_to_monitor =[] # not implemented yet..
    models_to_monitor=[]
    next_token=None
    while True:
        if next_token:
            models_response = sagemaker_client.list_models(NextToken=next_token)
        else:
            models_response = sagemaker_client.list_models()
        for model in models_response['Models']:
            model_name = model['ModelName']
            models_to_monitor.append(model_name)
            model_details = sagemaker_client.describe_model(ModelName=model_name)
            time.sleep(0.2)
            if "VpcConfig" in model_details:
                vpc_config = model_details['VpcConfig']
                print(vpc_config)
                        # Check if the VPC configuration exists
                if 'SecurityGroupIds' in vpc_config:
                    for sg_id in vpc_config['SecurityGroupIds']:
                        try:
                            ec2_client.describe_security_groups(GroupIds=[sg_id])
                        except ec2_client.exceptions.ClientError as e:
                            if e.response['Error']['Code'] == 'InvalidGroup.NotFound':
                                message = f"Security group {sg_id} used by model {model_name} does not exist."
                                print(message)
                                sns_client.publish(TopicArn=sns_topic_arn, Message=message, Subject="!!Missing Security Group!! Used by Sagemaker Model/Endpoint. [Action Required]")
                            else:
                               print(f"Error occurred while checking security group {sg_id}: {e}")
                             
   
        if 'NextToken' in models_response:
            next_token = models_response['NextToken']
        else:
            break

    return "Security group validation complete"
