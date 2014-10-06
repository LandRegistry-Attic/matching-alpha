#!/bin/bash
source /vagrant/script/dev-env-functions
source ./environment.sh
create_virtual_env "matching"

python manage.py unblock_user --lrid=$1
deactivate

echo
echo
echo "User unblocked"
echo
echo
