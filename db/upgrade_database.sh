#!/bin/bash
# This script will migrate the dataabase. It assumes that we're in a virtual environment
# with a version of python configured for the application.

set -e

if [ -z ${APP_ROOT} ]; then
	echo "Could not find setting for APP_ROOT in environment"
	echo "This must point to the root directory of your app"
	exit 1
fi

cd ${APP_ROOT} && python manage.py db upgrade 
