# CI/CD Pipeline Setup Guide

This document provides step-by-step instructions for setting up the CI/CD pipeline for the Movie Picture Pipeline project using GitHub Actions.

## Prerequisites

Before setting up the CI/CD pipeline, ensure you have:

1. **AWS Account** with appropriate permissions
2. **AWS Infrastructure** deployed via Terraform (EKS cluster, ECR repositories)
3. **GitHub Account** with repository admin access

## AWS Infrastructure Setup

### Step 1: Deploy AWS Resources with Terraform

1. Install and configure Terraform:

```bash
cd setup/terraform
terraform init
terraform apply
```

2. Take note of the Terraform outputs (you can retrieve them anytime with `terraform output`):
   - `frontend_ecr` - Frontend ECR repository URL
   - `backend_ecr` - Backend ECR repository URL
   - `cluster_name` - EKS cluster name
   - `github_action_user_arn` - IAM user ARN for GitHub Actions

### Step 2: Configure GitHub Actions User

Run the initialization script to add the GitHub Actions user to Kubernetes:

```bash
cd setup
./init.sh
```

This script adds the `github-action-user` IAM user to the EKS cluster with appropriate permissions.

### Step 3: Generate AWS Access Keys

1. Go to AWS IAM Console
2. Find the `github-action-user` user
3. Navigate to **Security Credentials** tab
4. Click **Create access key**
5. Select **Application running outside AWS**
6. Save the **Access Key ID** and **Secret Access Key** (you'll need these for GitHub Secrets)

## GitHub Repository Setup

### Step 1: Create GitHub Repository

1. Create a new repository on GitHub (e.g., `movie-picture-pipeline`)
2. Initialize the local repository:

```bash
cd "cd12354-Movie-Picture-Pipeline-main"
git init
git add .
git commit -m "Initial commit with CI/CD workflows"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Step 2: Configure GitHub Secrets

Add the following secrets to your GitHub repository:

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** and add each of the following:

| Secret Name | Description | How to Get It |
|-------------|-------------|---------------|
| `AWS_ACCESS_KEY_ID` | AWS Access Key for github-action-user | From Step 3 of AWS setup |
| `AWS_SECRET_ACCESS_KEY` | AWS Secret Access Key for github-action-user | From Step 3 of AWS setup |
| `AWS_ACCOUNT_ID` | Your AWS Account ID | AWS Console → Account dropdown → Account ID |

**Important**: Never commit AWS credentials to your repository!

## CI/CD Workflows Overview

This project includes four GitHub Actions workflows:

### 1. Frontend Continuous Integration (`frontend-ci.yaml`)

**Triggers:**
- Pull requests to `main` branch
- Manual dispatch
- Changes to `starter/frontend/**`

**Jobs:**
- **Lint**: Runs ESLint to check code quality
- **Test**: Runs unit tests with Jest
- **Build**: Builds Docker image (runs only if lint and test pass)

### 2. Backend Continuous Integration (`backend-ci.yaml`)

**Triggers:**
- Pull requests to `main` branch
- Manual dispatch
- Changes to `starter/backend/**`

**Jobs:**
- **Lint**: Runs Flake8 linter
- **Test**: Runs pytest tests
- **Build**: Builds Docker image (runs only if lint and test pass)

### 3. Frontend Continuous Deployment (`frontend-cd.yaml`)

**Triggers:**
- Push to `main` branch
- Manual dispatch
- Changes to `starter/frontend/**`

**Jobs:**
- **Lint**: Runs ESLint
- **Test**: Runs unit tests
- **Build**: Builds and pushes Docker image to ECR with git SHA tag
- **Deploy**: Deploys to EKS cluster using kubectl and kustomize

### 4. Backend Continuous Deployment (`backend-cd.yaml`)

**Triggers:**
- Push to `main` branch
- Manual dispatch
- Changes to `starter/backend/**`

**Jobs:**
- **Lint**: Runs Flake8 linter
- **Test**: Runs pytest tests
- **Build**: Builds and pushes Docker image to ECR with git SHA tag
- **Deploy**: Deploys to EKS cluster using kubectl and kustomize

## Testing the CI/CD Pipeline

### Test Continuous Integration (CI)

1. Create a new branch:
```bash
git checkout -b test-ci
```

2. Make a small change to the frontend or backend code
3. Commit and push:
```bash
git add .
git commit -m "Test CI pipeline"
git push origin test-ci
```

4. Create a Pull Request on GitHub
5. Verify that the CI workflow runs and all jobs pass

### Test Continuous Deployment (CD)

1. Merge the Pull Request to `main`
2. Verify that the CD workflow runs automatically
3. Check that:
   - Docker images are pushed to ECR with the correct git SHA tag
   - Applications are deployed to the EKS cluster

### Verify Deployment

1. Get the LoadBalancer URLs:
```bash
kubectl get services

# Expected output:
# NAME       TYPE           CLUSTER-IP      EXTERNAL-IP                                                               PORT(S)        AGE
# backend    LoadBalancer   10.100.xxx.xxx  xxx.us-east-1.elb.amazonaws.com   80:xxxxx/TCP   5m
# frontend   LoadBalancer   10.100.xxx.xxx  yyy.us-east-1.elb.amazonaws.com   80:xxxxx/TCP   5m
```

2. Test the backend API:
```bash
curl http://BACKEND_EXTERNAL_IP/movies
```

Expected response:
```json
{"movies":[{"id":"123","title":"Top Gun: Maverick"},{"id":"456","title":"Sonic the Hedgehog"},{"id":"789","title":"A Quiet Place"}]}
```

3. Test the frontend in your browser:
```bash
open http://FRONTEND_EXTERNAL_IP
```

The frontend should display the list of movies retrieved from the backend API.

## Manual Workflow Execution

All workflows support manual execution via the GitHub Actions UI:

1. Go to your repository on GitHub
2. Click **Actions** tab
3. Select the workflow you want to run
4. Click **Run workflow** dropdown
5. Select the branch and click **Run workflow**

## Troubleshooting

### Common Issues

1. **AWS Credentials Error**
   - Verify GitHub Secrets are correctly set
   - Ensure the IAM user has necessary permissions

2. **ECR Push Failed**
   - Check that ECR repositories exist: `frontend` and `backend`
   - Verify AWS credentials have ECR push permissions

3. **Kubernetes Deployment Failed**
   - Verify the EKS cluster is running: `aws eks describe-cluster --name cluster --region us-east-1`
   - Check kubeconfig is correctly configured
   - Ensure github-action-user has been added to the cluster via `init.sh`

4. **Tests Failing**
   - Run tests locally to debug:
     - Frontend: `cd starter/frontend && npm ci && CI=true npm test`
     - Backend: `cd starter/backend && pipenv install && pipenv run test`

5. **Build Failing**
   - Check Dockerfile syntax
   - Verify all dependencies are correctly specified

### View Workflow Logs

1. Go to **Actions** tab in your GitHub repository
2. Click on the workflow run
3. Click on individual jobs to view detailed logs

## Environment Variables

### Frontend
- `REACT_APP_MOVIE_API_URL`: Backend API URL (set to `http://backend:5000` for Kubernetes internal communication)

### Backend
No special environment variables required for basic operation.

## Cleanup

To avoid AWS charges, destroy the infrastructure when done:

```bash
cd setup/terraform
terraform destroy
```

Type `yes` when prompted to confirm destruction of resources.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Repository                        │
│  ┌──────────────────┐        ┌──────────────────┐          │
│  │   Frontend Code  │        │   Backend Code   │          │
│  └────────┬─────────┘        └────────┬─────────┘          │
│           │                           │                      │
└───────────┼───────────────────────────┼──────────────────────┘
            │                           │
            ▼                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Actions                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Frontend  │  │Backend   │  │Frontend  │  │Backend   │   │
│  │CI        │  │CI        │  │CD        │  │CD        │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
└───────┼─────────────┼─────────────┼─────────────┼──────────┘
        │             │             │             │
        ▼             ▼             ▼             ▼
┌─────────────────────────────────────────────────────────────┐
│                   Amazon ECR                                 │
│  ┌──────────────────┐        ┌──────────────────┐          │
│  │frontend:sha      │        │backend:sha       │          │
│  └────────┬─────────┘        └────────┬─────────┘          │
└───────────┼──────────────────────────┼─────────────────────┘
            │                          │
            ▼                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   Amazon EKS Cluster                         │
│  ┌──────────────────┐        ┌──────────────────┐          │
│  │Frontend Pod      │◄───────│Backend Pod       │          │
│  │(React App)       │        │(Flask API)       │          │
│  └────────┬─────────┘        └────────┬─────────┘          │
│           │                           │                      │
│  ┌────────▼─────────┐        ┌────────▼─────────┐          │
│  │Frontend Service  │        │Backend Service   │          │
│  │(LoadBalancer)    │        │(LoadBalancer)    │          │
│  └────────┬─────────┘        └────────┬─────────┘          │
└───────────┼──────────────────────────┼─────────────────────┘
            │                          │
            ▼                          ▼
        External IP               External IP
        (Port 80)                  (Port 80)
```

## Best Practices

1. **Branch Protection**: Enable branch protection rules for `main` branch requiring PR reviews and status checks
2. **Secrets Management**: Rotate AWS access keys regularly
3. **Monitoring**: Set up CloudWatch alarms for EKS cluster and application metrics
4. **Cost Management**: Monitor AWS costs and set up billing alerts
5. **Documentation**: Keep this document updated with any infrastructure changes

## Support

For issues or questions:
- Check workflow logs in GitHub Actions
- Review AWS CloudWatch logs for application issues
- Consult the project rubric for specific requirements

