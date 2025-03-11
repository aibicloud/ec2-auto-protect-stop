#!/bin/bash

# 设置错误时退出
set -e

# 项目名称和区域
PROJECT_NAME="ec2_protection_cdk"
REGION="us-west-2"  # 或者你想要的其他区域

# 确保我们在正确的目录中
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# 创建并激活虚拟环境（如果不存在）
if [ ! -d ".venv" ]; then
    echo "创建虚拟环境"
    python3 -m venv .venv
fi

echo "激活虚拟环境"
source .venv/bin/activate

# 安装依赖
echo "安装依赖"
pip install -r requirements.txt
pip install aws-cdk-lib

# 检查 Lambda 函数目录是否存在
if [ ! -d "lambda" ]; then
    echo "错误: Lambda 函数目录不存在"
    exit 1
fi

# 检查 index.py 是否存在
if [ ! -f "lambda/index.py" ]; then
    echo "错误: lambda/index.py 不存在"
    exit 1
fi

# 检查栈文件是否存在
if [ ! -f "${PROJECT_NAME}/${PROJECT_NAME}_stack.py" ]; then
    echo "错误: ${PROJECT_NAME}/${PROJECT_NAME}_stack.py 不存在"
    exit 1
fi

# 在部署 CDK 栈之前添加这些行
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
export AWS_DEFAULT_REGION=us-west-2

echo "开始部署 CDK 栈到 $AWS_DEFAULT_REGION 区域，账户 ID: $AWS_ACCOUNT_ID"
cdk bootstrap aws://$AWS_ACCOUNT_ID/$AWS_DEFAULT_REGION
cdk synth
cdk deploy --require-approval never


echo "CDK 部署完成！"
