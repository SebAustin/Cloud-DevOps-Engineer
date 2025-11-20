# Udagram - High-Availability Web Application Deployment

## Project Overview

This project demonstrates the deployment of a high-availability web application (Udagram) on AWS using Infrastructure as Code (IaC) principles with AWS CloudFormation. The infrastructure includes a custom VPC, public and private subnets across multiple availability zones, auto-scaling EC2 instances, an Application Load Balancer, and S3 for static content hosting.

## Architecture

The infrastructure follows AWS best practices for high availability and security:

- **Multi-AZ Deployment**: Resources distributed across 2 Availability Zones
- **Network Segmentation**: Public and private subnets with proper routing
- **Auto Scaling**: 4 EC2 instances (2 per AZ) with auto-scaling capabilities
- **Load Balancing**: Application Load Balancer for traffic distribution
- **Security**: EC2 instances in private subnets with least-privilege security groups
- **Static Content**: S3 bucket for hosting static web content
- **High Availability**: NAT Gateways in each AZ for redundancy

### Architecture Diagram

See `infrastructure-diagram.drawio` for a visual representation of the architecture. You can open this file with [draw.io](https://app.diagrams.net/) or [diagrams.net](https://www.diagrams.net/).

## Infrastructure Components

### Network Stack (`network.yml`)

- **VPC**: 10.0.0.0/16 CIDR block
- **Public Subnets**: 
  - Public Subnet 1: 10.0.1.0/24 (AZ1)
  - Public Subnet 2: 10.0.2.0/24 (AZ2)
- **Private Subnets**: 
  - Private Subnet 1: 10.0.3.0/24 (AZ1)
  - Private Subnet 2: 10.0.4.0/24 (AZ2)
- **Internet Gateway**: Provides internet access to public subnets
- **NAT Gateways**: 2 NAT Gateways (one per AZ) for high availability
- **Route Tables**: Separate route tables for public and private subnets

### Application Stack (`udagram.yml`)

- **S3 Bucket**: Public-read access for static content
- **IAM Role**: EC2 instance role with S3 read/write permissions
- **Security Groups**: 
  - Load Balancer SG: Allows HTTP (port 80) from anywhere
  - Web Server SG: Allows HTTP only from Load Balancer
- **Launch Template**: 
  - Instance Type: t2.micro
  - OS: Ubuntu 22.04 LTS
  - Disk: 10 GB
  - UserData: Installs Apache2, downloads content from S3
- **Auto Scaling Group**: 
  - Min: 2 instances
  - Max: 4 instances
  - Desired: 4 instances
- **Application Load Balancer**: Internet-facing, distributes traffic to EC2 instances
- **Target Group**: Health checks on port 80 with appropriate thresholds

## Prerequisites

Before deploying the infrastructure, ensure you have:

1. **AWS Account**: An active AWS account with appropriate permissions
2. **AWS CLI**: Installed and configured with valid credentials
   ```bash
   aws configure
   ```
3. **Python 3.7+**: Required for automation scripts
4. **Boto3**: AWS SDK for Python
   ```bash
   pip install -r requirements.txt
   ```
5. **Sufficient Permissions**: Your IAM user/role must have permissions to create:
   - VPC and networking resources
   - EC2 instances and Auto Scaling Groups
   - IAM roles and policies
   - S3 buckets
   - CloudFormation stacks

## Project Files

```
.
├── network.yml                    # Network infrastructure CloudFormation template
├── network-parameters.json        # Parameters for network stack
├── udagram.yml                    # Application infrastructure CloudFormation template
├── udagram-parameters.json        # Parameters for application stack
├── create.py                      # Python script to create infrastructure
├── delete.py                      # Python script to delete infrastructure
├── requirements.txt               # Python dependencies
├── infrastructure-diagram.drawio  # Architecture diagram (draw.io format)
├── static-content/
│   └── index.html                # Static web page
└── README.md                      # This file
```

## Deployment Instructions

### Option 1: Automated Deployment (Recommended)

The easiest way to deploy the infrastructure is using the provided Python scripts:

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Update Region** (if needed):
   Edit `create.py` and `delete.py` to set your preferred AWS region (default is `us-east-1`)

3. **Update AMI ID** (if needed):
   Edit `udagram-parameters.json` to use the correct Ubuntu 22.04 AMI for your region.
   Find AMI IDs at: https://cloud-images.ubuntu.com/locator/ec2/

4. **Create Infrastructure**:
   ```bash
   python create.py
   ```
   
   This script will:
   - Create the network stack
   - Wait for network stack completion
   - Create the application stack
   - Wait for application stack completion
   - Upload static content to S3
   - Display the Load Balancer URL

5. **Access Your Application**:
   Wait 5-10 minutes for the instances to become healthy, then access the application using the Load Balancer URL displayed in the output.

### Option 2: Manual Deployment

If you prefer to use the AWS CLI directly:

1. **Create Network Stack**:
   ```bash
   aws cloudformation create-stack \
     --stack-name udagram-network \
     --template-body file://network.yml \
     --parameters file://network-parameters.json \
     --region us-east-1
   ```

2. **Wait for Network Stack**:
   ```bash
   aws cloudformation wait stack-create-complete \
     --stack-name udagram-network \
     --region us-east-1
   ```

3. **Create Application Stack**:
   ```bash
   aws cloudformation create-stack \
     --stack-name udagram-app \
     --template-body file://udagram.yml \
     --parameters file://udagram-parameters.json \
     --capabilities CAPABILITY_NAMED_IAM \
     --region us-east-1
   ```

4. **Wait for Application Stack**:
   ```bash
   aws cloudformation wait stack-create-complete \
     --stack-name udagram-app \
     --region us-east-1
   ```

5. **Get S3 Bucket Name**:
   ```bash
   aws cloudformation describe-stacks \
     --stack-name udagram-app \
     --query 'Stacks[0].Outputs[?OutputKey==`S3BucketName`].OutputValue' \
     --output text \
     --region us-east-1
   ```

6. **Upload Static Content**:
   ```bash
   aws s3 cp static-content/index.html s3://YOUR-BUCKET-NAME/index.html
   ```

7. **Get Load Balancer URL**:
   ```bash
   aws cloudformation describe-stacks \
     --stack-name udagram-app \
     --query 'Stacks[0].Outputs[?OutputKey==`LoadBalancerURL`].OutputValue' \
     --output text \
     --region us-east-1
   ```

## Verification

After deployment, verify that the infrastructure is working correctly:

1. **Access the Application**:
   - Open the Load Balancer URL in your web browser
   - You should see: "It works! Udagram, Udacity"

2. **Check Stack Outputs**:
   ```bash
   aws cloudformation describe-stacks --stack-name udagram-app --region us-east-1
   aws cloudformation describe-stacks --stack-name udagram-network --region us-east-1
   ```

3. **Verify EC2 Instances**:
   ```bash
   aws ec2 describe-instances \
     --filters "Name=tag:Name,Values=Udagram-WebServer" \
     --query 'Reservations[*].Instances[*].[InstanceId,State.Name,PrivateIpAddress]' \
     --output table \
     --region us-east-1
   ```

4. **Check Load Balancer Health**:
   ```bash
   aws elbv2 describe-target-health \
     --target-group-arn YOUR-TARGET-GROUP-ARN \
     --region us-east-1
   ```

## Teardown Instructions

### Option 1: Automated Deletion (Recommended)

Use the provided Python script to safely delete all resources:

```bash
python delete.py
```

This script will:
- Ask for confirmation
- Empty the S3 bucket (required before deletion)
- Delete the application stack
- Wait for application stack deletion
- Delete the network stack
- Wait for network stack deletion

### Option 2: Manual Deletion

If you prefer to use the AWS CLI:

1. **Empty S3 Bucket** (required):
   ```bash
   aws s3 rm s3://YOUR-BUCKET-NAME --recursive --region us-east-1
   ```

2. **Delete Application Stack**:
   ```bash
   aws cloudformation delete-stack --stack-name udagram-app --region us-east-1
   ```

3. **Wait for Application Stack Deletion**:
   ```bash
   aws cloudformation wait stack-delete-complete --stack-name udagram-app --region us-east-1
   ```

4. **Delete Network Stack**:
   ```bash
   aws cloudformation delete-stack --stack-name udagram-network --region us-east-1
   ```

5. **Wait for Network Stack Deletion**:
   ```bash
   aws cloudformation wait stack-delete-complete --stack-name udagram-network --region us-east-1
   ```

## Cost Considerations

This infrastructure will incur AWS charges. Estimated monthly costs (us-east-1):

- **EC2 Instances**: 4 x t2.micro (~$3.36/instance/month) = ~$13.44/month
- **NAT Gateways**: 2 x NAT Gateway (~$32.40/gateway/month) = ~$64.80/month
- **Application Load Balancer**: ~$16.20/month
- **S3**: Minimal (first 50 TB is $0.023 per GB)
- **Data Transfer**: Variable based on usage

**Total Estimated Cost**: ~$95-100/month

**Important**: Remember to delete the infrastructure when not in use to avoid charges!

## Troubleshooting

### Common Issues

1. **Stack Creation Fails**:
   - Check CloudFormation events in AWS Console
   - Verify your AWS credentials have sufficient permissions
   - Ensure the AMI ID is valid for your region

2. **Website Not Loading**:
   - Wait 5-10 minutes for instances to pass health checks
   - Verify the static content was uploaded to S3
   - Check Security Group rules
   - View logs: `ssh` into bastion host (if configured) and check `/var/log/cloud-init-output.log`

3. **S3 Upload Fails**:
   - Verify the bucket was created successfully
   - Check IAM permissions for the EC2 role
   - Manually upload: `aws s3 cp static-content/index.html s3://YOUR-BUCKET-NAME/`

4. **Instances Not Healthy**:
   - Check the UserData script in the Launch Template
   - Verify Apache2 is running: `systemctl status apache2`
   - Check application logs: `/var/log/apache2/error.log`
   - Verify the S3 download succeeded in `/var/log/cloud-init-output.log`

5. **Cannot Delete Stack**:
   - Ensure S3 bucket is empty
   - Check for resources with dependencies
   - Delete resources manually if needed through AWS Console

### Debug Tips

- **UserData Logs**: Instance UserData script logs are in `/var/log/cloud-init-output.log`
- **Apache Logs**: `/var/log/apache2/access.log` and `/var/log/apache2/error.log`
- **CloudFormation Events**: Check stack events in AWS Console for detailed error messages
- **Health Check**: Ensure the health check path `/` returns HTTP 200

## Design Decisions

### Why Two Stacks?

The infrastructure is split into network and application stacks to:
- Allow different teams to manage network vs. application resources
- Enable application updates without affecting the network
- Follow separation of concerns principle
- Facilitate easier testing and rollback

### Why Private Subnets for EC2?

EC2 instances are in private subnets for security:
- No direct internet access (reduces attack surface)
- Access only through Load Balancer
- Outbound internet access via NAT Gateways for updates
- Follows AWS security best practices

### Why Two NAT Gateways?

Using one NAT Gateway per AZ provides:
- High availability (no single point of failure)
- Better performance (distributed load)
- Resilience to AZ failures
- AWS recommended architecture

## Customization

### Change Instance Type

Edit `udagram-parameters.json`:
```json
{
  "ParameterKey": "InstanceType",
  "ParameterValue": "t2.small"
}
```

### Change Number of Instances

Edit `udagram.yml`, find `WebServerAutoScalingGroup` and modify:
```yaml
MinSize: 2
MaxSize: 6
DesiredCapacity: 4
```

### Change CIDR Blocks

Edit `network-parameters.json` to use different IP ranges.

### Add HTTPS Support

1. Obtain an SSL certificate from ACM
2. Add a listener on port 443 to the ALB
3. Update Security Groups to allow port 443
4. Add redirect from HTTP to HTTPS

## Project Evidence

### Option 1: Working URL

After deployment, the application is accessible at:
```
http://udagram-alb-XXXXXXXXXX.us-east-1.elb.amazonaws.com
```

The page displays: **"It works! Udagram, Udacity"**

### Option 2: Screenshots

If you've deleted the infrastructure, include these screenshots:

1. **CloudFormation Stacks Outputs**: Shows both stacks with timestamps
2. **Load Balancer URL Access**: Browser showing the working application
3. **S3 Bucket Contents**: Shows `index.html` file in the bucket

## Additional Resources

- [AWS CloudFormation Documentation](https://docs.aws.amazon.com/cloudformation/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [Ubuntu Cloud Images](https://cloud-images.ubuntu.com/locator/ec2/)
- [AWS Auto Scaling Best Practices](https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-best-practices.html)

## License

This project is part of the Udacity Cloud DevOps Engineer Nanodegree program.

## Author

Created for the Udacity Cloud DevOps Engineer Nanodegree - Deploy a High-Availability Web App using CloudFormation project.

---

**Note**: Always remember to delete your infrastructure after testing to avoid unnecessary AWS charges!

```bash
python delete.py
```

