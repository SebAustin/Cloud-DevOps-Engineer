# Quick Reference Guide

Essential commands for working with the Movie Picture Pipeline CI/CD project.

## 🚀 Initial Setup

### Terraform Setup
```bash
# Install tfenv
git clone https://github.com/tfutils/tfenv.git ~/.tfenv
export PATH="$HOME/.tfenv/bin:$PATH"
tfenv install 1.3.9
tfenv use 1.3.9

# Initialize and apply
cd setup/terraform
terraform init
terraform apply

# View outputs
terraform output
```

### Kubernetes Setup
```bash
cd setup
./init.sh
```

### GitHub Repository Setup
```bash
cd "/Users/shenry/Documents/Personal/Training/Project/Udacity/Cloud DevOps Engineer/Movie Picture Pipeline/cd12354-Movie-Picture-Pipeline-main"

git init
git add .
git commit -m "Initial commit: Add CI/CD pipeline"
git remote add origin <your-repo-url>
git branch -M main
git push -u origin main
```

---

## 🧪 Local Testing

### Frontend
```bash
cd starter/frontend

# Install dependencies
npm ci

# Lint
npm run lint

# Test
CI=true npm test

# Build Docker
docker build --build-arg=REACT_APP_MOVIE_API_URL=http://localhost:5000 -t mp-frontend:latest .

# Run locally
docker run -p 3000:3000 mp-frontend:latest
```

### Backend
```bash
cd starter/backend

# Install pipenv
pip install pipenv

# Install dependencies
pipenv install --dev

# Lint
pipenv run lint

# Test
pipenv run test

# Build Docker
docker build -t mp-backend:latest .

# Run locally
docker run -p 5000:5000 mp-backend:latest

# Test API
curl http://localhost:5000/movies
```

---

## ☸️ Kubernetes Commands

### Cluster Access
```bash
# Update kubeconfig
aws eks update-kubeconfig --name cluster --region us-east-1

# Verify connection
kubectl cluster-info
```

### View Resources
```bash
# All resources
kubectl get all

# Deployments
kubectl get deployments
kubectl describe deployment frontend
kubectl describe deployment backend

# Pods
kubectl get pods
kubectl get pods -o wide

# Services
kubectl get services
kubectl describe service frontend
kubectl describe service backend
```

### View Logs
```bash
# Frontend logs
kubectl logs deployment/frontend
kubectl logs -f deployment/frontend  # Follow

# Backend logs
kubectl logs deployment/backend
kubectl logs -f deployment/backend  # Follow

# Specific pod
kubectl logs <pod-name>
```

### Debug Pods
```bash
# Describe pod
kubectl describe pod <pod-name>

# Get pod details
kubectl get pod <pod-name> -o yaml

# Execute command in pod
kubectl exec -it <pod-name> -- /bin/sh

# Port forward for local access
kubectl port-forward deployment/frontend 3000:3000
kubectl port-forward deployment/backend 5000:5000
```

### Restart Deployments
```bash
kubectl rollout restart deployment/frontend
kubectl rollout restart deployment/backend

# Check rollout status
kubectl rollout status deployment/frontend
kubectl rollout status deployment/backend
```

### Delete Resources
```bash
# Delete specific deployment
kubectl delete deployment frontend
kubectl delete deployment backend

# Delete all resources
kubectl delete all --all
```

---

## 🐳 Docker Commands

### Image Management
```bash
# List images
docker images

# Remove image
docker rmi <image-id>

# Prune unused images
docker image prune -a
```

### Container Management
```bash
# List running containers
docker ps

# List all containers
docker ps -a

# Stop container
docker stop <container-id>

# Remove container
docker rm <container-id>

# View logs
docker logs <container-id>
docker logs -f <container-id>  # Follow
```

---

## 📦 ECR Commands

### Repository Management
```bash
# List repositories
aws ecr describe-repositories --region us-east-1

# List images in repository
aws ecr describe-images --repository-name frontend --region us-east-1
aws ecr describe-images --repository-name backend --region us-east-1

# Get login command
aws ecr get-login-password --region us-east-1
```

### Image Management
```bash
# Delete specific image
aws ecr batch-delete-image \
  --repository-name frontend \
  --image-ids imageTag=<tag> \
  --region us-east-1

# List image tags
aws ecr list-images --repository-name frontend --region us-east-1
```

---

## 🔐 AWS IAM Commands

### User Management
```bash
# List users
aws iam list-users

# Get user details
aws iam get-user --user-name github-action-user

# List access keys
aws iam list-access-keys --user-name github-action-user
```

### Create Access Keys
```bash
# Create access key for github-action-user
aws iam create-access-key --user-name github-action-user
```

---

## 🌐 Testing Application

### Get Service URLs
```bash
# Frontend URL
kubectl get service frontend -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'

# Backend URL
kubectl get service backend -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'
```

### Test Backend API
```bash
# Get backend URL
BACKEND_URL=$(kubectl get service backend -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

# Test API
curl http://$BACKEND_URL/movies

# Pretty print JSON
curl http://$BACKEND_URL/movies | jq
```

### Test Frontend
```bash
# Get frontend URL
FRONTEND_URL=$(kubectl get service frontend -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

# Open in browser (macOS)
open http://$FRONTEND_URL

# Or use curl
curl http://$FRONTEND_URL
```

