import boto3
from botocore.exceptions import ClientError
import json
import sys

def check_s3_policy(bucket_name):
    client = boto3.client("s3", region_name='us-west-2')

    # Get existing policy so that we don't overwrite anything
    try:
        result = client.get_bucket_policy(Bucket=bucket_name)
        if result == None:
            return None
        else:
            return result
    except ClientError as e:
        print("failed to retrieve policy")
        print(e)
        return None

if __name__ == "__main__":
    bucket_name = sys.argv[1]
    source_aws_account = boto3.client('sts').get_caller_identity().get('Account')
    print("Our current account number: " + source_aws_account)
    connect_instance_arn = ""
    standard_bucket_policy = {

                "Sid": "AWSHTTPSAccess",
                "Action": [
                    "s3:*"
                ],
                "Effect": "Deny",
                "Resource": [
                    "arn:aws:s3:::"+ bucket_name,
                    "arn:aws:s3:::" + bucket_name + "/*"
                ],
                "Condition": {
                    "Bool": {
                        "aws:SecureTransport": "false"
                    }
                },
                "Principal": "*"

    }
    
    existing_policy = check_s3_policy(bucket_name)
    if existing_policy == None:
        print("No policy exists so lets create a new one")
        print("Applying our standard bucket policy that denies non-HTTPS traffic...")
        try:
            new_bucket_policy = {
                "Version": "2012-10-17",
                "Statement": [standard_bucket_policy]
            }
            client = boto3.client("s3", region_name='us-west-2')
            client.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(new_bucket_policy))
            
        except ClientError as e:
            print("failed to put bucket policy")
            print(e)
    else:
        print("There is a policy so we need to modify")
        policy_to_modify = json.loads(existing_policy['Policy'])
        policy_to_modify['Statement'].append(standard_bucket_policy)
        try:
            client = boto3.client("s3", region_name="us-west-2")
            client.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(policy_to_modify))
        except ClientError as e:
            print("Error putting new bucket policy")
            print(e)
        
    print("Our bucket now follows all compliance ...")
    print("Exiting ...")