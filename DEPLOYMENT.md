# Deployment Guide

This document provides step-by-step instructions for deploying the Coworking Space Analytics Microservice to AWS EKS.

## Prerequisites

Before starting, ensure you have:
- AWS CLI installed and configured with credentials
- kubectl installed (version 1.25+)
- eksctl installed
- Docker installed (for local testing)
- Git configured with SSH keys (for pushing to GitHub)
- An AWS account with appropriate IAM permissions

## Step 1: Set Up EKS Cluster

Create an EKS cluster using eksctl:

```bash
eksctl create cluster \
  --name my-cluster \
  --region us-east-1 \
  --nodegroup-name my-nodes \
  --node-type t3.small \
  --nodes 1 \
  --nodes-min 1 \
  --nodes-max 2
```

This command creates:
- An EKS cluster named "my-cluster"
- A node group with t3.small instances
- Auto-scaling between 1-2 nodes

Update your local kubeconfig:

```bash
aws eks --region us-east-1 update-kubeconfig --name my-cluster
```

Verify connection:

```bash
kubectl config current-context
kubectl get nodes
```

## Step 2: Create Amazon ECR Repository

Create an ECR repository for your Docker images:

```bash
aws ecr create-repository \
  --repository-name coworking-analytics \
  --region us-east-1
```

Note the repository URI from the output (format: `<ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/coworking-analytics`)

## Step 3: Set Up AWS CodeBuild

### Create CodeBuild Project

1. Navigate to AWS CodeBuild in the AWS Console
2. Click "Create build project"
3. Configure the following:
   - **Project name**: `coworking-analytics-build`
   - **Source provider**: GitHub
   - **Repository**: Connect your GitHub repository
   - **Environment image**: Managed image
   - **Operating system**: Amazon Linux 2
   - **Runtime**: Standard
   - **Image**: aws/codebuild/standard:5.0
   - **Privileged**: Enable (required for Docker builds)
   - **Service role**: Create new or use existing
   - **Buildspec**: Use buildspec file (buildspec.yaml)

4. Add environment variables:
   - `AWS_DEFAULT_REGION`: us-east-1
   - `AWS_ACCOUNT_ID`: Your AWS account ID
   - `IMAGE_REPO_NAME`: coworking-analytics
   - `IMAGE_TAG`: latest

### Update IAM Role Permissions

The CodeBuild service role needs ECR permissions:

```bash
# Get the role name from CodeBuild project settings
ROLE_NAME="codebuild-coworking-analytics-build-service-role"

# Attach ECR policy
aws iam attach-role-policy \
  --role-name $ROLE_NAME \
  --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryPowerUser
```

### Test CodeBuild

1. Click "Start build" in the CodeBuild console
2. Monitor the build logs
3. Verify the Docker image appears in ECR with proper tags

## Step 4: Deploy PostgreSQL Database

Apply Kubernetes manifests in order:

```bash
# Create Persistent Volume Claim
kubectl apply -f deployment/pvc.yaml

# Create Persistent Volume
kubectl apply -f deployment/pv.yaml

# Deploy PostgreSQL
kubectl apply -f deployment/postgresql-deployment.yaml

# Create PostgreSQL Service
kubectl apply -f deployment/postgresql-service.yaml

# Verify deployment
kubectl get pods
kubectl get svc
```

Wait until the PostgreSQL pod shows `RUNNING` status and `1/1` READY state.

## Step 5: Seed the Database

Set up port forwarding to access the database:

```bash
kubectl port-forward service/postgresql-service 5433:5432 &
```

Install PostgreSQL client (if not already installed):

```bash
# macOS
brew install postgresql

# Linux
apt update
apt install postgresql postgresql-contrib
```

Set database password and run seed files:

```bash
export DB_PASSWORD=mypassword

# Create tables
PGPASSWORD="$DB_PASSWORD" psql --host 127.0.0.1 -U myuser -d mydatabase -p 5433 < db/1_create_tables.sql

# Seed users
PGPASSWORD="$DB_PASSWORD" psql --host 127.0.0.1 -U myuser -d mydatabase -p 5433 < db/2_seed_users.sql

# Seed tokens
PGPASSWORD="$DB_PASSWORD" psql --host 127.0.0.1 -U myuser -d mydatabase -p 5433 < db/3_seed_tokens.sql
```

Verify the data:

```bash
PGPASSWORD="$DB_PASSWORD" psql --host 127.0.0.1 -U myuser -d mydatabase -p 5433

# In psql:
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM tokens;
\q
```

## Step 6: Deploy the Application

### Update Deployment Configuration

Edit `deployment/coworking.yaml` and replace the image placeholder with your ECR URI:

```yaml
image: <YOUR_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/coworking-analytics:latest
```

