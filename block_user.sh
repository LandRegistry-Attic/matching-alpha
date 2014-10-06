#!/bin/bash

source /vagrant/script/dev-env-functions
source ./environment.sh
create_virtual_env "matching"

python manage.py block_user --lrid=$1
deactivate

echo
echo
echo "Blocked user"
echo
echo
