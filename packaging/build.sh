#! /usr/bin/env bash
set -xe

export VERSION=0.1
export INSTALL_DIR=opt/alpha/matching # change this to somewhere better

cd ../
python setup.py sdist
cd -

# if this seems a little crazy then let me assure you it is.
# however I could not get setuptools dependency links and pip to play nice
export TEMP=$(mktemp -d -t external-deps-XXXXX)
curl -L https://github.com/Runscope/healthcheck/archive/master/master.tar.gz -o $TEMP/master.tar.gz
tar -xvf $TEMP/master.tar.gz -C $TEMP

cd $TEMP/healthcheck-master
python setup.py sdist
cd -
# end a bit of healthcheck craziness
# better solution is to get packages from pypi

mkdir -p build/$INSTALL_DIR
virtualenv build/$INSTALL_DIR

build/$INSTALL_DIR/bin/pip install -U pip distribute
build/$INSTALL_DIR/bin/pip uninstall -y distribute

build/$INSTALL_DIR/bin/pip install ../dist/*
build/$INSTALL_DIR/bin/pip install $TEMP/healthcheck-master/dist/*

#copy over migration dir and manage.py script into base dir
cp -a ../migrations build/$INSTALL_DIR/
cp ../alembic.ini build/$INSTALL_DIR/
cp ../manage.py build/$INSTALL_DIR/

# copy gunicorn config for runing of app
cp gunicorn_config.py build/$INSTALL_DIR/

cd build/$INSTALL_DIR
virtualenv-tools --update-path /$INSTALL_DIR
cd -

cp -a debian/* build
cd build

fpm \
    -t deb -s dir -a all -n matching -v $VERSION \
    --after-install postinst \
    --after-remove prerm \
    --url https://github.com/LandRegistry/matching \
    --deb-upstart matching \
    --prefix / \
    -x "*.pyc" \
    -x "*.pyo" \
    --description 'LR Matching service - used as part of GOV.UK Verify' \
    --license 'MIT' \
    .

cd -

mv build/*.deb .
rm -rf build
cd ../
rm -rf dist
rm -rf *.egg-info
rm -rf $TEMP
