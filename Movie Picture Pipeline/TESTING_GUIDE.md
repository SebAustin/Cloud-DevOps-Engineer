# CI/CD Pipeline Testing Guide

This guide provides detailed instructions for testing the CI/CD pipeline workflows.

## Prerequisites

Before testing, ensure you have completed all steps in `DEPLOYMENT_SETUP.md`:
- ✅ AWS infrastructure is set up (EKS cluster, ECR repositories)
- ✅ GitHub repository is created and code is pushed
- ✅ GitHub Secrets are configured
- ✅ Kubernetes is configured for GitHub Actions user

## Testing Strategy

The testing process is divided into four phases:
1. **Local Validation** - Test build and deployment commands locally
2. **CI Workflow Testing** - Test Continuous Integration on pull requests
3. **CD Workflow Testing** - Test Continuous Deployment on main branch
4. **Application Verification** - Verify the deployed application works correctly

---

## Phase 1: Local Validation

Before pushing to GitHub, validate that the application builds and tests pass locally.

### Frontend Local Validation

```bash
cd starter/frontend

# Install dependencies
npm ci

# Run linting
npm run lint
# Expected: No errors

# Run tests
CI=true npm test
# Expected: All tests pass

# Build Docker image
docker build --build-arg=REACT_APP_MOVIE_API_URL=http://localhost:5000 --tag=mp-frontend:latest .
# Expected: Image builds successfully

# Verify image exists
docker images | grep mp-frontend
```

### Backend Local Validation

```bash
cd starter/backend

# Install pipenv if not already installed
pip install pipenv

# Install dependencies
pipenv install --dev

# Run linting
pipenv run lint
# Expected: No errors (no output means success)

# Run tests
pipenv run test
# Expected: All 3 tests pass

# Build Docker image
docker build --tag=mp-backend:latest .
# Expected: Image builds successfully

# Verify image exists
docker images | grep mp-backend
```

---

## Phase 2: CI Workflow Testing

Test the Continuous Integration workflows by creating pull requests.

### Test Frontend CI

1. **Create a test branch**
   ```bash
   git checkout -b test-frontend-ci
   ```

2. **Make a small change to frontend**
   ```bash
   # Add a comment to trigger the workflow
   echo "// CI Pipeline Test" >> starter/frontend/src/App.js
   git add starter/frontend/src/App.js
   git commit -m "test: trigger frontend CI pipeline"
   git push origin test-frontend-ci
   ```

3. **Create Pull Request**
   - Go to GitHub repository
   - Click "Pull requests" → "New pull request"
   - Base: `main`, Compare: `test-frontend-ci`
   - Click "Create pull request"

4. **Monitor Workflow Execution**
   - Go to "Actions" tab
   - Click on "Frontend Continuous Integration" workflow
   - Verify all jobs complete:
     - ✅ lint (should pass)
     - ✅ test (should pass)
     - ✅ build (should pass after lint and test)

5. **Check Workflow Details**
   - Click on each job to see detailed logs
   - Verify:
     - Dependencies are cached
     - Linting produces no errors
     - All tests pass
     - Docker image builds successfully

6. **Expected Results**
   - All three jobs (lint, test, build) should show green checkmarks
   - Total workflow time: ~3-5 minutes
   - Pull request shows "All checks have passed"

### Test Backend CI

1. **Create a test branch**
   ```bash
   git checkout main
   git pull origin main
   git checkout -b test-backend-ci
   ```

2. **Make a small change to backend**
   ```bash
   # Add a comment to trigger the workflow
   echo "# CI Pipeline Test" >> starter/backend/test_app.py
   git add starter/backend/test_app.py
   git commit -m "test: trigger backend CI pipeline"
   git push origin test-backend-ci
   ```

3. **Create Pull Request**
   - Go to GitHub repository
   - Click "Pull requests" → "New pull request"
   - Base: `main`, Compare: `test-backend-ci`
   - Click "Create pull request"

4. **Monitor Workflow Execution**
   - Go to "Actions" tab
   - Click on "Backend Continuous Integration" workflow
   - Verify all jobs complete:
     - ✅ lint (should pass)
     - ✅ test (should pass)
     - ✅ build (should pass after lint and test)

