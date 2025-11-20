# 📋 Project Submission Checklist

Use this checklist to ensure your project is ready for submission to Udacity.

---

## ✅ Required Deliverables

### 1. GitHub Repository Link
- [ ] Repository is public (or reviewers have access)
- [ ] All code is pushed to the `main` branch
- [ ] Repository is clean (no unnecessary files)

**Submission Format:**
```
https://github.com/YOUR_USERNAME/YOUR_REPO_NAME
```

### 2. Workflow Files (Required)
- [ ] `.github/workflows/frontend-ci.yaml` exists and is functional
- [ ] `.github/workflows/backend-ci.yaml` exists and is functional
- [ ] `.github/workflows/frontend-cd.yaml` exists and is functional
- [ ] `.github/workflows/backend-cd.yaml` exists and is functional

### 3. Evidence of Working Application

#### Frontend Evidence
- [ ] Screenshot OR URL showing frontend application
- [ ] Must display the list of movies:
  - "Top Gun: Maverick"
  - "Sonic the Hedgehog"
  - "A Quiet Place"
- [ ] UI is functional and loads without errors

#### Backend Evidence
- [ ] Screenshot OR URL showing backend API response
- [ ] Must show JSON response from `/movies` endpoint
- [ ] Response must contain all 3 movies with correct structure

### 4. Workflow Execution Evidence
- [ ] Screenshot of successful workflow runs in GitHub Actions
- [ ] All 4 workflows show green checkmarks (passing)
- [ ] Lint, test, build, and deploy steps all passing

---

## 📸 Required Screenshots

### Screenshot 1: GitHub Actions - All Workflows Passing
**What to capture:**
- Go to: `https://github.com/YOUR_USERNAME/YOUR_REPO/actions`
- Show all 4 workflows with green checkmarks
- Include timestamps

**File Name:** `workflows-passing.png`

### Screenshot 2: Frontend Application
**What to capture:**
- Browser showing the frontend application
- URL visible in address bar
- Movie list visible with all 3 movies

**File Name:** `frontend-working.png`

**Alternative:** Provide LoadBalancer URL:
```bash
kubectl get service frontend -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'
```

### Screenshot 3: Backend API Response
**What to capture:**
- Terminal or browser showing API response
- Full JSON output visible
- Or use Postman/Insomnia screenshot

**File Name:** `backend-working.png`

**Command to get response:**
```bash
curl http://<BACKEND-URL>/movies
```

### Screenshot 4: Kubernetes Deployments (Optional but Recommended)
**What to capture:**
```bash
kubectl get all
```
Show running pods, services, and deployments

**File Name:** `kubernetes-deployed.png`

---

## 🔍 Pre-Submission Verification

### GitHub Repository Checks

```bash
# 1. Verify all workflow files exist
ls -la .github/workflows/
# Should show:
# - frontend-ci.yaml
# - backend-ci.yaml
# - frontend-cd.yaml
# - backend-cd.yaml

# 2. Verify no sensitive data in code
grep -r "AWS_ACCESS_KEY_ID\|AWS_SECRET_ACCESS_KEY" .github/
# Should return ONLY references to secrets, never actual values

# 3. Check git status
git status
# Should be clean or show only intended changes
```

### AWS Infrastructure Checks

```bash
# 1. Verify EKS cluster exists
aws eks list-clusters --region us-east-1

# 2. Verify ECR repositories exist
aws ecr describe-repositories --region us-east-1

# 3. Verify kubectl access
kubectl cluster-info
kubectl get nodes

# 4. Verify deployments are running
kubectl get deployments
# Both frontend and backend should show READY 1/1

# 5. Verify pods are running
kubectl get pods
# All pods should show STATUS: Running

# 6. Verify services have external IPs
kubectl get services
# Both services should have EXTERNAL-IP (not <pending>)
```

### Application Functionality Checks

