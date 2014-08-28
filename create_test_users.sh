#!/bin/bash

source /vagrant/script/dev-env-functions
source ./environment.sh
create_virtual_env "matching"
python manage.py create_user --lrid='2fd71646-7ebb-4b90-89d0-1a0221aafbff' --name='Walter White' --dob='1959-09-07' --gender='M' --current_address='1 High St, London, N1 4LT' --previous_address='2 High St, London, SW2 1LT'
deactivate