5. **Expected Results**
   - All three jobs should show green checkmarks
   - Total workflow time: ~3-5 minutes
   - Pull request shows "All checks have passed"

### Test CI Failure Scenarios

It's important to verify that the CI pipeline correctly catches errors.

#### Test Linting Failure (Frontend)

1. **Introduce a linting error**
   ```bash
   git checkout -b test-frontend-lint-fail
   
   # Add code with linting issues (e.g., unused variable)
   echo "const unusedVar = 'test';" >> starter/frontend/src/App.js
   
   git add starter/frontend/src/App.js
   git commit -m "test: introduce linting error"
   git push origin test-frontend-lint-fail
   ```

2. **Create PR and verify lint job fails**
   - Lint job should show red X
   - Build job should be skipped
   - PR should show "Some checks were not successful"

3. **Fix the issue**
   ```bash
   # Remove the bad code
   git checkout starter/frontend/src/App.js
   git add starter/frontend/src/App.js
   git commit -m "fix: remove linting error"
   git push origin test-frontend-lint-fail
   ```

4. **Verify workflow now passes**

#### Test Test Failure (Backend)

1. **Introduce a test failure**
   ```bash
   git checkout main
   git checkout -b test-backend-test-fail
   
   # Modify backend code to break a test
   # Edit starter/backend/movies/resources.py and change the movie data
   ```

2. **Create PR and verify test job fails**
   - Test job should fail
   - Build job should be skipped

3. **Revert and verify it passes again**

---

## Phase 3: CD Workflow Testing

Test the Continuous Deployment workflows by merging to main branch.

### Test Frontend CD

1. **Merge the Frontend CI test PR**
   - Go to the `test-frontend-ci` pull request
   - Click "Merge pull request" → "Confirm merge"
   - Delete the branch if prompted

2. **Monitor CD Workflow**
   - Go to "Actions" tab
   - Click on "Frontend Continuous Deployment" workflow
   - Verify all jobs complete:
     - ✅ lint
     - ✅ test
     - ✅ build (with ECR push)
     - ✅ deploy (to Kubernetes)

3. **Check Build Job Details**
   - Click on "build" job
   - Verify steps:
     - ✅ AWS credentials configured
     - ✅ ECR login successful
     - ✅ Docker image built with correct build arg
     - ✅ Image tagged with git SHA
     - ✅ Image pushed to ECR

4. **Check Deploy Job Details**
   - Click on "deploy" job
   - Verify steps:
     - ✅ Kubeconfig updated
     - ✅ Kustomize installed
     - ✅ Image reference updated
     - ✅ Kubernetes manifests applied

5. **Verify ECR Image**
   ```bash
   # List images in ECR
   aws ecr describe-images --repository-name frontend --region us-east-1
   
   # Expected: Should see image tagged with the git SHA
   ```

6. **Expected Results**
   - All jobs show green checkmarks
   - Total workflow time: ~5-8 minutes
   - Docker image pushed to ECR
   - Kubernetes deployment updated

### Test Backend CD

1. **Merge the Backend CI test PR**
   - Go to the `test-backend-ci` pull request
   - Click "Merge pull request" → "Confirm merge"

2. **Monitor CD Workflow**
   - Go to "Actions" tab
   - Click on "Backend Continuous Deployment" workflow
   - Verify all jobs complete successfully

3. **Verify ECR Image**
   ```bash
   aws ecr describe-images --repository-name backend --region us-east-1
   ```

4. **Expected Results**
   - All jobs pass
   - Docker image in ECR
   - Kubernetes deployment updated

---

## Phase 4: Application Verification

Verify that the deployed applications are working correctly in Kubernetes.

### Check Kubernetes Resources

```bash
# Update kubeconfig
aws eks update-kubeconfig --name cluster --region us-east-1

# Check all resources
kubectl get all

# Check deployments
kubectl get deployments
# Expected: frontend and backend deployments with READY 1/1

# Check pods
kubectl get pods
# Expected: frontend and backend pods in Running state

# Check services
kubectl get services
# Expected: frontend and backend services with EXTERNAL-IP
```

### Verify Backend API

1. **Get backend service URL**
   ```bash
   kubectl get service backend
   # Note the EXTERNAL-IP (may take a few minutes to provision)
   ```

