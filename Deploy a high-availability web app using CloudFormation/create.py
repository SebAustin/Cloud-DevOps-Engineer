#!/usr/bin/env python3
"""
Udagram Infrastructure Creation Script
This script automates the creation of the Udagram infrastructure using AWS CloudFormation.
It creates the network stack first, then the application stack, and uploads static content to S3.
"""

import boto3
import json
import time
import sys
from botocore.exceptions import ClientError, WaiterError

# Configuration
NETWORK_STACK_NAME = 'udagram-network'
APP_STACK_NAME = 'udagram-app'
NETWORK_TEMPLATE = 'network.yml'
NETWORK_PARAMETERS = 'network-parameters.json'
APP_TEMPLATE = 'udagram.yml'
APP_PARAMETERS = 'udagram-parameters.json'
STATIC_CONTENT_FILE = 'static-content/index.html'
REGION = 'us-east-1'  # Change this to your preferred region

# Initialize boto3 clients
cloudformation = boto3.client('cloudformation', region_name=REGION)
s3 = boto3.client('s3', region_name=REGION)


def print_section(message):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {message}")
    print("=" * 70)


def print_success(message):
    """Print a success message."""
    print(f"✓ {message}")


def print_error(message):
    """Print an error message."""
    print(f"✗ ERROR: {message}")


def print_info(message):
    """Print an info message."""
    print(f"ℹ {message}")


