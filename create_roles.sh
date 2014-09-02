#!/bin/bash

source /vagrant/script/dev-env-functions
source ./environment.sh
create_virtual_env "matching"

python manage.py create_role --name 'CITIZEN'
python manage.py create_role --name 'CONVEYANCER'

deactivate