```bash
# 1. Get service URLs
FRONTEND_URL=$(kubectl get service frontend -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
BACKEND_URL=$(kubectl get service backend -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

echo "Frontend: http://$FRONTEND_URL"
echo "Backend: http://$BACKEND_URL/movies"

# 2. Test backend API
curl http://$BACKEND_URL/movies | jq

# Expected output:
# {
#   "movies": [
#     {"id": "123", "title": "Top Gun: Maverick"},
#     {"id": "456", "title": "Sonic the Hedgehog"},
#     {"id": "789", "title": "A Quiet Place"}
#   ]
# }

# 3. Test frontend (in browser)
open http://$FRONTEND_URL
# Should display the movie list
```

### GitHub Actions Checks

```bash
# Using GitHub CLI (optional)
gh run list --limit 10

# Check latest run status
gh run view

# Or manually:
# Go to: https://github.com/YOUR_USERNAME/YOUR_REPO/actions
# Verify all workflows show green checkmarks
```

---

## 📝 Submission Format

### Option 1: Text Submission with Screenshots

```
GitHub Repository URL:
https://github.com/YOUR_USERNAME/movie-picture-pipeline

Frontend Application URL:
http://YOUR-FRONTEND-LB-URL

Backend API URL:
http://YOUR-BACKEND-LB-URL/movies

Attached Screenshots:
1. workflows-passing.png - All GitHub Actions workflows passing
2. frontend-working.png - Frontend displaying movies
3. backend-working.png - Backend API JSON response
4. kubernetes-deployed.png - Kubernetes resources (optional)

Notes:
- All workflows are passing
- Applications deployed to EKS cluster
- Using Udacity voclabs credentials (expire after session)
```

### Option 2: Text Submission with Working URLs

```
GitHub Repository URL:
https://github.com/YOUR_USERNAME/movie-picture-pipeline

Frontend Application:
http://a1b2c3d4.us-east-1.elb.amazonaws.com
(Load in browser to see movie list)

Backend API:
http://e5f6g7h8.us-east-1.elb.amazonaws.com/movies
(Returns JSON with 3 movies)

GitHub Actions:
https://github.com/YOUR_USERNAME/movie-picture-pipeline/actions
(All 4 workflows passing)

Notes:
- Infrastructure deployed using Terraform
- CI/CD pipelines fully automated
- All tests passing
```

---

## 🎯 Rubric Requirements Checklist

### Frontend CI (frontend-ci.yaml)
- [ ] Workflow file exists at `.github/workflows/frontend-ci.yaml`
- [ ] Named "Frontend Continuous Integration"
- [ ] Triggers on pull_request to main
- [ ] Triggers on workflow_dispatch (manual)
- [ ] Path filter: `starter/frontend/**`
- [ ] Lint job exists and passes
- [ ] Test job exists and passes
- [ ] Lint and test run in parallel
- [ ] Build job exists and passes
- [ ] Build job depends on lint and test (uses `needs`)
- [ ] Build step uses Docker
- [ ] Build uses `--build-arg` for `REACT_APP_MOVIE_API_URL`

### Backend CI (backend-ci.yaml)
- [ ] Workflow file exists at `.github/workflows/backend-ci.yaml`
- [ ] Named "Backend Continuous Integration"
- [ ] Triggers on pull_request to main
- [ ] Triggers on workflow_dispatch (manual)
- [ ] Path filter: `starter/backend/**`
- [ ] Lint job exists and passes
- [ ] Test job exists and passes
- [ ] Lint and test run in parallel
- [ ] Build job exists and passes
- [ ] Build job depends on lint and test (uses `needs`)
- [ ] Build step uses Docker

### Frontend CD (frontend-cd.yaml)
- [ ] Workflow file exists at `.github/workflows/frontend-cd.yaml`
- [ ] Named "Frontend Continuous Deployment"
- [ ] Triggers on push to main
- [ ] Triggers on workflow_dispatch (manual)
- [ ] Path filter: `starter/frontend/**`
- [ ] Lint job exists and passes
- [ ] Test job exists and passes
- [ ] Build job uses `aws-actions/amazon-ecr-login`
- [ ] Build job accesses GitHub Secrets for AWS credentials
- [ ] Build step uses `--build-arg` for `REACT_APP_MOVIE_API_URL`
- [ ] Docker image tagged with git SHA
- [ ] Image pushed to ECR
- [ ] Deploy job uses kubectl
- [ ] Application successfully deployed to EKS

