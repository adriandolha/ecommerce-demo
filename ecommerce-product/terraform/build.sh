#!/usr/bin/env bash

# Any subsequent(*) commands which fail will cause the shell script to exit immediately
set -e

# This script packages the connector and it's dependencies into a zip file
# that will be used by terraform to create a lambda function in aws

# variables
LAMDAFUN="https://github.com/adriandolha/ecommerce-demo.git"
LAMDADEST="ecommerce-product"
ARCHIVENAME="lambda_package"
BRANCH="${1-master}"
BUILD_DIR="/tmp/lambdabuild"
green="\e[32m"
default="\e[39m"

printf "%b⚓Building ${LAMDADEST} from the ${BRANCH} branch ...%b\n" "$green" "${default}"

printf "%b⚓cleaning buildir...%b\n" "${green}" "${default}"
rm -fr ${BUILD_DIR} && mkdir ${BUILD_DIR} && mkdir ${BUILD_DIR}/ecommerce-demo

printf "%b⚓cloning repo...%b\n" "$green" "$default"
git clone -b "${BRANCH}" --single-branch ${LAMDAFUN} ${BUILD_DIR}/ecommerce-demo --depth 1
BUILDIR="${BUILD_DIR}/ecommerce-demo/ecommerce-product"
# create a temporary virtualenv
python3 -m venv ${BUILDIR}/virtualenv

# activate the virtualenv
source ${BUILDIR}/virtualenv/bin/activate

# install deps
printf "%b⚓installing the dependencies in the virtualenv...%b\n" "${green}" "${default}"


#INSTALL ecommerce-product
mkdir -p ${BUILDIR}/ecommerce-product/lambda_package
pip install -q ${BUILDIR} -U -t $BUILDIR/lambda_package
pip install -q ${BUILDIR}/ -U -r ${BUILDIR}/requirements.txt -t ${BUILDIR}/lambda_package

    # sync files
rsync -aP  ${BUILDIR}/ecommerce_product/ ${BUILDIR}/lambda_package/
rsync -aP  ${BUILDIR}/*.py ${BUILDIR}/lambda_package/

    #CREATE ARCHIVE
( cd ${BUILDIR}/lambda_package && zip -q -r9 ${BUILDIR}/${ARCHIVENAME}.zip . )
cp ${BUILDIR}/${ARCHIVENAME}.zip ./${ARCHIVENAME}_ecommerce_product.zip
