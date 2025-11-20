# CI/CD Pipeline Deployment Setup Guide

This guide provides step-by-step instructions to set up the CI/CD pipeline for the Movie Picture application using GitHub Actions.

## Overview

The project includes four GitHub Actions workflows:
- **Frontend Continuous Integration** (`frontend-ci.yaml`): Runs on pull requests
- **Backend Continuous Integration** (`backend-ci.yaml`): Runs on pull requests
- **Frontend Continuous Deployment** (`frontend-cd.yaml`): Runs on pushes to main
- **Backend Continuous Deployment** (`backend-cd.yaml`): Runs on pushes to main

## Prerequisites

Before setting up the CI/CD pipeline, ensure you have:

1. AWS account with appropriate permissions (personal account recommended, Udacity voclabs supported)
2. AWS CLI installed and configured
3. kubectl installed
4. Terraform installed (v1.3.9) - use tfenv for version management
5. GitHub account
6. pipenv installed (`pip install pipenv`)
7. kustomize installed (`brew install kustomize`)
8. Docker Desktop or OrbStack installed

## Step 1: Set Up AWS Infrastructure

### Option A: Using Terraform (Recommended)

1. **Install Terraform Environment Manager (tfenv)**
   ```bash
   git clone https://github.com/tfutils/tfenv.git ~/.tfenv
   export PATH="$HOME/.tfenv/bin:$PATH"
   source ~/.bashrc
   tfenv install 1.3.9
   tfenv use 1.3.9
   ```

2. **Create AWS Administrator User**
   - Go to AWS IAM Console
   - Create a new IAM user with AdministratorAccess policy
   - Generate access keys for this user
   - Save the Access Key ID and Secret Access Key

3. **Apply Terraform Configuration**
   ```bash
   cd setup/terraform
   
   # Export AWS credentials
   export AWS_ACCESS_KEY_ID=<your-access-key-id>
   export AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
   
   # Initialize and apply Terraform
   terraform init
   terraform apply
   ```

4. **Save Terraform Outputs**
   After successful terraform apply, save the following outputs:
   ```bash
   terraform output
   ```
   
   You'll need:
   - `frontend_ecr`: ECR repository URL for frontend
   - `backend_ecr`: ECR repository URL for backend
   - `cluster_name`: EKS cluster name (should be "cluster")
   - `github_action_user_arn`: ARN for the GitHub Actions user

### Resources Created by Terraform:
- **VPC** with public and private subnets
- **EKS Cluster** named "cluster"
- **ECR Repositories**: "frontend" and "backend"
- **IAM User**: "github-action-user" for GitHub Actions

## Step 2: Configure Kubernetes for GitHub Actions

Run the init script to add the GitHub Actions IAM user to the Kubernetes cluster:

```bash
cd setup
./init.sh
```

This script:
- Fetches the github-action-user ARN
- Adds the user to the Kubernetes cluster with appropriate permissions
- Grants the user access to deploy applications

## Step 3: Generate AWS Credentials for GitHub Actions

1. **Navigate to IAM Console**
   - Go to AWS Console → IAM → Users
   - Select `github-action-user`

2. **Create Access Keys**
   - Click on "Security credentials" tab
   - Click "Create access key"
   - Select "Application running outside AWS"
   - Click "Create access key"
   - **Save these credentials securely** - you'll need them for GitHub Secrets

## Step 4: Create GitHub Repository

1. **Create a new repository on GitHub**
   - Go to https://github.com/new
   - Create a repository (e.g., "movie-picture-pipeline")
   - Do NOT initialize with README, .gitignore, or license

2. **Push the code to GitHub**
   ```bash
   cd "/Users/shenry/Documents/Personal/Training/Project/Udacity/Cloud DevOps Engineer/Movie Picture Pipeline/cd12354-Movie-Picture-Pipeline-main"
   
   # Initialize git repository
   git init
   
   # Add all files
   git add .
   
   # Create initial commit
   git commit -m "Initial commit: Add CI/CD pipeline workflows"
   
   # Add remote repository
   git remote add origin https://github.com/<your-username>/<your-repo-name>.git
   
   # Push to main branch
   git branch -M main
   git push -u origin main
   ```

## Step 5: Configure GitHub Secrets

1. **Navigate to Repository Settings**
   - Go to your GitHub repository
   - Click "Settings" → "Secrets and variables" → "Actions"

2. **Add the following Repository Secrets:**

   | Secret Name | Value | Description |
   |-------------|-------|-------------|
   | `AWS_ACCESS_KEY_ID` | From Step 3 | Access key for github-action-user |
   | `AWS_SECRET_ACCESS_KEY` | From Step 3 | Secret access key for github-action-user |

   **Note**: The AWS Account ID is automatically extracted from the ECR login process, so you don't need to add it as a separate secret.

3. **Verify Secrets Are Added**
   - All secrets should show in the "Actions secrets" section
   - You won't be able to view the values after creation (this is normal)

## Step 6: Test the CI/CD Pipeline

### Test Continuous Integration (CI)

1. **Create a test branch**
   ```bash
   git checkout -b test-ci-pipeline
   ```

2. **Make a small change** (e.g., update a comment in code)
   ```bash
   # Example: Edit starter/frontend/src/App.js
   echo "// Test CI pipeline" >> starter/frontend/src/App.js
   git add .
   git commit -m "Test: Trigger CI pipeline"
   git push origin test-ci-pipeline
   ```

3. **Create a Pull Request**
   - Go to GitHub repository
   - Click "Pull requests" → "New pull request"
   - Select `test-ci-pipeline` branch
   - Create the pull request

