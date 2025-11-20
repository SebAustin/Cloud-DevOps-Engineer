# Important Updates & Fixes

This document contains critical updates applied to the project to address compatibility issues discovered during implementation.

## 🔧 Critical Fixes Applied

### 1. Kubernetes Version Update
**Issue**: AWS EKS no longer supports Kubernetes 1.25  
**Fix**: Updated `setup/terraform/variables.tf`
```terraform
variable "k8s_version" {
  default = "1.28"  # Changed from 1.25
}
```
**Status**: ✅ Fixed

### 2. Udacity Voclabs Compatibility
**Issue**: Voclabs accounts have restricted IAM permissions and cannot create IAM users  
**Fix**: Commented out IAM user creation in `setup/terraform/main.tf`
```terraform
# Lines 315-332 now commented out:
# resource "aws_iam_user" "github_action_user" { ... }
# resource "aws_iam_user_policy" "github_action_user_permission" { ... }
```
**Status**: ✅ Fixed

**Impact on outputs.tf**: Removed `github_action_user_arn` output

### 3. init.sh macOS Compatibility
**Issue**: Script downloaded Linux binary on macOS systems  
**Fix**: Updated `setup/init.sh` to detect OS and architecture
```bash
# Now automatically detects:
# - macOS arm64 (Apple Silicon)
# - macOS amd64 (Intel)
# - Linux amd64
```
**Status**: ✅ Fixed

### 4. init.sh for Voclabs Accounts
**Issue**: Voclabs users get "Unauthorized" when trying to modify aws-auth ConfigMap  
**Fix**: Updated `setup/init.sh` to use current user ARN instead of github-action-user
```bash
# Changed from:
userarn=$(aws iam get-user --user-name github-action-user | jq -r .User.Arn)

# To:
userarn=$(aws sts get-caller-identity | jq -r .Arn)
```
**Status**: ✅ Fixed

**Alternative for Voclabs**: Skip init.sh entirely and just run:
```bash
aws eks update-kubeconfig --name cluster --region us-east-1
```

---

## 📋 Key Setup Differences: Personal AWS vs Udacity Voclabs

### Personal AWS Account
| Step | Action | Details |
|------|--------|---------|
| AWS Setup | Create IAM admin user | Use for Terraform |
| Terraform | Creates github-action-user | IAM user with ECR/EKS permissions |
| init.sh | Run the script | Adds github-action-user to Kubernetes |
| GitHub Secrets | Use github-action-user credentials | Long-lived, dedicated credentials |

### Udacity Voclabs Account
| Step | Action | Details |
|------|--------|---------|
| AWS Setup | Use voclabs credentials | Provided by lab environment |
| Terraform | ✅ IAM user creation skipped | Already commented out in code |
| init.sh | ⚠️ Skip this step | Or run updated version (optional) |
| kubectl | Direct configuration | `aws eks update-kubeconfig --name cluster --region us-east-1` |
| GitHub Secrets | Use voclabs credentials | ⚠️ Expire after lab session |

---

## 🔑 GitHub Secrets Configuration

### For Personal AWS Accounts
```
AWS_ACCESS_KEY_ID     = <github-action-user access key>
AWS_SECRET_ACCESS_KEY = <github-action-user secret key>
```

### For Udacity Voclabs Accounts
```
AWS_ACCESS_KEY_ID     = <voclabs access key>
AWS_SECRET_ACCESS_KEY = <voclabs secret key>
```

⚠️ **Important**: Voclabs credentials expire! Update GitHub Secrets before testing pipelines.

---

## 🛠️ Required Local Tools

Install these tools before starting:

```bash
# Terraform version manager
git clone https://github.com/tfutils/tfenv.git ~/.tfenv
echo 'export PATH="$HOME/.tfenv/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
tfenv install 1.3.9
tfenv use 1.3.9

# Python package manager
pip install pipenv
# or
brew install pipenv

# Kubernetes manifest tool
brew install kustomize

# Verify installations
terraform version    # Should show 1.3.9
pipenv --version     # Should show version
kustomize version    # Should show version
```

---

## 🐛 Common Issues & Solutions

### Issue: "Unsupported Terraform Core version"
**Solution**:
```bash
tfenv use 1.3.9
# If not installed:
tfenv install 1.3.9
```

### Issue: "unsupported Kubernetes version 1.25"
**Solution**: Already fixed - using version 1.28

### Issue: "not authorized to perform: iam:PutUserPolicy" (voclabs)
**Solution**: Already fixed - IAM user creation commented out

### Issue: "cannot execute binary file" (init.sh on macOS)
**Solution**: Already fixed - script detects OS automatically

### Issue: "Unauthorized" when running init.sh (voclabs)
**Solution**: Skip init.sh, use direct kubeconfig:
```bash
aws eks update-kubeconfig --name cluster --region us-east-1
kubectl get nodes
```

### Issue: "command not found: pipenv"
**Solution**:
```bash
pip install pipenv
# or
pip3 install pipenv
# or
brew install pipenv
```

### Issue: "command not found: kustomize"
**Solution**:
```bash
brew install kustomize
```

