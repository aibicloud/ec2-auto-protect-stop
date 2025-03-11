#!/usr/bin/env python3
import os
import aws_cdk as cdk
from ec2_protection_cdk.ec2_protection_cdk_stack import EC2ProtectionLambdaStack

app = cdk.App()
EC2ProtectionLambdaStack(app, "EC2ProtectionLambdaStack",
    env=cdk.Environment(
        account=os.environ.get("AWS_ACCOUNT_ID"),
        region=os.environ.get("AWS_DEFAULT_REGION", "us-west-2")
    )
)

app.synth()
