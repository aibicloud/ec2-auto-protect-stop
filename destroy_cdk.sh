#!/bin/bash

# 切换到脚本所在目录
cd "$(dirname "$0")"

# 设置错误时退出
set -e

# 项目名称和区域
PROJECT_NAME="ec2_protection_cdk"
REGION="us-west-2"

# 颜色代码
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 函数：显示带颜色的消息
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# 函数：确认操作
confirm_operation() {
    read -p "$(print_message $YELLOW "警告: 这将删除所有由此 CDK 栈创建的资源。是否确定要继续? (y/n) ")" choice
    case "$choice" in 
        y|Y ) return 0;;
        n|N ) return 1;;
        * ) print_message $RED "无效的输入"; return 1;;
    esac
}

# 主要删除逻辑
main() {
    # 检查项目目录是否存在
    if [ ! -d "$PROJECT_NAME" ]; then
        print_message $RED "错误: 项目目录 $PROJECT_NAME 不存在"
        exit 1
    fi

    # 检查虚拟环境是否存在
    if [ ! -d ".venv" ]; then
        print_message $RED "错误: 虚拟环境不存在，请先运行部署脚本"
        exit 1
    fi

    # 激活虚拟环境
    print_message $GREEN "激活虚拟环境"
    source .venv/bin/activate

    # 确认操作
    if ! confirm_operation; then
        print_message $YELLOW "操作已取消"
        exit 0
    fi

    # 删除 CDK 栈
    print_message $GREEN "开始删除 $REGION 区域的 CDK 栈"
    cdk destroy --force --region $REGION

    print_message $GREEN "CDK 栈删除完成！"
}

# 运行主函数
main
