---
name: aws_infrastructure
description: Design and implement AWS cloud infrastructure for the company's backend workloads — including ECS/Fargate container orchestration, RDS database tiers, S3 lifecycle management, IAM least-privilege policies, CloudWatch observability, and Terraform/CloudFormation IaC — aligned with the Stage 3 Deployment ADR.
version: "1.0.0"
---

# AWS Infrastructure

| Competency            | Description                                                                              | Quality Criteria                                                                                                                                      |
| --------------------- | ---------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| EC2 Instance Types    | Instance families (compute, memory, general), sizing, EBS volumes                        | Selects appropriate instance type based on workload characteristics; configures EBS volume type and IOPS; understands burst vs sustained performance  |
| ECS/Fargate           | Container deployment and service scaling on ECS Fargate, task definitions, health checks | Services defined as IaC; auto-scaling configured with CPU/memory targets; health checks on all task definitions; Fargate vs EC2 decision documented   |
| RDS & Aurora          | Engine selection, instance sizing, Multi-AZ, read replicas, backups, parameter groups    | Multi-AZ enabled for production; automated backups with 30-day retention; read replicas for read scaling; parameter group tuned for workload type     |
| S3 Lifecycle Policies | Storage classes, lifecycle transitions, versioning, encryption                           | Lifecycle rules move objects to Intelligent-Tiering or Glacier after defined periods; SSE-KMS encryption enforced; public access block on all buckets |
| IAM Roles & Policies  | Role assumption, policy documents, least privilege, service-linked roles                 | No wildcards in resource ARNs; roles scoped to specific services; access keys never in code; periodic review with IAM Access Analyzer                 |
| CloudWatch Alarms     | Metric alarms, log insights, dashboards, anomaly detection                               | Configures actionable alarms with appropriate thresholds; uses CloudWatch Logs Insights for debugging; creates operational dashboards                 |
| CloudFormation        | Stack management, parameters, outputs, nested stacks, drift detection                    | Writes reusable CloudFormation templates; uses parameters for environment configuration; implements drift detection                                   |

---

## Architecture Decision Context

This section provides the brief summary context needed for ADR authoring and PRD references. Refer to the sections below for full implementation detail.

### AWS Architecture Tiers

| Tier       | Services                                            | Sizing Guidance                          |
| ---------- | --------------------------------------------------- | ---------------------------------------- |
| Compute    | ECS Fargate, Lambda (async)                         | CPU: 0.5–4 vCPU; Memory: 1–8 GB per task |
| Database   | RDS Aurora PostgreSQL (multi-AZ), ElastiCache Redis | db.r6g.large minimum for production      |
| Storage    | S3 Standard → Intelligent-Tiering → Glacier         | Lifecycle transition at 30/90/365 days   |
| Networking | VPC with private subnets, NAT Gateway, ALB          | ALB idle timeout 60s for mobile clients  |

### IaC Standard

All AWS resources must be defined as Infrastructure as Code (Terraform or AWS CloudFormation). No manual console creation for production resources. IaC changes go through the same PR review process as application code.

### Fargate vs EC2 Decision

| Factor              | Fargate                        | EC2                                  |
| ------------------- | ------------------------------ | ------------------------------------ |
| Management overhead | None (serverless)              | Manage instances, patching, scaling  |
| Cost predictability | Pay per vCPU/GB-hour           | Pay for instance (cheaper at scale)  |
| Startup time        | ~2-5 seconds                   | Immediate (instance already running) |
| Custom AMI/kernel   | No                             | Yes                                  |
| GPU support         | Limited                        | Full support                         |
| Recommendation      | < 50 containers, variable load | > 50 containers, steady load         |

---

## EC2 Instance Selection

**Instance family decision matrix:**

| Family            | Use Case                          | Examples               | Characteristics                           |
| ----------------- | --------------------------------- | ---------------------- | ----------------------------------------- |
| General Purpose   | Web servers, dev environments     | t4g.medium, m7g.large  | Balanced CPU/memory, burstable (t-series) |
| Compute Optimized | API servers, batch processing     | c7g.large, c7gn.xlarge | High CPU-to-memory ratio                  |
| Memory Optimized  | Databases, caching, analytics     | r7g.large, x2gd.large  | High memory-to-CPU ratio                  |
| Storage Optimized | NoSQL databases, data warehousing | i4i.large, d3en.xlarge | High disk I/O, NVMe SSD                   |

**Production EC2 configuration:**

