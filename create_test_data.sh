#!/bin/bash

source /vagrant/script/dev-env-functions
source ./environment.sh
create_virtual_env "matching"

python manage.py create_role --name 'CITIZEN'
python manage.py create_role --name 'CONVEYANCER'

python manage.py create_user --name='Walter White' --dob='1959-09-07' --gender='M' --current_address='1 High St, London, N1 4LT' --previous_address='2 High St, London, SW2 1LT'

python manage.py create_user --name='Skyler White' --dob='1970-08-11' --gender='F' --current_address='100 Somewhere Far, End Of The Earth, X1 4LT' --previous_address='2 High St, London, SW2 1LT'

python manage.py create_user --name='Tuco Salamanca' --dob='1970-01-01' --gender='M' --current_address='123 Bad Place, Rottentown, ABC 123' --previous_address='981 A Worse Place, Grottytown, XYZ 123'

python manage.py add_role_to_user --username='Walter White' --rolename='CITIZEN'
python manage.py add_role_to_user --username='Skyler White' --rolename='CITIZEN'
python manage.py add_role_to_user --username='Tuco Salamanca' --rolename='CONVEYANCER'

deactivate
