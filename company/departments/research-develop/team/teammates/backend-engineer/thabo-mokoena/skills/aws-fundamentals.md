---
version: "1.0.0"
---

| Competency            | Description                                                              | Quality Criteria                                                                                                                                     |
| --------------------- | ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| EC2 Instance Types    | Instance families (compute, memory, general), sizing, EBS volumes        | Selects appropriate instance type based on workload characteristics; configures EBS volume type and IOPS; understands burst vs sustained performance |
| ECS Task Definitions  | Container definitions, resource allocation, networking, health checks    | Designs task definitions with proper CPU/memory limits; configures Fargate vs EC2 launch type; implements health check integration                   |
| RDS Configuration     | Engine selection, instance sizing, Multi-AZ, read replicas, backups      | Configures RDS for production (Multi-AZ, automated backups); sets up read replicas for read scaling; configures parameter groups                     |
| S3 Lifecycle Policies | Storage classes, lifecycle transitions, versioning, encryption           | Designs lifecycle policies for cost optimization; configures versioning for data protection; implements encryption at rest and in transit            |
| IAM Roles & Policies  | Role assumption, policy documents, least privilege, service-linked roles | Writes least-privilege IAM policies; uses roles instead of access keys; implements cross-account access when needed                                  |
| CloudWatch Alarms     | Metric alarms, log insights, dashboards, anomaly detection               | Configures actionable alarms with appropriate thresholds; uses CloudWatch Logs Insights for debugging; creates operational dashboards                |
| CloudFormation        | Stack management, parameters, outputs, nested stacks, drift detection    | Writes reusable CloudFormation templates; uses parameters for environment configuration; implements drift detection                                  |

## Execution Guidance

### EC2 Instance Selection

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
    InstanceType: !Ref InstanceType # e.g., m7g.large
    ImageId: !Ref AMIID # Amazon Linux 2023 ARM64
    SubnetId: !Ref PrivateSubnet1
    SecurityGroupIds:
      - !Ref ApiSecurityGroup
    IamInstanceProfile: !Ref ApiInstanceProfile
    Monitoring: true # Detailed monitoring (1-minute intervals)

    BlockDeviceMappings:
      - DeviceName: /dev/xvda
        Ebs:
          VolumeType: gp3 # General purpose SSD (cheaper than gp2)
          VolumeSize: 50 # GB
          Encrypted: true
          KmsKeyId: !Ref KmsKey

    UserData:
      Fn::Base64: !Sub |
        #!/bin/bash
        yum update -y
        amazon-linux-extras install docker
        systemctl enable docker
        systemctl start docker
        # Install ECS agent
        echo ECS_CLUSTER=${ClusterName} >> /etc/ecs/ecs.config

    Tags:
      - Key: Name
        Value: !Sub ${AWS::StackName}-api-server
      - Key: Environment
        Value: !Ref Environment
```

**When to use Fargate vs EC2 for ECS:**

| Factor              | Fargate                        | EC2                                  |
| ------------------- | ------------------------------ | ------------------------------------ |
| Management overhead | None (serverless)              | Manage instances, patching, scaling  |
| Cost predictability | Pay per vCPU/GB-hour           | Pay for instance (cheaper at scale)  |
| Startup time        | ~2-5 seconds                   | Immediate (instance already running) |
| Custom AMI/kernel   | No                             | Yes                                  |
| GPU support         | Limited                        | Full support                         |
| Recommendation      | < 50 containers, variable load | > 50 containers, steady load         |

### ECS Task Definitions

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
      "portMappings": [
        {
          "containerPort": 8080,
          "protocol": "tcp"
        }
      ],
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
      },
      "resourceRequirements": [
        { "type": "VCPU", "value": "1" },
        { "type": "MEMORY", "value": "2048" }
      ]
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

# Auto-scaling
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
      TargetValue: 70.0 # Target 70% CPU utilization
      PredefinedMetricSpecification:
        PredefinedMetricType: ECSServiceAverageCPUUtilization
      ScaleInCooldown: 300
      ScaleOutCooldown: 60
```

### RDS Configuration