### Apply Kubernetes Manifests

```bash
# Apply ConfigMap and Secret
kubectl apply -f deployment/configmap.yaml

# Deploy the application
kubectl apply -f deployment/coworking.yaml

# Verify deployment
kubectl get pods
kubectl get svc
kubectl describe deployment coworking
```

Wait for the coworking pod to reach `RUNNING` status. The LoadBalancer service will take a few minutes to provision an external IP.

## Step 7: Verify the Deployment

Check the service external IP:

```bash
kubectl get svc coworking
```

Once the `EXTERNAL-IP` is available (not `<pending>`), test the API endpoints:

```bash
# Replace <EXTERNAL-IP> with the actual LoadBalancer IP
EXTERNAL_IP=$(kubectl get svc coworking -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

# Test health check
curl http://$EXTERNAL_IP:5153/health_check

# Test daily usage report
curl http://$EXTERNAL_IP:5153/api/reports/daily_usage

# Test user visits report
curl http://$EXTERNAL_IP:5153/api/reports/user_visits
```

Expected responses:
- Health check: `ok`
- Reports: JSON data with analytics

## Step 8: Set Up CloudWatch Container Insights

Enable CloudWatch logging for the cluster:

```bash
aws eks update-cluster-config \
  --region us-east-1 \
  --name my-cluster \
  --logging '{"clusterLogging":[{"types":["api","audit","authenticator","controllerManager","scheduler"],"enabled":true}]}'
```

Deploy CloudWatch agent:

```bash
kubectl apply -f deployment/cloudwatch-insights.yaml
```

Update the cluster name in the ConfigMap:

```bash
kubectl edit configmap cwagentconfig -n amazon-cloudwatch
# Replace {{cluster_name}} with your actual cluster name (my-cluster)
```

Verify CloudWatch logs:
1. Navigate to CloudWatch in AWS Console
2. Go to "Log groups"
3. Find `/aws/eks/my-cluster/` log groups
4. Verify application logs are being collected

## Step 9: Capture Screenshots

Follow the instructions in `screenshots/README.md` to capture all required screenshots for project submission:

1. AWS CodeBuild pipeline
2. AWS ECR repository
3. kubectl get svc
4. kubectl get pods
5. kubectl describe svc postgresql-service
6. kubectl describe deployment coworking
7. AWS CloudWatch Container Insights logs

## Troubleshooting

### Pod Not Starting

```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

Common issues:
- Image pull errors: Check ECR permissions and image URI
- Database connection: Verify ConfigMap and Secret values
- Readiness probe failing: Check database connectivity

### Database Connection Issues

```bash
# Verify PostgreSQL service
kubectl get svc postgresql-service

# Check PostgreSQL logs
kubectl logs <postgresql-pod-name>

# Test connection from within cluster
kubectl run -it --rm debug --image=postgres:latest --restart=Never -- \
  psql postgresql://myuser:mypassword@postgresql-service:5432/mydatabase
```

### LoadBalancer Pending

If the external IP remains `<pending>`:
1. Check AWS Load Balancer Controller is installed
2. Verify VPC has available subnets
3. Check CloudFormation for provisioning errors

### Update Environment Variables

If you need to change database credentials or other settings:

```bash
# Edit ConfigMap
kubectl edit configmap coworking-configmap

# Edit Secret (base64 encoded)
kubectl edit secret coworking-secret

# Restart pods to pick up changes
kubectl rollout restart deployment coworking
```

## Cleanup

When finished with the project, clean up resources to avoid charges:

```bash
# Delete application
kubectl delete -f deployment/coworking.yaml
kubectl delete -f deployment/configmap.yaml

# Delete database
kubectl delete -f deployment/postgresql-service.yaml
kubectl delete -f deployment/postgresql-deployment.yaml
kubectl delete -f deployment/pv.yaml
kubectl delete -f deployment/pvc.yaml

# Delete CloudWatch
kubectl delete -f deployment/cloudwatch-insights.yaml

# Delete EKS cluster
eksctl delete cluster --name my-cluster --region us-east-1
```

## Continuous Deployment Workflow

After initial setup, deploy new versions:

1. Make code changes
2. Commit and push to GitHub
3. CodeBuild automatically builds and tags new image
4. Update `deployment/coworking.yaml` with new image tag
5. Apply: `kubectl apply -f deployment/coworking.yaml`
6. Monitor rollout: `kubectl rollout status deployment/coworking`

For rollback:

```bash
kubectl rollout undo deployment/coworking
```

## Additional Resources

- [Amazon EKS Documentation](https://docs.aws.amazon.com/eks/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [AWS CodeBuild Documentation](https://docs.aws.amazon.com/codebuild/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

