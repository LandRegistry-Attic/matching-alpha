#!/bin/bash


set -e

if [[ $# -ne 5 ]]; then
    echo "Usage ./create_matching_record.sh 'A Name' DateOfBirth [format = YYYY-MM-DD] gender [M/F] 'Current address' 'Previous address'"
    exit 1
fi

source /vagrant/script/dev-env-functions
source ../environment.sh
create_virtual_env "matching"


export SETTINGS=config.DevelopmentConfig

python manage.py create_matching_record --name=$1 --dob=$2 --gender=$3 --current_address=$4 --previous_address=$5

deactivate