### Backend CD (backend-cd.yaml)
- [ ] Workflow file exists at `.github/workflows/backend-cd.yaml`
- [ ] Named "Backend Continuous Deployment"
- [ ] Triggers on push to main
- [ ] Triggers on workflow_dispatch (manual)
- [ ] Path filter: `starter/backend/**`
- [ ] Lint job exists and passes
- [ ] Test job exists and passes
- [ ] Build job uses `aws-actions/amazon-ecr-login`
- [ ] Build job accesses GitHub Secrets for AWS credentials
- [ ] Docker image tagged with git SHA
- [ ] Image pushed to ECR
- [ ] Deploy job uses kubectl
- [ ] Application successfully deployed to EKS

### Security
- [ ] NO AWS credentials hardcoded in workflow files
- [ ] All AWS credentials referenced via GitHub Secrets only
- [ ] No sensitive data committed to repository

### Functionality
- [ ] All workflows run without errors
- [ ] All tests pass (no failing tests)
- [ ] Docker images successfully pushed to ECR
- [ ] Applications running on EKS cluster
- [ ] Frontend displays movie list correctly
- [ ] Backend API returns correct JSON response
- [ ] Failed tests prevent deployment (CI gates work)

---

## 🚨 Common Submission Mistakes to Avoid

### ❌ FAIL Conditions

1. **AWS credentials in workflow files**
   - Check: `grep -r "AKIA" .github/` should return nothing
   - Use GitHub Secrets only

2. **Workflows passing despite test failures**
   - Test by introducing a failing test
   - Workflow should fail and prevent merge/deployment

3. **Workflows not running**
   - Check workflow syntax
   - Verify triggers are correct
   - Ensure path filters match file changes

4. **Applications not deployed**
   - Check `kubectl get pods` - should show Running
   - Check `kubectl get services` - should have EXTERNAL-IP
   - Verify frontend displays movies
   - Verify backend returns JSON

5. **Missing workflow files**
   - All 4 files must exist in `.github/workflows/`
   - Names must match requirements exactly

6. **Repository not accessible**
   - Make repository public OR
   - Add reviewers as collaborators

---

## 🧪 Final Test Before Submission

Run this complete test sequence:

```bash
# 1. Create a test branch
git checkout -b test-submission

# 2. Make a small change to trigger CI
echo "# Test" >> starter/frontend/README.md
git add .
git commit -m "test: verify CI pipeline"
git push origin test-submission

# 3. Create pull request on GitHub
# - CI workflows should run automatically
# - Verify all checks pass

# 4. Merge pull request
# - CD workflows should run automatically
# - Verify deployment succeeds

# 5. Verify application
kubectl get all
# - Check pods are running
# - Check services have EXTERNAL-IPs

# 6. Test frontend
FRONTEND_URL=$(kubectl get service frontend -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
open http://$FRONTEND_URL
# - Should see movie list

# 7. Test backend
BACKEND_URL=$(kubectl get service backend -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
curl http://$BACKEND_URL/movies | jq
# - Should see JSON with 3 movies

# 8. Take screenshots
# - GitHub Actions page
# - Frontend application
# - Backend API response

# 9. Prepare submission text
# - Repository URL
# - Application URLs or screenshots
# - Brief notes
```

---

## 📤 Submission Steps

### Step 1: Verify Everything Works
- [ ] Run final test sequence above
- [ ] All checks passing
- [ ] Applications working

### Step 2: Prepare Submission Materials
- [ ] GitHub repository URL
- [ ] Screenshots captured (3-4 screenshots)
- [ ] Application URLs (if services still running)
- [ ] Brief notes written

### Step 3: Submit to Udacity
- [ ] Go to Udacity project submission page
- [ ] Paste GitHub repository URL
- [ ] Upload screenshots OR provide URLs
- [ ] Add any relevant notes
- [ ] Click Submit