---

## 🔄 Git Workflow

### Create Feature Branch
```bash
# Create and switch to new branch
git checkout -b feature/my-feature

# Make changes
# ... edit files ...

# Stage and commit
git add .
git commit -m "feat: add new feature"

# Push to remote
git push origin feature/my-feature
```

### Create Pull Request
```bash
# Push branch first
git push origin <branch-name>

# Then go to GitHub web interface to create PR
# Or use GitHub CLI
gh pr create --title "My Feature" --body "Description"
```

### Sync with Main
```bash
# Update main branch
git checkout main
git pull origin main

# Update feature branch
git checkout feature/my-feature
git merge main
```

---

## 🔍 Monitoring & Debugging

### Check Workflow Status
```bash
# Using GitHub CLI
gh run list
gh run view <run-id>
gh run watch
```

### Check Cluster Health
```bash
# Node status
kubectl get nodes

# Cluster info
kubectl cluster-info
kubectl cluster-info dump

# Events
kubectl get events --sort-by=.metadata.creationTimestamp
```

### Resource Usage
```bash
# Node resources
kubectl top nodes

# Pod resources
kubectl top pods
```

---

## 🧹 Cleanup

### Delete Kubernetes Resources
```bash
kubectl delete all --all
```

### Destroy AWS Infrastructure
```bash
cd setup/terraform
terraform destroy
# Type 'yes' to confirm
```

### Clean Docker
```bash
# Remove all stopped containers
docker container prune

# Remove all unused images
docker image prune -a

# Remove all unused volumes
docker volume prune

# Remove everything
docker system prune -a --volumes
```

### Clean Local Dependencies
```bash
# Frontend
cd starter/frontend
rm -rf node_modules
rm -rf build

# Backend
cd starter/backend
pipenv --rm  # Remove virtual environment
```

---

## 📊 Useful One-Liners

### Check if everything is running
```bash
kubectl get pods --no-headers | awk '{if ($3 != "Running") print $0}'
```

### Get all LoadBalancer URLs
```bash
kubectl get svc -o wide | grep LoadBalancer
```

### Watch pod status
```bash
watch kubectl get pods
```

### Get pod restart counts
```bash
kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.containerStatuses[0].restartCount}{"\n"}{end}'
```

### Check workflow run time
```bash
# Using GitHub CLI
gh run list --limit 5 --json conclusion,createdAt,updatedAt
```

---

## 🔧 Troubleshooting

### Pod not starting
```bash
# Check pod events
kubectl describe pod <pod-name>

# Check logs
kubectl logs <pod-name>

# Check image pull
kubectl get events | grep <pod-name>
```

### Service not accessible
```bash
# Check service
kubectl get svc <service-name>

# Check endpoints
kubectl get endpoints <service-name>

# Test from within cluster
kubectl run test-pod --image=busybox -it --rm -- wget -O- http://<service-name>:<port>
```

### ECR authentication issues
```bash
# Re-login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Verify credentials
aws sts get-caller-identity
```

### Workflow not triggering
```bash
# Check workflow syntax
yamllint .github/workflows/*.yaml

# Check GitHub Actions tab for errors
# Ensure branch name is correct (main, not master)
# Verify path filters match changed files
```

---

## 📝 Environment Variables

### Required GitHub Secrets
- `AWS_ACCESS_KEY_ID`: GitHub Actions AWS access key
- `AWS_SECRET_ACCESS_KEY`: GitHub Actions AWS secret key

### Workflow Environment Variables
- `AWS_REGION`: us-east-1
- `EKS_CLUSTER`: cluster
- `REACT_APP_MOVIE_API_URL`: http://backend:5000 (set during Docker build)

---

## 🔗 Useful Links

- **GitHub Repository**: `https://github.com/<username>/<repo>`
- **GitHub Actions**: `https://github.com/<username>/<repo>/actions`
- **AWS Console**: `https://console.aws.amazon.com/`
- **ECR**: `https://console.aws.amazon.com/ecr/`
- **EKS**: `https://console.aws.amazon.com/eks/`

---

## 📞 Getting Help

### Check Documentation
1. `DEPLOYMENT_SETUP.md` - Setup instructions
2. `TESTING_GUIDE.md` - Testing procedures
3. `VALIDATION_SUMMARY.md` - Requirements validation
4. `README_CICD.md` - Project overview

### Check Logs
1. GitHub Actions logs
2. Kubernetes pod logs
3. Docker container logs
4. AWS CloudWatch logs (if configured)

### Common Issues
- **Workflow not triggering**: Check path filters and branch names
- **Tests failing**: Run tests locally first
- **Deployment failing**: Check kubeconfig and AWS credentials
- **Application not accessible**: Check LoadBalancer status and security groups

---

## 💡 Tips

1. **Use caching**: First workflow run will be slow, subsequent runs are faster
2. **Test locally first**: Always test locally before pushing
3. **Check logs**: Most issues can be debugged through logs
4. **Use manual triggers**: Test workflows without pushing code
5. **Monitor costs**: Check AWS billing regularly
6. **Clean up resources**: Destroy infrastructure when done
7. **Use descriptive commits**: Helps track changes in workflow runs
8. **Enable auto-merge**: After CI passes (requires branch protection)

---

This quick reference should cover most common tasks. For detailed information, refer to the full documentation files.

