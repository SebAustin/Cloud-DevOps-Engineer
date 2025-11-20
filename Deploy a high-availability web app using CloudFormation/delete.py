#!/usr/bin/env python3
"""
Udagram Infrastructure Deletion Script
This script automates the deletion of the Udagram infrastructure.
It empties the S3 bucket, deletes the application stack, then deletes the network stack.
"""

import boto3
import sys
from botocore.exceptions import ClientError, WaiterError

# Configuration
NETWORK_STACK_NAME = 'udagram-network'
APP_STACK_NAME = 'udagram-app'
REGION = 'us-east-1'  # Change this to your preferred region

# Initialize boto3 clients
cloudformation = boto3.client('cloudformation', region_name=REGION)
s3 = boto3.resource('s3', region_name=REGION)


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


def print_warning(message):
    """Print a warning message."""
    print(f"⚠ WARNING: {message}")


def stack_exists(stack_name):
    """Check if a CloudFormation stack exists."""
    try:
        response = cloudformation.describe_stacks(StackName=stack_name)
        status = response['Stacks'][0]['StackStatus']
        if status == 'DELETE_COMPLETE':
            return False
        return True
    except ClientError as e:
        if 'does not exist' in str(e):
            return False
        raise


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


def empty_s3_bucket(bucket_name):
    """Empty all objects from an S3 bucket."""
    try:
        print_info(f"Emptying S3 bucket: {bucket_name}")
        bucket = s3.Bucket(bucket_name)
        
        # Delete all objects
        bucket.objects.all().delete()
        
        # Delete all object versions (if versioning is enabled)
        bucket.object_versions.all().delete()
        
        print_success(f"S3 bucket {bucket_name} emptied successfully!")
        return True
    except ClientError as e:
        if 'NoSuchBucket' in str(e):
            print_info(f"Bucket {bucket_name} does not exist or is already deleted.")
            return True
        print_error(f"Failed to empty S3 bucket: {e}")
        return False


def delete_stack(stack_name):
    """Delete a CloudFormation stack."""
    try:
        print_info(f"Deleting stack: {stack_name}")
        cloudformation.delete_stack(StackName=stack_name)
        print_success(f"Stack deletion initiated: {stack_name}")
        return True
    except ClientError as e:
        print_error(f"Failed to delete stack: {e}")
        return False


def wait_for_stack_deletion(stack_name):
    """Wait for a CloudFormation stack to be deleted."""
    print_info(f"Waiting for stack {stack_name} to be deleted...")
    print_info("This may take several minutes. Please be patient.")
    
    waiter = cloudformation.get_waiter('stack_delete_complete')
    try:
        waiter.wait(
            StackName=stack_name,
            WaiterConfig={
                'Delay': 30,
                'MaxAttempts': 120
            }
        )
        print_success(f"Stack {stack_name} deleted successfully!")
        return True
    except WaiterError as e:
        print_error(f"Stack deletion failed: {e}")
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


def confirm_deletion():
    """Ask user to confirm deletion."""
    print_section("Udagram Infrastructure Deletion")
    print_warning("This will DELETE all Udagram infrastructure!")
    print_warning("This action CANNOT be undone!")
    print("\nThe following stacks will be deleted:")
    print(f"  1. {APP_STACK_NAME}")
    print(f"  2. {NETWORK_STACK_NAME}")
    
    response = input("\nAre you sure you want to continue? (yes/no): ").lower().strip()
    return response in ['yes', 'y']


def main():
    """Main function to orchestrate the infrastructure deletion."""
    print_info(f"Region: {REGION}")
    
    # Confirm deletion
    if not confirm_deletion():
        print_info("Deletion cancelled by user.")
        sys.exit(0)
    
    # Check if stacks exist
    app_stack_exists = stack_exists(APP_STACK_NAME)
    network_stack_exists = stack_exists(NETWORK_STACK_NAME)
    
    if not app_stack_exists and not network_stack_exists:
        print_info("No Udagram stacks found. Nothing to delete.")
        sys.exit(0)
    
    # Step 1: Empty S3 Bucket
    if app_stack_exists:
        print_section("Step 1: Emptying S3 Bucket")
        s3_bucket_name = get_stack_output(APP_STACK_NAME, 'S3BucketName')
        
        if s3_bucket_name:
            if not empty_s3_bucket(s3_bucket_name):
                print_error("Failed to empty S3 bucket. Cannot proceed with deletion.")
                print_info("Please manually empty the S3 bucket and try again.")
                sys.exit(1)
        else:
            print_warning("Could not retrieve S3 bucket name. Proceeding with stack deletion.")
    
    # Step 2: Delete Application Stack
    if app_stack_exists:
        print_section("Step 2: Deleting Application Infrastructure")
        
        if not delete_stack(APP_STACK_NAME):
            print_error("Failed to initiate application stack deletion. Exiting.")
            sys.exit(1)
        
        if not wait_for_stack_deletion(APP_STACK_NAME):
            print_error("Application stack deletion failed.")
            print_info("Please check the AWS Console for more details.")
            sys.exit(1)
    else:
        print_info(f"Stack {APP_STACK_NAME} does not exist or is already deleted.")
    
    # Step 3: Delete Network Stack
    if network_stack_exists:
        print_section("Step 3: Deleting Network Infrastructure")
        
        if not delete_stack(NETWORK_STACK_NAME):
            print_error("Failed to initiate network stack deletion. Exiting.")
            sys.exit(1)
        
        if not wait_for_stack_deletion(NETWORK_STACK_NAME):
            print_error("Network stack deletion failed.")
            print_info("Please check the AWS Console for more details.")
            sys.exit(1)
    else:
        print_info(f"Stack {NETWORK_STACK_NAME} does not exist or is already deleted.")
    
    # Final Summary
    print_section("Infrastructure Deletion Complete!")
    print_success("All Udagram resources have been successfully deleted.")
    print_info("Your AWS account has been cleaned up.")
    print("\n" + "=" * 70 + "\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)

