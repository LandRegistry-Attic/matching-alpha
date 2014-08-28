    #!/bin/bash

source ./environment.sh

set +o errexit
createuser -s matching
createdb -U matching -O matching matching -T template0

python manage.py db upgrade
python run_dev.py