```yaml
# CloudFormation snippet for EC2
ApiServerInstance:
  Type: AWS::EC2::Instance
  Properties:
    InstanceType: !Ref InstanceType
    ImageId: !Ref AMIID
    SubnetId: !Ref PrivateSubnet1
    SecurityGroupIds:
      - !Ref ApiSecurityGroup
    IamInstanceProfile: !Ref ApiInstanceProfile
    Monitoring: true

    BlockDeviceMappings:
      - DeviceName: /dev/xvda
        Ebs:
          VolumeType: gp3
          VolumeSize: 50
          Encrypted: true
          KmsKeyId: !Ref KmsKey

    UserData:
      Fn::Base64: !Sub |
        #!/bin/bash
        yum update -y
        amazon-linux-extras install docker
        systemctl enable docker
        systemctl start docker
        echo ECS_CLUSTER=${ClusterName} >> /etc/ecs/ecs.config

    Tags:
      - Key: Name
        Value: !Sub ${AWS::StackName}-api-server
      - Key: Environment
        Value: !Ref Environment
```

---

## ECS Task Definitions

```json
{
  "family": "api-service",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::123456789:role/ecs-execution-role",
  "taskRoleArn": "arn:aws:iam::123456789:role/ecs-task-role",
  "containerDefinitions": [
    {
      "name": "api",
      "image": "123456789.dkr.ecr.us-east-1.amazonaws.com/api:latest",
      "essential": true,
      "portMappings": [{ "containerPort": 8080, "protocol": "tcp" }],
      "environment": [
        { "name": "ENVIRONMENT", "value": "production" },
        { "name": "LOG_LEVEL", "value": "info" }
      ],
      "secrets": [
        {
          "name": "DATABASE_URL",
          "valueFrom": "arn:aws:ssm:us-east-1:123456789:parameter/api/database-url"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/api-service",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "healthCheck": {
        "command": [
          "CMD-SHELL",
          "curl -f http://localhost:8080/healthz || exit 1"
        ],
        "interval": 30,
        "timeout": 5,
        "retries": 3,
        "startPeriod": 60
      }
    }
  ]
}
```

**ECS Service with auto-scaling:**

```yaml
# CloudFormation — ECS Service
ApiService:
  Type: AWS::ECS::Service
  DependsOn: LoadBalancerListener
  Properties:
    Cluster: !Ref Cluster
    TaskDefinition: !Ref ApiTaskDefinition
    ServiceName: api-service
    DesiredCount: 3
    LaunchType: FARGATE
    NetworkConfiguration:
      AwsvpcConfiguration:
        Subnets:
          - !Ref PrivateSubnet1
          - !Ref PrivateSubnet2
          - !Ref PrivateSubnet3
        SecurityGroups:
          - !Ref ApiSecurityGroup
        AssignPublicIp: DISABLED
    LoadBalancers:
      - ContainerName: api
        ContainerPort: 8080
        TargetGroupArn: !Ref ApiTargetGroup
    HealthCheckGracePeriodSeconds: 120

ApiScalableTarget:
  Type: AWS::ApplicationAutoScaling::ScalableTarget
  Properties:
    ServiceNamespace: ecs
    ResourceId: !Sub service/${Cluster}/${ApiService}
    ScalableDimension: ecs:service:DesiredCount
    MinCapacity: 3
    MaxCapacity: 20
    RoleARN: !Ref AutoScalingRole

ApiScalingPolicy:
  Type: AWS::ApplicationAutoScaling::ScalingPolicy
  Properties:
    PolicyName: api-cpu-scaling
    PolicyType: TargetTrackingScaling
    ScalingTargetId: !Ref ApiScalableTarget
    TargetTrackingScalingPolicyConfiguration:
      TargetValue: 70.0
      PredefinedMetricSpecification:
        PredefinedMetricType: ECSServiceAverageCPUUtilization
      ScaleInCooldown: 300
      ScaleOutCooldown: 60
```

---

## RDS Configuration