def read_template(template_file):
    """Read and return the CloudFormation template."""
    try:
        with open(template_file, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print_error(f"Template file not found: {template_file}")
        sys.exit(1)


def read_parameters(parameter_file):
    """Read and return the parameters JSON."""
    try:
        with open(parameter_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print_error(f"Parameter file not found: {parameter_file}")
        sys.exit(1)


def stack_exists(stack_name):
    """Check if a CloudFormation stack exists."""
    try:
        cloudformation.describe_stacks(StackName=stack_name)
        return True
    except ClientError as e:
        if 'does not exist' in str(e):
            return False
        raise


def create_stack(stack_name, template_body, parameters):
    """Create a CloudFormation stack."""
    try:
        print_info(f"Creating stack: {stack_name}")
        response = cloudformation.create_stack(
            StackName=stack_name,
            TemplateBody=template_body,
            Parameters=parameters,
            Capabilities=['CAPABILITY_NAMED_IAM'],
            Tags=[
                {'Key': 'Project', 'Value': 'Udagram'},
                {'Key': 'Environment', 'Value': 'Production'}
            ]
        )
        print_success(f"Stack creation initiated: {response['StackId']}")
        return True
    except ClientError as e:
        print_error(f"Failed to create stack: {e}")
        return False


def wait_for_stack_creation(stack_name):
    """Wait for a CloudFormation stack to be created."""
    print_info(f"Waiting for stack {stack_name} to be created...")
    print_info("This may take several minutes. Please be patient.")
    
    waiter = cloudformation.get_waiter('stack_create_complete')
    try:
        waiter.wait(
            StackName=stack_name,
            WaiterConfig={
                'Delay': 30,
                'MaxAttempts': 120
            }
        )
        print_success(f"Stack {stack_name} created successfully!")
        return True
    except WaiterError as e:
        print_error(f"Stack creation failed: {e}")
        # Get stack events to show what went wrong
        try:
            events = cloudformation.describe_stack_events(StackName=stack_name)
            print("\nRecent stack events:")
            for event in events['StackEvents'][:10]:
                if 'FAILED' in event.get('ResourceStatus', ''):
                    print(f"  - {event['LogicalResourceId']}: {event.get('ResourceStatusReason', 'Unknown error')}")
        except Exception:
            pass
        return False


def get_stack_output(stack_name, output_key):
    """Get a specific output value from a CloudFormation stack."""
    try:
        response = cloudformation.describe_stacks(StackName=stack_name)
        outputs = response['Stacks'][0].get('Outputs', [])
        for output in outputs:
            if output['OutputKey'] == output_key:
                return output['OutputValue']
        return None
    except ClientError as e:
        print_error(f"Failed to get stack output: {e}")
        return None


def upload_to_s3(bucket_name, file_path, s3_key):
    """Upload a file to S3."""
    try:
        print_info(f"Uploading {file_path} to S3 bucket: {bucket_name}")
        s3.upload_file(
            file_path,
            bucket_name,
            s3_key,
            ExtraArgs={'ContentType': 'text/html'}
        )
        print_success(f"File uploaded successfully to s3://{bucket_name}/{s3_key}")
        return True
    except FileNotFoundError:
        print_error(f"File not found: {file_path}")
        return False
    except ClientError as e:
        print_error(f"Failed to upload to S3: {e}")
        return False


def display_stack_outputs(stack_name):
    """Display all outputs from a CloudFormation stack."""
    try:
        response = cloudformation.describe_stacks(StackName=stack_name)
        outputs = response['Stacks'][0].get('Outputs', [])
        
        if outputs:
            print_section(f"Stack Outputs: {stack_name}")
            for output in outputs:
                print(f"  {output['OutputKey']}: {output['OutputValue']}")
                if 'Description' in output:
                    print(f"    Description: {output['Description']}")
        else:
            print_info(f"No outputs available for stack: {stack_name}")
    except ClientError as e:
        print_error(f"Failed to get stack outputs: {e}")


def main():
    """Main function to orchestrate the infrastructure creation."""
    print_section("Udagram Infrastructure Creation")
    print_info(f"Region: {REGION}")
    print_info(f"Network Stack: {NETWORK_STACK_NAME}")
    print_info(f"Application Stack: {APP_STACK_NAME}")
    
    # Check if stacks already exist
    if stack_exists(NETWORK_STACK_NAME):
        print_error(f"Stack {NETWORK_STACK_NAME} already exists!")
        print_info("Please delete the existing stack first or use a different stack name.")
        sys.exit(1)
    
    if stack_exists(APP_STACK_NAME):
        print_error(f"Stack {APP_STACK_NAME} already exists!")
        print_info("Please delete the existing stack first or use a different stack name.")
        sys.exit(1)
    
    # Step 1: Create Network Stack
    print_section("Step 1: Creating Network Infrastructure")
    network_template = read_template(NETWORK_TEMPLATE)
    network_parameters = read_parameters(NETWORK_PARAMETERS)
    
    if not create_stack(NETWORK_STACK_NAME, network_template, network_parameters):
        print_error("Failed to create network stack. Exiting.")
        sys.exit(1)
    
    if not wait_for_stack_creation(NETWORK_STACK_NAME):
        print_error("Network stack creation failed. Exiting.")
        sys.exit(1)
    
    display_stack_outputs(NETWORK_STACK_NAME)
    
    # Step 2: Create Application Stack
    print_section("Step 2: Creating Application Infrastructure")
    app_template = read_template(APP_TEMPLATE)
    app_parameters = read_parameters(APP_PARAMETERS)
    
    if not create_stack(APP_STACK_NAME, app_template, app_parameters):
        print_error("Failed to create application stack. Exiting.")
        sys.exit(1)
    
    if not wait_for_stack_creation(APP_STACK_NAME):
        print_error("Application stack creation failed. Exiting.")
        sys.exit(1)
    
    display_stack_outputs(APP_STACK_NAME)
    
    # Step 3: Upload Static Content to S3
    print_section("Step 3: Uploading Static Content to S3")
    s3_bucket_name = get_stack_output(APP_STACK_NAME, 'S3BucketName')
    
    if s3_bucket_name:
        if upload_to_s3(s3_bucket_name, STATIC_CONTENT_FILE, 'index.html'):
            print_success("Static content uploaded successfully!")
        else:
            print_error("Failed to upload static content.")
            print_info("You can manually upload the file later.")
    else:
        print_error("Could not retrieve S3 bucket name from stack outputs.")
    
    # Final Summary
    print_section("Infrastructure Creation Complete!")
    load_balancer_url = get_stack_output(APP_STACK_NAME, 'LoadBalancerURL')
    
    if load_balancer_url:
        print_success(f"Your application is now available at:")
        print(f"\n    {load_balancer_url}\n")
        print_info("Note: It may take a few minutes for the instances to become healthy.")
        print_info("The health check grace period is 5 minutes.")
    
    print("\n" + "=" * 70)
    print("  Next Steps:")
    print("  1. Wait 5-10 minutes for instances to become healthy")
    print("  2. Access your application using the URL above")
    print("  3. Verify the page displays: 'It works! Udagram, Udacity'")
    print("=" * 70 + "\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)