### Step 4: After Submission
- [ ] Keep AWS infrastructure running until graded
- [ ] Ensure voclabs credentials don't expire during grading
- [ ] Monitor for reviewer feedback
- [ ] Be ready to update GitHub Secrets if credentials expire

---

## 💰 Cost Management

**Important**: AWS resources cost money!

### During Grading
- ✅ Keep infrastructure running
- ✅ Keep applications deployed
- ✅ Ensure services are accessible

### After Approval
```bash
# Destroy all AWS resources
cd setup/terraform
terraform destroy
# Type 'yes' to confirm

# Verify cleanup
aws eks list-clusters --region us-east-1
aws ecr describe-repositories --region us-east-1
# Both should return empty or no resources
```

**Estimated cost while running**: ~$4/day (~$120/month)

---

## 🎓 For Udacity Voclabs Users

### Special Considerations

1. **Credential Expiration**
   - Voclabs credentials expire after lab session
   - Update GitHub Secrets before each test
   - Ensure credentials are fresh during grading

2. **Starting New Lab Session**
   ```bash
   # Export new credentials
   export AWS_ACCESS_KEY_ID=<new-key>
   export AWS_SECRET_ACCESS_KEY=<new-secret>
   
   # Update GitHub Secrets
   # Go to: Settings → Secrets and variables → Actions
   # Update both AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
   
   # Verify access
   aws eks update-kubeconfig --name cluster --region us-east-1
   kubectl get pods
   ```

3. **For Grading**
   - Inform reviewer that you're using voclabs credentials
   - Note that infrastructure may need fresh credentials
   - Provide timing for when credentials will be valid

---

## ✅ Final Checklist

Before clicking Submit:

- [ ] GitHub repository is public and accessible
- [ ] All 4 workflow files exist and are properly named
- [ ] All workflows showing green checkmarks
- [ ] AWS infrastructure deployed (EKS, ECR)
- [ ] Applications running on Kubernetes
- [ ] Frontend displays movies correctly
- [ ] Backend API returns correct JSON
- [ ] Screenshots captured or URLs ready
- [ ] No AWS credentials in code
- [ ] GitHub Secrets configured correctly
- [ ] Documentation is clear
- [ ] Repository is clean and organized

---

## 📧 Example Submission Text

```
PROJECT SUBMISSION: Movie Picture Pipeline CI/CD

GitHub Repository:
https://github.com/yourusername/movie-picture-pipeline

WORKING APPLICATIONS:

Frontend (Movie List UI):
http://a1b2c3d4-1234567890.us-east-1.elb.amazonaws.com
- Displays all 3 movies correctly
- UI loads without errors

Backend (Movies API):
http://e5f6g7h8-0987654321.us-east-1.elb.amazonaws.com/movies
- Returns JSON with 3 movies
- API responding correctly

WORKFLOWS IMPLEMENTED:
✅ Frontend Continuous Integration (CI)
✅ Backend Continuous Integration (CI)
✅ Frontend Continuous Deployment (CD)
✅ Backend Continuous Deployment (CD)

All workflows available at:
https://github.com/yourusername/movie-picture-pipeline/actions

INFRASTRUCTURE:
- AWS EKS Cluster: cluster
- AWS Region: us-east-1
- ECR Repositories: frontend, backend
- Deployment: Kubernetes with LoadBalancer services

TESTING:
- All linting checks passing
- All unit tests passing
- Docker builds successful
- Deployments successful
- Applications functional

SCREENSHOTS ATTACHED:
1. GitHub Actions - All workflows passing
2. Frontend application showing movie list
3. Backend API JSON response
4. Kubernetes deployments

NOTES:
- Using Udacity voclabs credentials
- All code pushed to main branch
- Complete documentation included
- Terraform used for infrastructure
- GitHub Actions for CI/CD

Thank you for reviewing!
```

---

**Ready to submit?** Use this checklist to ensure you have everything! 🚀

**Questions?** Review the documentation:
- [IMPORTANT_UPDATES.md](IMPORTANT_UPDATES.md)
- [TESTING_GUIDE.md](TESTING_GUIDE.md)
- [DEPLOYMENT_SETUP.md](DEPLOYMENT_SETUP.md)