### Issue: "docker: invalid reference format"
**Solution**: Check for extra characters or missing build context:
```bash
# Wrong:
docker build --tag mp-backend:latest
docker run --name mp-frontend -p 3000:3000 -d mp-frontend]

# Correct:
docker build --tag mp-backend:latest .
docker run --name mp-frontend -p 3000:3000 -d mp-frontend
```

### Issue: Backend API not responding
**Solution**:
```bash
# Check logs
docker logs mp-backend

# Check if running
docker ps

# Try foreground mode
docker run --rm -p 5000:5000 mp-backend:latest

# Test API
curl http://localhost:5000/movies
```

---

## ✅ Verification Checklist

Before running CI/CD pipelines:

### Local Environment
- [ ] Terraform 1.3.9 installed (`terraform version`)
- [ ] pipenv installed (`pipenv --version`)
- [ ] kustomize installed (`kustomize version`)
- [ ] Docker running (`docker ps`)
- [ ] AWS CLI configured (`aws sts get-caller-identity`)

### AWS Infrastructure
- [ ] EKS cluster created (`aws eks list-clusters --region us-east-1`)
- [ ] ECR repositories exist (`aws ecr describe-repositories --region us-east-1`)
- [ ] kubectl configured (`kubectl cluster-info`)
- [ ] Nodes running (`kubectl get nodes`)

### GitHub Setup
- [ ] Repository created and code pushed
- [ ] GitHub Secrets configured (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
- [ ] All 4 workflow files in `.github/workflows/`

### Local Testing
- [ ] Frontend tests pass (`cd starter/frontend && CI=true npm test`)
- [ ] Frontend lint passes (`npm run lint`)
- [ ] Frontend builds (`docker build --build-arg=REACT_APP_MOVIE_API_URL=http://localhost:5000 -t mp-frontend:latest .`)
- [ ] Backend tests pass (`cd starter/backend && pipenv run test`)
- [ ] Backend lint passes (`pipenv run lint`)
- [ ] Backend builds (`docker build -t mp-backend:latest .`)

---

## 🚀 Quick Start Command Reference

### Initial Setup
```bash
# 1. Install tools
brew install kustomize pipenv

# 2. Setup Terraform
tfenv use 1.3.9
cd setup/terraform
export AWS_ACCESS_KEY_ID=<your-key>
export AWS_SECRET_ACCESS_KEY=<your-secret>
terraform init
terraform apply

# 3. Configure kubectl (voclabs)
aws eks update-kubeconfig --name cluster --region us-east-1
kubectl get nodes

# 4. Verify infrastructure
terraform output
aws ecr describe-repositories --region us-east-1
```

### Local Testing
```bash
# Frontend
cd starter/frontend
npm ci
npm run lint
CI=true npm test
docker build --build-arg=REACT_APP_MOVIE_API_URL=http://localhost:5000 -t mp-frontend:latest .

# Backend
cd starter/backend
pipenv install --dev
pipenv run lint
pipenv run test
docker build -t mp-backend:latest .
```

### GitHub Setup
```bash
# Initialize repo
git init
git add .
git commit -m "feat: Add CI/CD pipeline"
git remote add origin <your-repo-url>
git branch -M main
git push -u origin main
```

---

## 📝 File Changes Summary

| File | Change | Reason |
|------|--------|--------|
| `setup/terraform/variables.tf` | k8s_version: 1.28 | AWS no longer supports 1.25 |
| `setup/terraform/main.tf` | IAM user commented out | Voclabs compatibility |
| `setup/terraform/outputs.tf` | Removed IAM output | IAM user not created |
| `setup/init.sh` | OS detection added | macOS compatibility |
| `setup/init.sh` | Use current user ARN | Voclabs compatibility |

---

## 📚 Documentation Files

- `DEPLOYMENT_SETUP.md` - Comprehensive setup guide
- `TESTING_GUIDE.md` - Testing procedures and verification
- `README_CICD.md` - Project overview and architecture
- `VALIDATION_SUMMARY.md` - Rubric compliance checklist
- `QUICK_REFERENCE.md` - Command reference
- `IMPLEMENTATION_COMPLETE.md` - Next steps after implementation
- `IMPORTANT_UPDATES.md` - This file

---

## 💡 Pro Tips

1. **Use tfenv**: Makes switching Terraform versions easy
2. **Test locally first**: Always verify builds work before pushing
3. **Check logs**: Most issues can be debugged via container logs
4. **Voclabs credentials expire**: Update GitHub Secrets regularly
5. **Use manual triggers**: Test workflows without code changes
6. **Monitor AWS costs**: Check billing regularly
7. **Clean up after**: Run `terraform destroy` when done

---

## 🎯 Production vs Learning Considerations

### In This Project (Learning)
- ✅ Voclabs credentials acceptable
- ✅ IAM user creation optional
- ✅ Simplified authentication

### In Production
- ❌ Never use temporary credentials
- ✅ Always create dedicated IAM users
- ✅ Use IAM roles for services
- ✅ Implement least-privilege access
- ✅ Enable MFA for sensitive operations
- ✅ Rotate credentials regularly

---

**Last Updated**: November 19, 2024  
**Terraform Version**: 1.3.9  
**Kubernetes Version**: 1.28  
**AWS Region**: us-east-1  
**Status**: All fixes applied and tested ✅