2. **Test backend endpoint**
   ```bash
   # Wait for LoadBalancer to be ready (check EXTERNAL-IP is not <pending>)
   
   # Test the API
   curl http://<BACKEND-EXTERNAL-IP>/movies
   
   # Expected output:
   # {"movies":[{"id":"123","title":"Top Gun: Maverick"},{"id":"456","title":"Sonic the Hedgehog"},{"id":"789","title":"A Quiet Place"}]}
   ```

3. **Verify JSON response**
   ```bash
   curl http://<BACKEND-EXTERNAL-IP>/movies | jq
   # Should show formatted JSON with 3 movies
   ```

### Verify Frontend Application

1. **Get frontend service URL**
   ```bash
   kubectl get service frontend
   # Note the EXTERNAL-IP
   ```

2. **Test frontend in browser**
   - Open browser to `http://<FRONTEND-EXTERNAL-IP>`
   - Expected: Movie Picture Pipeline UI loads
   - Should display list of 3 movies from the backend API

3. **Verify frontend is calling backend**
   - Open browser developer tools (F12)
   - Go to Network tab
   - Refresh the page
   - Look for API call to backend
   - Should see successful request to backend service

4. **Visual Verification Checklist**
   - ✅ Page loads without errors
   - ✅ Movie list is displayed
   - ✅ All 3 movies are visible:
     - Top Gun: Maverick
     - Sonic the Hedgehog
     - A Quiet Place
   - ✅ No console errors in browser

### Verify Pod Logs

```bash
# Check frontend logs
kubectl logs deployment/frontend
# Expected: Server logs showing app running

# Check backend logs
kubectl logs deployment/backend
# Expected: Flask app logs

# Follow logs in real-time
kubectl logs -f deployment/backend
```

### Check Pod Health

```bash
# Describe frontend pod
kubectl describe pod -l app=frontend

# Describe backend pod
kubectl describe pod -l app=backend

# Check for issues:
# - Pod should be in Running state
# - No restart count (or very low)
# - Events should show successful image pull and start
```

---

## Testing Manual Workflow Triggers

Test that workflows can be manually triggered.

### Manually Trigger Frontend CD

1. Go to GitHub → Actions → "Frontend Continuous Deployment"
2. Click "Run workflow"
3. Select branch: `main`
4. Click "Run workflow"
5. Verify workflow runs successfully

### Manually Trigger Backend CD

1. Go to GitHub → Actions → "Backend Continuous Deployment"
2. Click "Run workflow"
3. Select branch: `main`
4. Click "Run workflow"
5. Verify workflow runs successfully

---

## Testing Path Filters

Verify that workflows only trigger on relevant file changes.

### Test Frontend Path Filter

```bash
# Make a change to ONLY backend files
git checkout -b test-path-filter
echo "# test" >> starter/backend/README.md
git add starter/backend/README.md
git commit -m "test: change backend only"
git push origin test-path-filter
```

- Create PR
- Expected: Only "Backend Continuous Integration" runs
- Frontend workflow should NOT trigger

### Test Backend Path Filter

```bash
# Make a change to ONLY frontend files
echo "// test" >> starter/frontend/src/index.js
git add starter/frontend/src/index.js
git commit -m "test: change frontend only"
git push origin test-path-filter
```

- Expected: Only "Frontend Continuous Integration" runs on this commit
- Backend workflow should NOT trigger

---

## Performance Testing

### CI Pipeline Performance Targets

| Workflow | Expected Time | With Cache |
|----------|--------------|------------|
| Frontend CI | 3-5 minutes | 2-3 minutes |
| Backend CI | 3-5 minutes | 2-3 minutes |
| Frontend CD | 6-8 minutes | 4-6 minutes |
| Backend CD | 6-8 minutes | 4-6 minutes |

### Cache Effectiveness

After the first workflow run, subsequent runs should be faster due to caching:

```bash
# Check workflow run times
# Go to Actions → Select a workflow → Compare run times
```

- First run: Dependencies downloaded
- Second run: Dependencies restored from cache
- Cache hit should show: "Cache restored successfully"

---

## Troubleshooting Common Issues

### Issue: Workflow doesn't trigger

**Symptoms**: No workflow runs after creating PR

