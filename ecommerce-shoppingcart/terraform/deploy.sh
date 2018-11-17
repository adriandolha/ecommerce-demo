#!/usr/bin/env bash
set -e

#VARS
# by default build package from the _develop_ branch and deploy it to the _dev_ environment
BRANCH="${2-master}"
ENV="${3-dev}"
green="\e[32m"
default="\e[39m"



# call the build script
function build {
  # ./build.sh branch
  ./build.sh "${BRANCH}"
}


function terraform_init {
  # init terraform
  printf "%b⚓Terraform init...%b\n" "$green" "$default"
  terraform init

  # make sure that the workspace exists, if not create a new one and use that one
  printf "%b⚓Creating and selecting the $ENV environment(workspace)...%b\n" "$green" "$default"
  terraform workspace select "$ENV" || terraform workspace new "$ENV"
}

case "$1" in
  apply)
    build "$BRANCH"
    terraform_init
    printf "%b⚓Deploying from branch \"$BRANCH\" to \"$ENV\" environment%b\n" "$green" "$default"
    terraform apply -auto-approve -var env="$ENV"
    printf "%b⚓Deployment finished from branch \"$BRANCH\" to \"$ENV\" environment%b\n" "$green" "$default"
    ;;
  destroy)
    # if destroy is called then the environment should be the next argument
    ENV=$2
    printf "%b⚓Destroying \"$ENV\" environment for this component\n%b" "$green" "$default"
    terraform_init
    terraform destroy -auto-approve -var env="$ENV"
    # switch to the default workspace so that we can delete the workspace
    terraform workspace select default
    # delete the workspace/environment
    terraform workspace delete "$ENV"
    ;;
  *)
    printf "%b⚓Usage: $0 {apply branch environment|destroy environment}\n%b" "$green" "$default"
esac