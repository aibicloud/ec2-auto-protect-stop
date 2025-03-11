
# 安装依赖组件

1. 安装 Python 3.9 或更高版本
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3.9
   
   # CentOS/RHEL
   sudo yum install python39
   ```

2. 安装 AWS CLI
   ```bash
   # Linux
   curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
   unzip awscliv2.zip
   sudo ./aws/install
   
   # macOS (使用 Homebrew)
   brew install awscli
   ```

3. 安装 AWS CDK CLI
   ```bash
   npm install -g aws-cdk
   ```

4. 配置 AWS 凭证
   ```bash
   aws configure
   ```

# AWS 凭证权限要求

部署此 CDK 应用程序需要以下 AWS IAM 权限:

1. CDK 部署基础权限:
   - cloudformation:*
   - iam:CreateRole
   - iam:DeleteRole 
   - iam:PutRolePolicy
   - iam:DeleteRolePolicy
   - iam:GetRole
   - iam:GetRolePolicy
   - iam:PassRole

2. Lambda 相关权限:
   - lambda:CreateFunction
   - lambda:DeleteFunction
   - lambda:GetFunction
   - lambda:UpdateFunctionCode
   - lambda:UpdateFunctionConfiguration

3. EventBridge 相关权限:
   - events:PutRule
   - events:DeleteRule
   - events:PutTargets
   - events:RemoveTargets

4. Lambda 函数运行时所需权限:
   - ec2:DescribeInstanceTypes
   - ec2:DescribeInstances
   - ec2:ModifyInstanceAttribute

建议创建具有以上权限的 IAM 用户或角色来部署此应用。



## 部署

```bash
./deploy_cdk.sh
```

## 删除

```bash
./destroy_cdk.sh
```

