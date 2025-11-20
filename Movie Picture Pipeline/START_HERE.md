# 🚀 Movie Picture Pipeline - CI/CD Project

## ⚠️ READ THIS FIRST

**Important**: Several fixes have been applied to ensure compatibility with current AWS services and Udacity voclabs accounts.

👉 **Start by reading**: [`IMPORTANT_UPDATES.md`](IMPORTANT_UPDATES.md)

---

## 📚 Documentation Guide

### 1. **Start Here** (You are here)
Quick overview and navigation

### 2. **[IMPORTANT_UPDATES.md](IMPORTANT_UPDATES.md)** 🔴 READ FIRST
- Critical fixes applied
- Udacity voclabs compatibility
- Common issues and solutions
- Tool installation requirements

### 3. **[DEPLOYMENT_SETUP.md](DEPLOYMENT_SETUP.md)**
- Complete step-by-step setup instructions
- AWS infrastructure with Terraform
- GitHub repository configuration
- Kubernetes setup

### 4. **[TESTING_GUIDE.md](TESTING_GUIDE.md)**
- Local validation procedures
- CI/CD workflow testing
- Application verification
- Troubleshooting guide

### 5. **[README_CICD.md](README_CICD.md)**
- Project architecture overview
- Technology stack
- Workflow descriptions
- Best practices

### 6. **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)**
- Essential commands
- Quick troubleshooting
- Common operations

### 7. **[VALIDATION_SUMMARY.md](VALIDATION_SUMMARY.md)**
- Rubric compliance checklist
- Requirements validation
- Pre-submission verification

### 8. **[IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md)**
- Next steps after setup
- Testing procedures
- Submission guidelines

---

## 🎯 Quick Start (5 Minutes)

### Prerequisites
```bash
# Install required tools
brew install kustomize pipenv

# Setup Terraform
tfenv install 1.3.9
tfenv use 1.3.9
```

### Deploy Infrastructure
```bash
# Set AWS credentials
export AWS_ACCESS_KEY_ID=<your-key>
export AWS_SECRET_ACCESS_KEY=<your-secret>

# Run Terraform
cd setup/terraform
terraform init
terraform apply

# Configure kubectl (for voclabs, skip init.sh)
aws eks update-kubeconfig --name cluster --region us-east-1
kubectl get nodes
```

### Setup GitHub
```bash
# Create repository and push code
git init
git add .
git commit -m "feat: Add CI/CD pipeline"
git remote add origin <your-repo-url>
git push -u origin main
```

### Configure GitHub Secrets
Add in repository Settings → Secrets:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

### Test CI/CD
1. Create a pull request → CI workflows run
2. Merge to main → CD workflows deploy to EKS
3. Verify deployment: `kubectl get all`

---

## ✅ Critical Fixes Applied

### 1. Kubernetes Version
- ❌ Old: 1.25 (unsupported)
- ✅ New: 1.28 (supported)

### 2. Voclabs Compatibility
- ✅ IAM user creation disabled (permission restrictions)
- ✅ init.sh can be skipped
- ✅ Direct kubectl configuration

### 3. macOS Compatibility
- ✅ init.sh detects OS automatically
- ✅ Downloads correct binary for Apple Silicon

---

## 📁 Project Structure

```
.
├── .github/workflows/          # GitHub Actions workflows
│   ├── frontend-ci.yaml        # Frontend CI (PR trigger)
│   ├── backend-ci.yaml         # Backend CI (PR trigger)
│   ├── frontend-cd.yaml        # Frontend CD (push to main)
│   └── backend-cd.yaml         # Backend CD (push to main)
├── starter/
│   ├── frontend/               # React application
│   └── backend/                # Flask application
├── setup/
│   ├── terraform/              # Infrastructure as Code
│   └── init.sh                 # Kubernetes config script
├── IMPORTANT_UPDATES.md        # 🔴 Critical updates
├── DEPLOYMENT_SETUP.md         # Setup guide
├── TESTING_GUIDE.md            # Testing procedures
├── README_CICD.md              # Project documentation
├── QUICK_REFERENCE.md          # Command reference
└── START_HERE.md               # This file
```

---

## 🔑 Key Features

✅ **Automated CI/CD** - GitHub Actions workflows  
✅ **Parallel Testing** - Lint and test run simultaneously  
✅ **Docker Builds** - Containerized applications  
✅ **EKS Deployment** - Kubernetes on AWS  
✅ **ECR Integration** - Container registry  
✅ **Git SHA Tagging** - Traceable deployments  
✅ **Voclabs Compatible** - Works with Udacity labs  

---

## 🚨 Common Issues

### "Unsupported Terraform Core version"
```bash
tfenv use 1.3.9
```

### "unsupported Kubernetes version 1.25"
Already fixed - using 1.28

### "command not found: pipenv"
```bash
pip install pipenv
```

### "command not found: kustomize"
```bash
brew install kustomize
```

### "Unauthorized" (init.sh)
Skip init.sh, use:
```bash
aws eks update-kubeconfig --name cluster --region us-east-1
```

See [IMPORTANT_UPDATES.md](IMPORTANT_UPDATES.md) for more solutions.

---

## 🎓 For Udacity Students

### Using Voclabs
1. ✅ Use your voclabs AWS credentials
2. ✅ Skip init.sh (you already have access)
3. ✅ Update GitHub Secrets before each session (credentials expire)
4. ✅ All fixes already applied - just follow the guides

### For Grading
- Ensure voclabs credentials are fresh
- All workflows should be passing
- Applications deployed and accessible
- Take screenshots of working applications

---

## 📊 Workflow Overview

```
Pull Request Created
       ↓
   CI Workflow
   ├── Lint (parallel)
   ├── Test (parallel)
   └── Build (after lint + test)
       ↓
   Review & Merge
       ↓
   CD Workflow
   ├── Lint (parallel)
   ├── Test (parallel)
   ├── Build & Push to ECR
   └── Deploy to EKS
       ↓
   Application Live
```

---

## 💬 Need Help?

1. Check [IMPORTANT_UPDATES.md](IMPORTANT_UPDATES.md) for fixes
2. Review [TESTING_GUIDE.md](TESTING_GUIDE.md) for troubleshooting
3. See [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for commands
4. Check container logs: `docker logs <container-name>`
5. Check workflow logs in GitHub Actions tab

---

## 🧹 Cleanup (After Grading)

```bash
# Delete Kubernetes resources
kubectl delete all --all

# Destroy AWS infrastructure
cd setup/terraform
terraform destroy
```

**Estimated AWS Cost**: ~$120/month (tear down when not in use!)

---

## 🎉 Success Criteria

Your project is successful when:

- ✅ All 4 workflow files exist
- ✅ CI triggers on pull requests
- ✅ CD triggers on push to main
- ✅ Tests pass locally and in CI
- ✅ Docker images push to ECR
- ✅ Applications deploy to Kubernetes
- ✅ Frontend displays movies
- ✅ Backend API returns data
- ✅ All workflows show green checkmarks

---

**Ready to start?** → Read [IMPORTANT_UPDATES.md](IMPORTANT_UPDATES.md) first! 🚀