```yaml
# CloudFormation — RDS PostgreSQL (production)
Database:
  Type: AWS::RDS::DBInstance
  Properties:
    Engine: postgres
    EngineVersion: "16.2"
    DBInstanceClass: db.r7g.large
    AllocatedStorage: 100
    MaxAllocatedStorage: 500
    StorageType: gp3
    StorageEncrypted: true
    KmsKeyId: !Ref KmsKey

    DBName: !Ref DatabaseName
    MasterUsername: !Sub "{{resolve:secretsmanager:${DatabaseSecret}::username}}"
    MasterUserPassword: !Sub "{{resolve:secretsmanager:${DatabaseSecret}::password}}"

    MultiAZ: true
    DeletionProtection: true
    BackupRetentionPeriod: 35
    PreferredBackupWindow: "03:00-04:00"
    PreferredMaintenanceWindow: "sun:04:00-sun:05:00"

    DBSubnetGroupName: !Ref DBSubnetGroup
    VPCSecurityGroups:
      - !Ref DatabaseSecurityGroup
    DBParameterGroupName: !Ref DBParameterGroup

    EnableCloudwatchLogsExports:
      - postgresql
      - upgrade
    MonitoringInterval: 60
    MonitoringRoleArn: !Ref RDSMonitoringRole

# Read replica for read scaling
DatabaseReadReplica:
  Type: AWS::RDS::DBInstance
  Properties:
    SourceDBInstanceIdentifier: !Ref Database
    DBInstanceClass: db.r7g.large
    MultiAZ: false
    StorageEncrypted: true
    KmsKeyId: !Ref KmsKey
```

---

## S3 Lifecycle Policies

```yaml
DataBucket:
  Type: AWS::S3::Bucket
  Properties:
    BucketName: !Sub company-data-${AWS::AccountId}-${AWS::Region}
    VersioningConfiguration:
      Status: Enabled
    BucketEncryption:
      ServerSideEncryptionConfiguration:
        - ServerSideEncryptionByDefault:
            SSEAlgorithm: aws:kms
            KMSMasterKeyID: !Ref KmsKey
    PublicAccessBlockConfiguration:
      BlockPublicAcls: true
      BlockPublicPolicy: true
      IgnorePublicAcls: true
      RestrictPublicBuckets: true
    LifecycleConfiguration:
      Rules:
        - Id: TransitionToIA
          Status: Enabled
          Prefix: uploads/
          Transitions:
            - TransitionInDays: 30
              StorageClass: STANDARD_IA
            - TransitionInDays: 90
              StorageClass: GLACIER_INSTANT_RETRIEVAL
            - TransitionInDays: 365
              StorageClass: GLACIER
          NoncurrentVersionTransitions:
            - NoncurrentDays: 30
              StorageClass: STANDARD_IA
            - NoncurrentDays: 90
              StorageClass: GLACIER
          NoncurrentVersionExpiration:
            NoncurrentDays: 365
        - Id: AbortIncompleteUploads
          Status: Enabled
          Prefix: ""
          AbortIncompleteMultipartUpload:
            DaysAfterInitiation: 7
```

**S3 storage class decision:**

| Storage Class | Retrieval Time | Cost (per GB/month) | Use Case                           |
| ------------- | -------------- | ------------------- | ---------------------------------- |
| STANDARD      | Milliseconds   | $0.023              | Active data, frequent access       |
| STANDARD_IA   | Milliseconds   | $0.0125             | Infrequent access, rapid retrieval |
| GLACIER_IR    | Milliseconds   | $0.004              | Long-term with instant access      |
| GLACIER       | 1-5 minutes    | $0.0036             | Archive, occasional access         |
| DEEP_ARCHIVE  | 12 hours       | $0.00199            | Compliance archive, rare access    |

---

## IAM Roles & Policies

**Least-privilege IAM policy for ECS task:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["logs:CreateLogStream", "logs:PutLogEvents"],
      "Resource": "arn:aws:logs:us-east-1:123456789:log-group:/ecs/api-service:*"
    },
    {
      "Effect": "Allow",
      "Action": ["ssm:GetParameters", "secretsmanager:GetSecretValue"],
      "Resource": [
        "arn:aws:ssm:us-east-1:123456789:parameter/api/*",
        "arn:aws:secretsmanager:us-east-1:123456789:secret:api/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
      "Resource": "arn:aws:s3:::company-data-*/uploads/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "sqs:SendMessage",
        "sqs:ReceiveMessage",
        "sqs:DeleteMessage",
        "sqs:GetQueueAttributes"
      ],
      "Resource": "arn:aws:sqs:us-east-1:123456789:api-event-queue"
    }
  ]
}
```

**IAM policy principles:**

| Principle       | Implementation                                                |
| --------------- | ------------------------------------------------------------- |
| Least privilege | Grant only required actions on specific resources             |
| No wildcards    | Avoid `*` in Action and Resource unless absolutely necessary  |
| Use conditions  | Add `StringEquals`, `DateLessThan` for additional constraints |
| Roles over keys | Use IAM roles for services, never store access keys in code   |
| Regular review  | Audit unused permissions quarterly with IAM Access Analyzer   |

---

## CloudWatch Alarms

```yaml
ApiCpuAlarm:
  Type: AWS::CloudWatch::Alarm
  Properties:
    AlarmName: !Sub ${AWS::StackName}-api-high-cpu
    AlarmDescription: "API service CPU utilization exceeds 80% for 5 minutes"
    Namespace: AWS/ECS
    MetricName: CPUUtilization
    Dimensions:
      - Name: ClusterName
        Value: !Ref Cluster
      - Name: ServiceName
        Value: !Ref ApiService
    Statistic: Average
    Period: 300
    EvaluationPeriods: 2
    Threshold: 80
    ComparisonOperator: GreaterThanThreshold
    AlarmActions:
      - !Ref AlertSNSTopic
    OKActions:
      - !Ref AlertSNSTopic

