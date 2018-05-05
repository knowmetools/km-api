#!/bin/bash

# Usage: deploy.sh <ansible_dir> <inventory_name> <terraform_dir> <workspace>

set -euf
set -o pipefail

if [ -z ${1+x} ]
then
    cat<<EOF
Ansible directory not specified. You must specify the relative path to the
directory containing the 'deploy.yml' playbook.
EOF
fi

ANSIBLE_DIR=$1
shift

if [ -z ${1+x} ]
then
    cat <<EOF
No inventory file was specified. The inventory file should be relative to the
provided Ansible directory.
EOF
fi

ANSIBLE_INVENTORY=$1
shift

if [ -z ${1+x} ]
then
    cat <<EOF
No Terraform directory was specified. You must specify the relative path to the
directory containing the project's Terraform configuration.
EOF
fi

TERRAFORM_DIR=$1
shift

if [ -z ${1+x} ]
then
    cat <<EOF
No Terraform workspace specified. You must specify the Terraform workspace to
pull infrastructure information from.
EOF
fi

export TF_WORKSPACE=$1
shift


echo -e "\nUsing Terraform configuration in $TERRAFORM_DIR"
echo "Selecting '$TF_WORKSPACE' workspace"

BUCKET=$(cd $TERRAFORM_DIR && terraform output static_bucket)
DATABASE=$(cd $TERRAFORM_DIR && terraform output database)

cat<<EOF

Deploying with following parameters:

  Database Endpoint: $DATABASE
  Static Bucket: $BUCKET

EOF

echo -e "Running Ansible playbook:\n"
(
    cd $ANSIBLE_DIR
    ansible-playbook \
        -i $ANSIBLE_INVENTORY \
        --vault-password-file VAULT_PASSWORD_FILE \
        -e db_endpoint="$DATABASE" \
        -e static_bucket="$BUCKET" \
        deploy.yml
)
