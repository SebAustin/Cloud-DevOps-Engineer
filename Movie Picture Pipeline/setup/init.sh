#!/bin/bash
set -e -o pipefail

echo "Fetching current IAM user ARN"
# For Udacity voclabs accounts, get the current assumed role ARN
userarn=$(aws sts get-caller-identity | jq -r .Arn)
echo "Using ARN: $userarn"

# Download tool for manipulating aws-auth
echo "Downloading tool..."
# Detect OS and architecture
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)

if [ "$OS" = "darwin" ]; then
    if [ "$ARCH" = "arm64" ]; then
        BINARY_URL="https://github.com/kubernetes-sigs/aws-iam-authenticator/releases/download/v0.6.2/aws-iam-authenticator_0.6.2_darwin_arm64"
    else
        BINARY_URL="https://github.com/kubernetes-sigs/aws-iam-authenticator/releases/download/v0.6.2/aws-iam-authenticator_0.6.2_darwin_amd64"
    fi
elif [ "$OS" = "linux" ]; then
    BINARY_URL="https://github.com/kubernetes-sigs/aws-iam-authenticator/releases/download/v0.6.2/aws-iam-authenticator_0.6.2_linux_amd64"
else
    echo "Unsupported OS: $OS"
    exit 1
fi

echo "Downloading from: $BINARY_URL"
curl -X GET -L "$BINARY_URL" -o aws-iam-authenticator
chmod +x aws-iam-authenticator

echo "Updating permissions"
./aws-iam-authenticator add user --userarn="${userarn}" --username=github-action-role --groups=system:masters --kubeconfig="$HOME"/.kube/config --prompt=false

echo "Cleaning up"
rm aws-iam-authenticator
echo "Done!"