4. **Verify CI Workflows Run**
   - Go to "Actions" tab
   - You should see "Frontend Continuous Integration" or "Backend Continuous Integration" running
   - Check that lint, test, and build jobs complete successfully

### Test Continuous Deployment (CD)

1. **Merge the Pull Request**
   - After CI passes, merge the PR to main branch

2. **Verify CD Workflows Run**
   - Go to "Actions" tab
   - You should see "Frontend Continuous Deployment" or "Backend Continuous Deployment" running
   - Check that lint, test, build, and deploy jobs complete successfully

3. **Verify Deployment to Kubernetes**
   ```bash
   # Update kubeconfig
   aws eks update-kubeconfig --name cluster --region us-east-1
   
   # Check deployments
   kubectl get deployments
   
   # Check pods
   kubectl get pods
   
   # Check services
   kubectl get services
   ```

4. **Access the Application**
   ```bash
   # Get frontend service external IP/hostname
   kubectl get service frontend
   
   # Get backend service external IP/hostname
   kubectl get service backend
   ```
   
   - Frontend LoadBalancer will provide external access on port 80
   - Backend LoadBalancer will provide external access on port 80
   - Wait a few minutes for LoadBalancers to provision

5. **Test the Applications**
   ```bash
   # Test backend API
   curl http://<backend-loadbalancer-url>/movies
   
   # Expected output:
   # {"movies":[{"id":"123","title":"Top Gun: Maverick"},{"id":"456","title":"Sonic the Hedgehog"},{"id":"789","title":"A Quiet Place"}]}
   ```
   
   - Open browser to `http://<frontend-loadbalancer-url>` to see the movie list UI

## Workflow Triggers

### Frontend CI (`frontend-ci.yaml`)
- **Trigger**: Pull requests to `main` branch with changes in `starter/frontend/**`
- **Manual**: Can be triggered manually via "Actions" tab → "Run workflow"
- **Jobs**: lint, test, build (runs in parallel, build needs lint & test)

### Backend CI (`backend-ci.yaml`)
- **Trigger**: Pull requests to `main` branch with changes in `starter/backend/**`
- **Manual**: Can be triggered manually via "Actions" tab → "Run workflow"
- **Jobs**: lint, test, build (runs in parallel, build needs lint & test)

### Frontend CD (`frontend-cd.yaml`)
- **Trigger**: Push to `main` branch with changes in `starter/frontend/**`
- **Manual**: Can be triggered manually via "Actions" tab → "Run workflow"
- **Jobs**: lint, test, build (with ECR push), deploy (to EKS)

### Backend CD (`backend-cd.yaml`)
- **Trigger**: Push to `main` branch with changes in `starter/backend/**`
- **Manual**: Can be triggered manually via "Actions" tab → "Run workflow"
- **Jobs**: lint, test, build (with ECR push), deploy (to EKS)

## Manual Workflow Execution

To manually trigger a workflow:

1. Go to GitHub repository → "Actions" tab
2. Select the workflow you want to run
3. Click "Run workflow" button
4. Select the branch (usually `main`)
5. Click "Run workflow"

## Troubleshooting

### Workflow Fails on AWS Authentication
- Verify GitHub Secrets are correctly set
- Ensure `github-action-user` has appropriate IAM permissions
- Check that `init.sh` script was run to add user to Kubernetes

### Linting Failures
- **Frontend**: Run `npm run lint` locally to see errors
- **Backend**: Run `pipenv run lint` locally to see errors
- Fix linting errors before pushing

### Test Failures
- **Frontend**: Run `CI=true npm test` locally
- **Backend**: Run `pipenv run test` locally
- Ensure all tests pass before creating PR

### Docker Build Failures
- Check Dockerfile syntax
- Ensure all dependencies are available
- Verify build arguments are correctly passed

### Kubernetes Deployment Failures
- Verify kubeconfig is correctly updated
- Check that ECR images were successfully pushed
- Ensure kustomize is properly installed
- Check kubectl logs: `kubectl logs deployment/<deployment-name>`

### ECR Push Failures
- Verify ECR repositories exist: `aws ecr describe-repositories --region us-east-1`
- Ensure IAM user has ECR permissions
- Check ECR login succeeded in workflow logs

## Cleanup

To avoid AWS charges, tear down the infrastructure after completing the project:

```bash
cd setup/terraform
terraform destroy
```

Type `yes` when prompted to confirm destruction of resources.

## Architecture Overview

```
GitHub Repository
    ↓
Pull Request → CI Workflows (lint, test, build)
    ↓
Merge to Main → CD Workflows (lint, test, build, push to ECR, deploy to EKS)
    ↓
AWS EKS Cluster
    ├── Frontend Deployment (React app)
    │   └── LoadBalancer Service (port 80 → 3000)
    └── Backend Deployment (Flask API)
        └── LoadBalancer Service (port 80 → 5000)
```

## Key Features

1. **Parallel Execution**: Lint and test jobs run in parallel for faster feedback
2. **Dependency Management**: Build job only runs after lint and test succeed
3. **Path Filtering**: Workflows only trigger on relevant file changes
4. **Docker Caching**: npm and pipenv dependencies are cached for faster builds
5. **Git SHA Tagging**: Docker images are tagged with commit SHA for traceability
6. **Secure Credentials**: AWS credentials stored as GitHub Secrets
7. **Infrastructure as Code**: Terraform manages all AWS resources
8. **Kubernetes Native**: Uses kustomize for manifest management

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [AWS EKS Documentation](https://docs.aws.amazon.com/eks/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Kustomize Documentation](https://kustomize.io/)

