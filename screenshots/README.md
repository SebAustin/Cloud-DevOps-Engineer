# Screenshots for Project Submission

This directory should contain all required screenshots for the Udacity project submission. Please capture and save the following screenshots here:

## Required Screenshots

### 1. AWS CodeBuild Pipeline
**Filename**: `codebuild_pipeline.png`
- Navigate to AWS CodeBuild in AWS Console
- Open your CodeBuild project
- Show a successful build execution
- Ensure the build number and status are visible

### 2. AWS ECR Repository
**Filename**: `ecr_repository.png`
- Navigate to Amazon ECR in AWS Console
- Open your coworking application repository
- Show the Docker images with semantic versioning tags
- Ensure multiple tags are visible (e.g., latest, 1.0.X, commit hash)

### 3. Kubectl Get Services
**Filename**: `kubectl_get_svc.png`
- Run: `kubectl get svc`
- Capture the output showing:
  - coworking service with LoadBalancer type
  - postgresql-service
  - External IP addresses
  - Port mappings

### 4. Kubectl Get Pods
**Filename**: `kubectl_get_pods.png`
- Run: `kubectl get pods`
- Capture the output showing:
  - All pods in RUNNING state
  - READY status (e.g., 1/1)
  - No restarts or minimal restarts
  - Pod age

### 5. Kubectl Describe Database Service
**Filename**: `kubectl_describe_svc_postgresql.png`
- Run: `kubectl describe svc postgresql-service`
- Capture the full output showing:
  - Service name and namespace
  - Labels and selectors
  - Type and IP addresses
  - Port configurations
  - Endpoints

### 6. Kubectl Describe Deployment
**Filename**: `kubectl_describe_deployment_coworking.png`
- Run: `kubectl describe deployment coworking`
- Capture the full output showing:
  - Deployment name and namespace
  - Replicas status
  - Pod template details
  - Container image from ECR
  - Environment variables (ConfigMap and Secret references)
  - Resource limits and requests
  - Conditions and events

### 7. AWS CloudWatch Container Insights Logs
**Filename**: `cloudwatch_logs.png`
- Navigate to AWS CloudWatch in AWS Console
- Go to Container Insights or Log Groups
- Show logs for the coworking application
- Ensure application logs are visible (periodic health status checks)
- Show that application is running without errors

## Screenshot Guidelines

- Use PNG or JPG format
- Ensure screenshots are clear and readable
- Capture full window when possible
- Include timestamps where applicable
- Ensure no sensitive information (passwords, keys) is visible
- Screenshots should demonstrate successful deployment and operation

## Verification Checklist

Before submitting, verify that:
- [ ] All 7 screenshots are present in this directory
- [ ] File names match the recommendations above
- [ ] Screenshots clearly show the requested information
- [ ] Images are readable and high quality
- [ ] No sensitive credentials are exposed
- [ ] Timestamps and version numbers are visible
- [ ] All services and pods show healthy/running status

