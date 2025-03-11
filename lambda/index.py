import boto3
import logging
import re

# 设置日志
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 创建 EC2 客户端
ec2 = boto3.client('ec2')

def get_instance_types_with_local_storage():
    """获取所有支持实例存储的实例类型，并使用通配符合并相同系列"""
    instance_types = set()
    paginator = ec2.get_paginator('describe_instance_types')
    
    for page in paginator.paginate(Filters=[{'Name': 'instance-storage-supported', 'Values': ['true']}]):
        for instance_type in page['InstanceTypes']:
            # 使用正则表达式提取实例系列
            match = re.match(r'([a-z]+\d+[a-z]*)\..*', instance_type['InstanceType'])
            if match:
                instance_family = match.group(1)
                instance_types.add(f"{instance_family}.*")
            else:
                instance_types.add(instance_type['InstanceType'])
    
    return list(instance_types)

def get_instances_with_local_storage():
    """获取所有使用实例存储的 EC2 实例"""
    instances = []
    instance_types = get_instance_types_with_local_storage()
    
    paginator = ec2.get_paginator('describe_instances')
    filters = [
        {'Name': 'instance-state-name', 'Values': ['running', 'stopped']},
        {'Name': 'instance-type', 'Values': instance_types}
    ]

    for page in paginator.paginate(Filters=filters):
        for reservation in page['Reservations']:
            for instance in reservation['Instances']:
                instances.append(instance['InstanceId'])
    
    return instances

def check_and_disable_instance_stop(instance_id):
    """检查并禁止实例关机"""
    try:
        response = ec2.describe_instance_attribute(
            InstanceId=instance_id,
            Attribute='disableApiStop'
        )
        if not response.get('DisableApiStop', {}).get('Value', False):
            ec2.modify_instance_attribute(
                InstanceId=instance_id,
                DisableApiStop={'Value': True}
            )
            logger.info(f"已禁止实例 {instance_id} 的关机操作")
        else:
            logger.info(f"实例 {instance_id} 已经禁止关机操作")
    except Exception as e:
        logger.error(f"检查或禁止实例 {instance_id} 关机时出错: {str(e)}")

def check_and_disable_instance_termination(instance_id):
    """检查并禁止实例终止"""
    try:
        response = ec2.describe_instance_attribute(
            InstanceId=instance_id,
            Attribute='disableApiTermination'
        )
        if not response.get('DisableApiTermination', {}).get('Value', False):
            ec2.modify_instance_attribute(
                InstanceId=instance_id,
                DisableApiTermination={'Value': True}
            )
            logger.info(f"已禁止实例 {instance_id} 的终止操作")
        else:
            logger.info(f"实例 {instance_id} 已经禁止终止操作")
    except Exception as e:
        logger.error(f"检查或禁止实例 {instance_id} 终止时出错: {str(e)}")

def lambda_handler(event, context):
    # 获取所有使用实例存储的 EC2 实例
    instances_with_local_storage = get_instances_with_local_storage()
    logger.info(f"找到 {len(instances_with_local_storage)} 个使用实例存储的 EC2 实例")

    # 对每个实例执行操作
    for instance_id in instances_with_local_storage:
        check_and_disable_instance_stop(instance_id)
        check_and_disable_instance_termination(instance_id)
    
    return {
        'statusCode': 200,
        'body': f'处理了 {len(instances_with_local_storage)} 个实例'
    }
