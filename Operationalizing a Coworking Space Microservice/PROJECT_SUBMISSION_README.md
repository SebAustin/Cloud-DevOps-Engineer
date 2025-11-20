# Coworking Space Analytics Service - Deployment Documentation

## Overview

This microservice provides business analytics APIs for tracking user activity in a coworking space service. The application is containerized using Docker and deployed to AWS Elastic Kubernetes Service (EKS) with automated CI/CD through AWS CodeBuild. The architecture includes a PostgreSQL database deployed via Helm for data persistence and CloudWatch Container Insights for monitoring and logging.

## Technologies & Tools

- **Docker**: Containerization of the Python Flask application using `python:3.8-slim` base image from AWS ECR Public
- **AWS ECR**: Container image registry for storing Docker images with semantic versioning
- **AWS CodeBuild**: Automated CI/CD pipeline triggered by GitHub commits
- **AWS EKS**: Managed Kubernetes cluster for container orchestration
- **Kubernetes**: Deployment, service, ConfigMap, and Secret management
- **PostgreSQL**: Relational database deployed via Bitnami Helm Chart
- **AWS CloudWatch**: Container Insights for monitoring and log aggregation

## Prerequisites

### Local Tools
- Python 3.8+ (for local development)
- Docker CLI (for building images)
- kubectl (configured for EKS cluster access)
- AWS CLI v2 (configured with IAM credentials)
- Helm 3.x (for PostgreSQL deployment)
- eksctl (for EKS cluster management)

### AWS Resources
- AWS Account with IAM permissions for EKS, ECR, CodeBuild, CloudWatch, and Secrets Manager
- EKS cluster created via eksctl with t3.small nodes
- ECR repository named `coworking`
- CodeBuild project with GitHub source connection
- IAM role for CodeBuild with ECR and Secrets Manager permissions

## Architecture & Deployment Process

### Database Layer

The PostgreSQL database is deployed using the Bitnami Helm Chart within the Kubernetes cluster. The Helm deployment automatically creates a StatefulSet with persistent storage (1Gi gp2 volume), ensuring data persistence across pod restarts. The database is exposed internally via a ClusterIP service named `mypostgres-postgresql` on port 5432, accessible only within the cluster. Default credentials use username `postgres` with a randomly generated password stored in Kubernetes secrets.

### Application Layer

The analytics application runs as a containerized Flask service (Python 3.8) with dedicated health and readiness probes. Health checks (`/health_check`) verify basic application status, while readiness probes (`/readiness_check`) ensure database connectivity before routing traffic. Configuration is separated into ConfigMaps for non-sensitive data (DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_USERNAME) and Secrets for credentials (DB_PASSWORD). The service is exposed externally via an AWS LoadBalancer on port 5153, providing public API access. Resource allocation includes 128Mi-256Mi memory and 250m-500m CPU for stable performance.

### CI/CD Pipeline

AWS CodeBuild automates the Docker image build process triggered by GitHub repository commits. The pipeline executes three phases: pre-build (ECR authentication using `aws ecr get-login-password`), build (Docker image creation with semantic versioning format `1.0.$BUILD_NUMBER`), and post-build (multi-tag push to ECR including latest, version number, and git commit hash). This approach enables version tracking and easy rollbacks. The buildspec.yaml uses environment variables (AWS_ACCOUNT_ID, AWS_DEFAULT_REGION, IMAGE_REPO_NAME) configured in CodeBuild for portability across environments.

## Deploying New Changes

### For Application Code Changes

1. **Commit Changes**: Push code changes to the GitHub repository `main` branch
2. **Automatic Build**: CodeBuild detects the commit via webhook and starts a new build automatically
3. **Image Creation**: Docker image is built from `analytics/` directory and pushed to ECR with tag `1.0.X` where X is the build number
4. **Update Deployment**: Edit `deployment/coworking.yaml` and update the image tag to the new version, or use `latest` for continuous deployment
5. **Apply Changes**: Run `kubectl apply -f deployment/coworking.yaml` to update the deployment
6. **Verify Deployment**: Monitor rollout with `kubectl rollout status deployment/coworking` and check logs using `kubectl logs -l service=coworking --tail=50`

### For Configuration Changes

1. **Update ConfigMap/Secret**: Modify `deployment/configmap.yaml` with new configuration values (e.g., DB_HOST, environment-specific settings)
2. **Apply Configuration**: Run `kubectl apply -f deployment/configmap.yaml` to update the ConfigMap and Secret
3. **Restart Pods**: Execute `kubectl rollout restart deployment/coworking` to gracefully restart pods with new configuration
4. **Verify**: Check application logs with `kubectl logs -l service=coworking` to ensure configuration is loaded correctly without errors

### For Database Changes