```yaml
# CloudFormation — RDS PostgreSQL (production)
Database:
  Type: AWS::RDS::DBInstance
  Properties:
    Engine: postgres
    EngineVersion: "16.2"
    DBInstanceClass: db.r7g.large # Memory-optimized for database
    AllocatedStorage: 100
    MaxAllocatedStorage: 500 # Auto-scaling up to 500GB
    StorageType: gp3
    StorageEncrypted: true
    KmsKeyId: !Ref KmsKey

    DBName: !Ref DatabaseName
    MasterUsername: !Sub "{{resolve:secretsmanager:${DatabaseSecret}::username}}"
    MasterUserPassword: !Sub "{{resolve:secretsmanager:${DatabaseSecret}::password}}"

    # High availability
    MultiAZ: true
    DeletionProtection: true
    BackupRetentionPeriod: 35 # 35 days
    PreferredBackupWindow: "03:00-04:00"
    PreferredMaintenanceWindow: "sun:04:00-sun:05:00"

    # Network
    DBSubnetGroupName: !Ref DBSubnetGroup
    VPCSecurityGroups:
      - !Ref DatabaseSecurityGroup

    # Parameter group
    DBParameterGroupName: !Ref DBParameterGroup

    # CloudWatch monitoring
    EnableCloudwatchLogsExports:
      - postgresql
      - upgrade
    MonitoringInterval: 60
    MonitoringRoleArn: !Ref RDSMonitoringRole

# Read replica (for read scaling)
DatabaseReadReplica:
  Type: AWS::RDS::DBInstance
  Properties:
    SourceDBInstanceIdentifier: !Ref Database
    DBInstanceClass: db.r7g.large
    MultiAZ: false # Replica doesn't need Multi-AZ (source has it)
    StorageEncrypted: true
    KmsKeyId: !Ref KmsKey
```

### S3 Lifecycle Policies

```yaml
# CloudFormation — S3 bucket with lifecycle
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
              StorageClass: STANDARD_IA # Infrequent Access (cheaper)
            - TransitionInDays: 90
              StorageClass: GLACIER_INSTANT_RETRIEVAL
            - TransitionInDays: 365
              StorageClass: GLACIER # Long-term archive
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

### IAM Roles & Policies

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

### CloudWatch Alarms

```yaml
# CloudFormation — CloudWatch alarms
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
    Threshold: 10 # 10 errors per minute (adjust based on traffic)
    ComparisonOperator: GreaterThanThreshold
    AlarmActions:
      - !Ref PagerDutySNSTopic

# Log Insights query for debugging
# fields @timestamp, @message
# | filter @logStream like /api/
# | filter @message like /ERROR/
# | sort @timestamp desc
# | limit 100
```

### CloudFormation Basics

**Template structure with best practices:**

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Description: >
  API Service Infrastructure
  Deployed by: backend-team
  Last updated: 2026-04-04

# Parameters for environment customization
Parameters:
  Environment:
    Type: String
    AllowedValues: [development, staging, production]
    Default: development

  InstanceType:
    Type: String
    Default: t4g.medium
    AllowedValues: [t4g.small, t4g.medium, m7g.large]

# Mappings for environment-specific values
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

# Resources
Resources:
  # ... resource definitions ...

# Outputs for cross-stack references
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

## Pipeline Integration

**Stage 3 (Architecture):** Infrastructure diagrams must show AWS service topology, network architecture (VPC, subnets, security groups), and data flow. ADR required for EC2 vs Fargate, RDS vs managed alternatives.

**Stage 4 (Implementation Plan):** CloudFormation templates authored as infrastructure dependencies. IAM policies defined per service. RDS and S3 configuration aligned with data model requirements.

**Stage 5 (Development):** Infrastructure provisioned via CloudFormation. ECS task definitions deployed. CloudWatch alarms configured. IAM roles attached to services.

**Stage 6 (Code Review):** Review IAM policies for least privilege. Validate CloudFormation template correctness. Check CloudWatch alarm thresholds. Verify encryption configuration.

**Stage 7 (Testing):** Infrastructure tests validate CloudFormation deployment. Security tests validate IAM policies. Load tests validate auto-scaling configuration.

**Stage 10 (Release Readiness):** Panel verifies infrastructure matches architecture, all alarms configured, backup policies in place, and IAM policies follow least privilege.

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
