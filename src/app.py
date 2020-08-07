import boto3
import json
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info(event)

    instances = get_instances(event['detail']['pipeline'])

    if not instances:
        logger.info('パイプライン名からのインスタンス取得に失敗')
        return False

    response = boto3.client('ec2').describe_instance_status(
        InstanceIds=instances,
        IncludeAllInstances=True
    )

    target = []
    for instance in response['InstanceStatuses']:
        state_code = instance['InstanceState']['Code']
        # ToDo: stopping(64)の場合はsleepする？
        if state_code != 80:  # 80: stopped
            continue

        target.append(instance['InstanceId'])

    if not target:
        logger.info('停止中のインスタンスなし')
        return True

    boto3.client('ec2').start_instances(
        InstanceIds=target
    )

    logger.info('### 開始したインスタンス ###')
    logger.info(target)

    return True


def get_instances(pipeline):
    data = open('instances.json', 'r')
    result = json.load(data)

    return result[pipeline]

