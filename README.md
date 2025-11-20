# Cloud DevOps Engineer Portfolio

This repository showcases production-ready implementations of cloud infrastructure, containerization, and CI/CD pipelines. Each project demonstrates best practices in AWS cloud architecture, Kubernetes orchestration, Infrastructure as Code, and automated deployment workflows.

## Projects

### 1. Udagram - High-Availability Web Application

**Infrastructure as Code with AWS CloudFormation**

A highly available web application deployment on AWS using CloudFormation templates. The infrastructure spans multiple availability zones with a custom VPC, public and private subnets, auto-scaling EC2 instances behind an Application Load Balancer, and S3 for static content hosting. Features include automated NAT gateway deployment for high availability, security groups following least-privilege principles, and IAM roles for secure service integration. The project includes Python automation scripts for streamlined stack creation and teardown, demonstrating infrastructure orchestration and AWS best practices for fault-tolerant architectures.

**Technologies**: AWS CloudFormation, EC2 Auto Scaling Groups, Application Load Balancer, VPC, S3, IAM, Python (boto3)

[📂 View Project](./Deploy%20a%20high-availability%20web%20app%20using%20CloudFormation/)

---

### 2. Coworking Space Analytics Microservice

**Kubernetes Deployment with CI/CD Automation**

A microservices-based analytics API deployed on AWS EKS with fully automated CI/CD pipeline. The Flask application is containerized using Docker and automatically built via AWS CodeBuild upon GitHub commits. The deployment leverages Kubernetes best practices including health/readiness probes, ConfigMaps for configuration management, Secrets for credential handling, and resource limits for stable performance. PostgreSQL database is deployed using Helm charts with persistent storage, while AWS CloudWatch Container Insights provides comprehensive monitoring and log aggregation. The architecture demonstrates modern DevOps practices including semantic versioning, zero-downtime deployments, and infrastructure observability.

**Technologies**: AWS EKS, Docker, AWS CodeBuild, AWS ECR, Kubernetes, Helm, PostgreSQL, AWS CloudWatch, Python Flask

[📂 View Project](./Operationalizing%20a%20Coworking%20Space%20Microservice/)

---

### 3. Movie Picture Pipeline

**Complete CI/CD Implementation with GitHub Actions**

A full-stack application with sophisticated CI/CD pipelines built using GitHub Actions. The project includes a React frontend (TypeScript) and Flask backend (Python), each with dedicated continuous integration and deployment workflows. CI pipelines run automated linting and testing in parallel on pull requests, while CD pipelines build Docker images tagged with Git SHA, push to container registries, and deploy to Kubernetes using Kustomize for dynamic manifest generation. The infrastructure is provisioned using Terraform on AWS EKS, demonstrating end-to-end automation from code commit to production deployment with proper environment separation and deployment validation.

**Technologies**: GitHub Actions, Docker, Kubernetes, Kustomize, React, TypeScript, Python Flask, Terraform, AWS EKS, AWS ECR

[📂 View Project](./Movie%20Picture%20Pipeline/)

---

## Technologies & Skills

### Cloud Platforms
- **AWS Services**: EKS, ECR, CodeBuild, CloudFormation, CloudWatch, S3, IAM, VPC, EC2, ALB

### Container & Orchestration
- **Docker**: Multi-stage builds, image optimization, semantic versioning
- **Kubernetes**: Deployments, Services, ConfigMaps, Secrets, Health Probes, Resource Management
- **Helm**: Chart deployment and package management

### CI/CD & Automation
- **GitHub Actions**: Workflow automation, parallel job execution, conditional deployment
- **AWS CodeBuild**: Automated Docker builds, ECR integration, webhook triggers
- **Infrastructure as Code**: CloudFormation templates, Terraform modules, Kustomize overlays

### Development & Frameworks
- **Languages**: Python, TypeScript, JavaScript, SQL
- **Frameworks**: Flask (REST APIs), React (SPA)
- **Tools**: pytest, eslint, npm, pipenv

### Monitoring & Observability
- **AWS CloudWatch**: Container Insights, log aggregation, metrics collection
- **Kubernetes**: Readiness/liveness probes, resource monitoring

## Repository Structure

```
.
├── Deploy a high-availability web app using CloudFormation/
│   ├── network.yml                 # VPC and networking infrastructure
│   ├── udagram.yml                 # Application stack with ALB and ASG
│   ├── create.py                   # Automated deployment script
│   └── README.md                   # Detailed documentation
│
├── Operationalizing a Coworking Space Microservice/
│   ├── analytics/                  # Flask application source
│   ├── deployment/                 # Kubernetes manifests
│   ├── buildspec.yaml             # CodeBuild pipeline configuration
│   └── README.md                   # Deployment documentation
│
├── Movie Picture Pipeline/
│   ├── starter/
│   │   ├── frontend/              # React TypeScript application
│   │   └── backend/               # Flask Python API
│   ├── setup/terraform/           # Infrastructure provisioning
│   └── README.md                   # CI/CD workflow documentation
│
└── README.md                       # This file
```

## Getting Started

Each project contains comprehensive documentation including:
- Architecture diagrams and design decisions
- Step-by-step deployment instructions
- Configuration details and customization options
- Troubleshooting guides and best practices
- Cost considerations and optimization strategies

To explore a specific project, navigate to its directory and review the detailed README for prerequisites, setup instructions, and usage examples.

## Skills Demonstrated

- **Infrastructure as Code**: Declarative infrastructure using CloudFormation and Terraform
- **Container Orchestration**: Production Kubernetes deployments with proper resource management
- **CI/CD Pipelines**: Automated testing, building, and deployment workflows
- **Cloud Architecture**: Multi-AZ high availability, security best practices, cost optimization
- **Monitoring & Logging**: Centralized observability with CloudWatch Container Insights
- **DevOps Automation**: End-to-end automation from development to production
- **Microservices Design**: Scalable, maintainable service architectures
- **Security Best Practices**: Least-privilege IAM policies, secrets management, network segmentation

---

**Note**: These projects demonstrate practical implementations of Cloud DevOps engineering principles, emphasizing automation, scalability, security, and operational excellence.

