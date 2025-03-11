import os
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_events as events,
    aws_events_targets as targets,
    Duration,
)
from constructs import Construct

class EC2ProtectionLambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 创建 Lambda 函数
        lambda_fn = _lambda.Function(
            self, "EC2ProtectionLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="index.lambda_handler",
            code=_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), "..", "lambda")),
            timeout=Duration.minutes(15),
            memory_size=512,
        )

        # 添加必要的 IAM 权限
        lambda_fn.add_to_role_policy(iam.PolicyStatement(
            actions=[
                "ec2:DescribeInstanceTypes",
                "ec2:DescribeInstances",
                "ec2:ModifyInstanceAttribute",
                "ec2:DescribeInstanceAttribute" 
            ],
            resources=["*"]
        ))

        # 创建 EventBridge 规则
        rule = events.Rule(
            self, "EC2ProtectionRule",
            schedule=events.Schedule.rate(Duration.minutes(10))
        )

        # 将 Lambda 函数添加为规则的目标
        rule.add_target(targets.LambdaFunction(lambda_fn))

# 主应用程序代码
# app = cdk.App()
# EC2ProtectionLambdaStack(app, "EC2ProtectionLambdaStack",
#     env=cdk.Environment(account=os.environ["CDK_DEFAULT_ACCOUNT"], region="us-west-2")
# )
# app.synth()
