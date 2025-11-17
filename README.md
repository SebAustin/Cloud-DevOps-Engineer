# Coworking Space Analytics Microservice

## Overview
This microservice provides analytics APIs for the Coworking Space Service, delivering business intelligence on user activity. The application is deployed on AWS EKS using a fully automated CI/CD pipeline that leverages AWS CodeBuild for container image builds and Kubernetes for orchestration. The system tracks coworking space usage patterns and generates reports on daily usage and individual user visits.

## Architecture
The deployment architecture consists of four key AWS services: Amazon EKS hosts the containerized Python Flask application and PostgreSQL database, Amazon ECR stores versioned Docker images, AWS CodeBuild automates the build pipeline, and AWS CloudWatch monitors application logs and metrics. The application connects to a PostgreSQL database running as a Deployment within the same EKS cluster, ensuring low-latency data access.

## Technologies Used
**AWS EKS** provides managed Kubernetes orchestration with auto-scaling and self-healing capabilities. **Docker** containerizes the Python application ensuring consistent environments across development and production. **AWS CodeBuild** automates the CI/CD pipeline, building Docker images and pushing tagged versions to ECR. **PostgreSQL** serves as the relational database with EmptyDir storage for development environments. **CloudWatch Container Insights** provides comprehensive observability into application performance and cluster health. **Python Flask** powers the REST API with scheduled background tasks using APScheduler.

## Deployment Pipeline
Developers commit code changes to the GitHub repository, which can trigger AWS CodeBuild via webhook integration. CodeBuild executes `buildspec.yaml`, building a Docker image from the Dockerfile with the `--platform linux/amd64` flag for EKS compatibility, tagging it with semantic versioning using the build number, and pushing multiple tags (latest, build-number, commit-hash) to Amazon ECR for rollback flexibility. Operators then update the Kubernetes deployment YAML with the new image tag and apply it using kubectl, which triggers a rolling update with zero downtime via health and readiness probes.

## Releasing New Builds
To deploy a new version, developers push code to the repository and trigger the CodeBuild pipeline. Once the build completes successfully and the image appears in ECR, update the `deployment/coworking.yaml` file with the new image tag (e.g., `v1.1`). Apply the updated configuration with `kubectl apply -f deployment/coworking.yaml` which initiates a rolling update, gradually replacing old pods with new ones while maintaining service availability through LoadBalancer routing. Monitor the rollout status with `kubectl rollout status deployment/coworking` and verify pod health using `kubectl get pods`. If issues arise, rollback instantly with `kubectl rollout undo deployment/coworking`.

## AWS Instance Type Recommendation
The **t3.small** instance type (2 vCPUs, 2GB RAM) is recommended for the worker nodes in this deployment. This instance provides sufficient resources for the lightweight Flask application (250m-500m CPU, 256Mi-512Mi memory) and a single PostgreSQL pod, while offering burstable CPU performance ideal for the analytics workload's variable traffic patterns. For production environments with higher traffic or multiple replicas, consider **t3.medium** instances (2 vCPUs, 4GB RAM) to accommodate horizontal scaling and ensure adequate headroom during peak usage periods.

## Cost Optimization Strategies
**Implement cluster auto-scaling** using Kubernetes Cluster Autoscaler to scale nodes based on pod demand, reducing costs during off-peak hours by automatically removing unused nodes. **Use spot instances** for non-critical workloads, offering up to 90% cost savings compared to on-demand instances, though the database should remain on on-demand or reserved instances for stability. **Right-size resources** by monitoring actual CPU and memory usage via CloudWatch Container Insights and adjusting pod resource requests/limits accordingly to prevent over-provisioning. Consider **reserved instances** for predictable baseline capacity, providing up to 75% savings for one or three-year commitments. Finally, implement **pod disruption budgets** and **horizontal pod autoscaling** to optimize resource utilization while maintaining application availability.

## Quick Start

### Prerequisites
- AWS CLI configured with appropriate credentials
- kubectl installed and configured
- Docker installed locally (optional, for local testing)
- An AWS EKS cluster running
- An Amazon ECR repository created

### Database Setup
```bash
# Apply Persistent Volume and Persistent Volume Claim
kubectl apply -f deployment/pvc.yaml
kubectl apply -f deployment/pv.yaml

# Deploy PostgreSQL
kubectl apply -f deployment/postgresql-deployment.yaml
kubectl apply -f deployment/postgresql-service.yaml

# Verify database is running
kubectl get pods

# Port forward to seed the database
kubectl port-forward service/postgresql-service 5433:5432 &

# Run seed files
export DB_PASSWORD=mypassword
PGPASSWORD="$DB_PASSWORD" psql --host 127.0.0.1 -U myuser -d mydatabase -p 5433 < db/1_create_tables.sql
PGPASSWORD="$DB_PASSWORD" psql --host 127.0.0.1 -U myuser -d mydatabase -p 5433 < db/2_seed_users.sql
PGPASSWORD="$DB_PASSWORD" psql --host 127.0.0.1 -U myuser -d mydatabase -p 5433 < db/3_seed_tokens.sql
```

### Application Deployment
```bash
# Apply ConfigMap and Secret
kubectl apply -f deployment/configmap.yaml

# Update the image URI in deployment/coworking.yaml with your ECR repository URI
# Format: <AWS_ACCOUNT_ID>.dkr.ecr.<AWS_REGION>.amazonaws.com/<ECR_REPO_NAME>:<IMAGE_TAG>

# Deploy the application
kubectl apply -f deployment/coworking.yaml

# Verify deployment
kubectl get svc
kubectl get pods

# Access the application (use the EXTERNAL-IP from LoadBalancer)
curl http://<EXTERNAL-IP>:5153/api/reports/daily_usage
curl http://<EXTERNAL-IP>:5153/api/reports/user_visits
```

### CloudWatch Setup
```bash
# Apply CloudWatch Container Insights configuration
kubectl apply -f deployment/cloudwatch-insights.yaml

# Enable control plane logging
aws eks update-cluster-config \
  --region <region> \
  --name <cluster-name> \
  --logging '{"clusterLogging":[{"types":["api","audit","authenticator","controllerManager","scheduler"],"enabled":true}]}'
```

## API Endpoints
- `GET /health_check` - Health check endpoint
- `GET /readiness_check` - Readiness probe endpoint
- `GET /api/reports/daily_usage` - Daily usage statistics
- `GET /api/reports/user_visits` - User visit analytics

## Project Structure
```
.
├── analytics/              # Application source code
│   ├── app.py             # Main Flask application
│   ├── config.py          # Database configuration
│   ├── requirements.txt   # Python dependencies
│   └── Dockerfile         # Container image definition
├── db/                    # Database seed files
├── deployment/            # Kubernetes manifests
│   ├── configmap.yaml    # Environment configuration
│   ├── coworking.yaml    # Application deployment
│   ├── postgresql-*.yaml # Database resources
│   └── cloudwatch-*.yaml # Monitoring configuration
└── buildspec.yaml        # AWS CodeBuild specification
```

## Support
For issues or questions, consult the AWS EKS documentation, Kubernetes documentation, or check CloudWatch logs for application errors.