ApiErrorRateAlarm:
  Type: AWS::CloudWatch::Alarm
  Properties:
    AlarmName: !Sub ${AWS::StackName}-api-high-error-rate
    AlarmDescription: "API 5xx error rate exceeds 1% for 5 minutes"
    Namespace: AWS/ApplicationELB
    MetricName: HTTPCode_Target_5XX_Count
    Dimensions:
      - Name: LoadBalancer
        Value: !GetAtt LoadBalancer.LoadBalancerFullName
      - Name: TargetGroup
        Value: !GetAtt ApiTargetGroup.TargetGroupFullName
    Statistic: Sum
    Period: 60
    EvaluationPeriods: 5
    Threshold: 10
    ComparisonOperator: GreaterThanThreshold
    AlarmActions:
      - !Ref PagerDutySNSTopic
```

**CloudWatch Logs Insights — debugging query:**

```
fields @timestamp, @message
| filter @logStream like /api/
| filter @message like /ERROR/
| sort @timestamp desc
| limit 100
```

---

## CloudFormation Template Structure

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Description: >
  API Service Infrastructure
  Deployed by: backend-team

Parameters:
  Environment:
    Type: String
    AllowedValues: [development, staging, production]
    Default: development

  InstanceType:
    Type: String
    Default: t4g.medium
    AllowedValues: [t4g.small, t4g.medium, m7g.large]

Mappings:
  EnvironmentConfig:
    development:
      InstanceCount: 1
      BackupRetention: 7
    staging:
      InstanceCount: 2
      BackupRetention: 14
    production:
      InstanceCount: 3
      BackupRetention: 35

Resources:
  # ... resource definitions ...

Outputs:
  ApiEndpoint:
    Description: "API service endpoint URL"
    Value: !Sub https://${LoadBalancer.DNSName}
    Export:
      Name: !Sub ${AWS::StackName}-ApiEndpoint

  DatabaseEndpoint:
    Description: "RDS database endpoint"
    Value: !GetAtt Database.Endpoint.Address
    Export:
      Name: !Sub ${AWS::StackName}-DatabaseEndpoint
```

---

## Pipeline Integration

- **Stage 3 (Architecture):** Infrastructure diagrams must show AWS service topology, network architecture (VPC, subnets, security groups), and data flow. ADR required for EC2 vs Fargate, RDS vs managed alternatives.
- **Stage 4 (Implementation Plan):** CloudFormation templates authored as infrastructure dependencies. IAM policies defined per service. RDS and S3 configuration aligned with data model requirements.
- **Stage 5 (Development):** Infrastructure provisioned via CloudFormation. ECS task definitions deployed. CloudWatch alarms configured. IAM roles attached to services.
- **Stage 6 (Code Review):** Review IAM policies for least privilege. Validate CloudFormation template correctness. Check CloudWatch alarm thresholds. Verify encryption configuration.
- **Stage 7 (Testing):** Infrastructure tests validate CloudFormation deployment. Security tests validate IAM policies. Load tests validate auto-scaling configuration.
- **Stage 10 (Release Readiness):** Panel verifies infrastructure matches architecture, all alarms configured, backup policies in place, and IAM policies follow least privilege.

## Quality Standards

| Metric                | Target                        | Measurement                        |
| --------------------- | ----------------------------- | ---------------------------------- |
| IAM policy compliance | 100% least privilege          | IAM Access Analyzer                |
| Encryption at rest    | 100% of data stores           | AWS Config rules                   |
| Backup coverage       | 100% of production databases  | Backup audit                       |
| Alarm coverage        | 100% of critical metrics      | CloudWatch alarm inventory         |
| CloudFormation drift  | 0 resources drifted           | Drift detection                    |
| S3 public access      | 0 publicly accessible buckets | S3 public access block             |
| Auto-scaling          | Tested and functional         | Load test with scaling observation |
| Cost efficiency       | Within 10% of estimate        | AWS Cost Explorer                  |
