# GitHub Actions Workflows

This directory contains the CI/CD pipeline workflows for the Movie Picture Pipeline project.

## Workflows

### 1. frontend-ci.yaml
**Purpose:** Continuous Integration for Frontend
**Triggers:** Pull requests to main, manual dispatch, changes to `starter/frontend/**`
**Jobs:** lint → test → build (parallel lint/test, then build)

### 2. backend-ci.yaml
**Purpose:** Continuous Integration for Backend
**Triggers:** Pull requests to main, manual dispatch, changes to `starter/backend/**`
**Jobs:** lint → test → build (parallel lint/test, then build)

### 3. frontend-cd.yaml
**Purpose:** Continuous Deployment for Frontend
**Triggers:** Push to main, manual dispatch, changes to `starter/frontend/**`
**Jobs:** lint → test → build → deploy
**Deploys to:** AWS EKS cluster via kubectl and kustomize

### 4. backend-cd.yaml
**Purpose:** Continuous Deployment for Backend
**Triggers:** Push to main, manual dispatch, changes to `starter/backend/**`
**Jobs:** lint → test → build → deploy
**Deploys to:** AWS EKS cluster via kubectl and kustomize

## Required GitHub Secrets

| Secret | Description |
|--------|-------------|
| `AWS_ACCESS_KEY_ID` | AWS access key for github-action-user |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key for github-action-user |
| `AWS_ACCOUNT_ID` | AWS account ID (for ECR URLs) |

## Workflow Features

- **Path Filtering:** Workflows only run when relevant code changes
- **Dependency Caching:** npm and pipenv dependencies are cached for faster builds
- **Job Dependencies:** Build only runs if lint and test pass
- **Manual Dispatch:** All workflows can be triggered manually
- **Git SHA Tagging:** Docker images tagged with commit SHA for traceability
- **Parallel Execution:** Lint and test jobs run in parallel

## Testing

See [TESTING_GUIDE.md](../../TESTING_GUIDE.md) for detailed testing instructions.

## Setup

See [CICD_SETUP.md](../../CICD_SETUP.md) for complete setup instructions.

# This forces GitHub to discover workflows