1. **Port Forward**: Set up port forwarding using `kubectl port-forward svc/mypostgres-postgresql 5432:5432` to connect from local machine
2. **Get Password**: Retrieve Helm-generated password with `kubectl get secret mypostgres-postgresql -o jsonpath="{.data.postgres-password}" | base64 -d`
3. **Apply SQL Scripts**: Run database migration scripts via `psql -h localhost -U postgres -d postgres -f migration.sql`
4. **Verify Changes**: Connect to database and run `\dt` to list tables or query directly to verify schema/data updates

## Monitoring & Observability

AWS CloudWatch Container Insights collects metrics and logs from the EKS cluster automatically. Application logs are streamed to CloudWatch Log Groups under `/aws/containerinsights/my-cluster/application`. The Flask application includes a background scheduler (APScheduler) that runs health checks every 30 seconds, visible in logs for monitoring application health. Key metrics include pod CPU/memory utilization, container restart counts, and custom application logs showing query results from daily usage reports. CloudWatch dashboards provide visibility into cluster performance and application behavior.

## Resource Allocation & Infrastructure

### CPU and Memory

The application deployment specifies resource requests of 128Mi memory and 250m CPU (quarter of a core), with limits of 256Mi memory and 500m CPU. These conservative values are appropriate for the analytics microservice workload, which primarily performs scheduled database queries (every 30 seconds) and serves API requests for aggregated data. The application does not perform heavy computational tasks, data processing, or large in-memory operations, making these allocations sufficient for stable operation under normal load.

### Recommended AWS Instance Types

**Development/Testing Environment**: t3.small instances (2 vCPU, 2 GiB memory) are recommended for development and testing. They provide burstable CPU performance suitable for low-traffic scenarios and intermittent workloads. With baseline performance credits, t3.small instances handle development testing efficiently while minimizing costs. A single t3.small node can support the coworking application pod plus PostgreSQL with adequate headroom.

**Production Environment**: t3.medium instances (2 vCPU, 4 GiB memory) are recommended for production deployments. They offer double the memory of t3.small, providing better baseline performance and buffer for traffic spikes. For high availability and fault tolerance, deploy a minimum of 2 t3.medium nodes across different availability zones. This configuration ensures the application remains available if one node fails and provides capacity for rolling updates without downtime.

### Cost Optimization Strategies

**Right-Sizing Resources**: Monitor CloudWatch metrics weekly to identify over-provisioned resources. Review actual CPU/memory usage patterns and adjust pod resource requests/limits accordingly. If average CPU usage is consistently below 50% of requests, reduce allocation to optimize node utilization and potentially reduce the number of nodes required.

**Spot Instances for Non-Critical Workloads**: Implement EC2 Spot Instances in the EKS node group for development and testing environments to achieve up to 90% cost savings compared to On-Demand pricing. Spot Instances are suitable for fault-tolerant workloads. For production, consider a mixed node group with 50% On-Demand (for critical pods) and 50% Spot Instances (for scalable worker pods) to balance cost and reliability.

**Horizontal Pod Autoscaling**: Configure Kubernetes Horizontal Pod Autoscaler (HPA) to automatically scale the coworking deployment based on CPU utilization metrics (target 70% CPU). This ensures optimal resource usage by scaling pods up during peak hours (8 AM - 6 PM) when API traffic is highest and scaling down during off-peak hours (nights and weekends) to reduce costs. Set minimum replicas to 1 and maximum to 3 for predictable cost control.

## Key Configuration Details

### Database Connection
- **Service Name**: `mypostgres-postgresql`
- **Port**: 5432
- **Database Name**: `postgres`
- **Username**: `postgres`
- **Password**: Retrieved from Kubernetes secret `mypostgres-postgresql`

### Environment Variables
The application requires these environment variables configured in ConfigMap and Secret:
- `DB_HOST`: mypostgres-postgresql
- `DB_PORT`: "5432"
- `DB_NAME`: postgres
- `DB_USER`: postgres
- `DB_USERNAME`: postgres
- `DB_PASSWORD`: (from secret)

### API Endpoints
- `GET /health_check`: Basic health status
- `GET /readiness_check`: Database connectivity check
- `GET /api/reports/daily_usage`: Daily check-in statistics
- `GET /api/reports/user_visits`: User visit analytics

### Troubleshooting Common Issues

**Pod CrashLoopBackOff**: Check logs with `kubectl logs <pod-name> --previous`. Common causes include missing environment variables or incorrect database credentials.

**Database Connection Failed**: Verify ConfigMap has correct `DB_HOST` (mypostgres-postgresql) and Secret contains valid password matching PostgreSQL secret.

**Readiness Probe Failing**: Ensure PostgreSQL pod is running (`kubectl get pods | grep postgres`) and database is seeded with required tables (users, tokens).