**Solutions**:
1. Check file paths - workflow only triggers on specific paths
2. Verify `.github/workflows/*.yaml` files are in main branch
3. Check branch name is exactly `main` (not `master`)

### Issue: ECR login fails

**Symptoms**: "Error: Cannot perform an interactive login from a non TTY device"

**Solutions**:
1. Verify AWS credentials are set in GitHub Secrets
2. Check IAM user has ECR permissions
3. Verify `aws-actions/amazon-ecr-login@v2` action version

### Issue: Kubernetes deployment fails

**Symptoms**: "error: You must be logged in to the server"

**Solutions**:
1. Verify `init.sh` was run to add user to Kubernetes
2. Check IAM user has EKS permissions
3. Verify cluster name is correct: "cluster"

### Issue: Tests fail in CI but pass locally

**Symptoms**: Tests pass with `npm test` but fail in CI

**Solutions**:
1. Use `CI=true npm test` locally to simulate CI environment
2. Check for timing issues or race conditions
3. Verify all dependencies are in package.json

### Issue: Frontend can't reach backend

**Symptoms**: Frontend loads but shows no movies

**Solutions**:
1. Verify backend service is running: `kubectl get svc backend`
2. Check backend logs: `kubectl logs deployment/backend`
3. Verify REACT_APP_MOVIE_API_URL build arg is correct
4. In Kubernetes, frontend should use: `http://backend:5000`

---

## Success Criteria Checklist

Use this checklist to verify complete implementation:

### CI Workflows
- ✅ Frontend CI workflow file exists
- ✅ Backend CI workflow file exists
- ✅ CI triggers on pull requests to main
- ✅ CI triggers only on relevant path changes
- ✅ Lint jobs run and pass
- ✅ Test jobs run and pass
- ✅ Lint and test run in parallel
- ✅ Build job requires lint and test to pass
- ✅ Build job successfully builds Docker image
- ✅ Failed tests prevent build job from running
- ✅ Workflows can be manually triggered

### CD Workflows
- ✅ Frontend CD workflow file exists
- ✅ Backend CD workflow file exists
- ✅ CD triggers on push to main
- ✅ CD triggers only on relevant path changes
- ✅ AWS credentials configured from GitHub Secrets
- ✅ ECR login successful
- ✅ Docker images tagged with git SHA
- ✅ Images successfully pushed to ECR
- ✅ Kubeconfig updated correctly
- ✅ Kustomize installed and runs successfully
- ✅ Kubernetes manifests applied
- ✅ Deployments updated with new images
- ✅ Workflows can be manually triggered

### Infrastructure & Deployment
- ✅ EKS cluster is running
- ✅ ECR repositories exist
- ✅ Frontend and backend pods are running
- ✅ LoadBalancer services are provisioned
- ✅ Backend API returns movie list
- ✅ Frontend UI displays movies
- ✅ Frontend successfully calls backend
- ✅ No AWS credentials in workflow files (only in secrets)

### Documentation
- ✅ Setup documentation is complete
- ✅ Testing guide is comprehensive
- ✅ Troubleshooting section included
- ✅ All commands tested and verified

---

## Submitting for Review

Before submitting your project, ensure:

1. **All workflows are passing**
   - Screenshot or URL of successful workflow runs

2. **Application is deployed and working**
   - Screenshot or URL of frontend showing movie list
   - Screenshot or URL of backend API response

3. **Repository is accessible**
   - Make repository public or add reviewers
   - Include link to repository in submission

4. **Documentation is complete**
   - README explains the project
   - DEPLOYMENT_SETUP.md provides setup instructions
   - All workflow files are properly commented

---

## Cleanup After Testing

To avoid AWS charges after completing the project:

```bash
# Delete Kubernetes resources
kubectl delete all --all

# Destroy AWS infrastructure
cd setup/terraform
terraform destroy
# Type 'yes' to confirm

# Expected: All AWS resources deleted
# - EKS cluster
# - ECR repositories  
# - VPC and networking
# - IAM users and roles
```

Verify cleanup:
```bash
# Check ECR repositories
aws ecr describe-repositories --region us-east-1

# Check EKS clusters
aws eks list-clusters --region us-east-1

# Expected: No resources found
```
