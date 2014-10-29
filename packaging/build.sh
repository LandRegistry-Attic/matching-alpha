#! /usr/bin/env bash
set -xe

export VERSION=0.1
export INSTALL_DIR=opt/alpha/matching # change this to somewhere better

# build the python installable distribution of matching
cd ../
python setup.py sdist
cd -

# if this following part seems a little crazy then let me assure you it is.
# however I could not get setuptools dependency links and pip to play nice
# so we have to go through some healthcheck pain
export TEMP=$(mktemp -d -t external-deps-XXXXX)
curl -L https://github.com/Runscope/healthcheck/archive/master/master.tar.gz -o $TEMP/master.tar.gz
tar -xvf $TEMP/master.tar.gz -C $TEMP

cd $TEMP/healthcheck-master
python setup.py sdist
cd -
# end a bit of healthcheck craziness
# better solution is to get packages from pypi

# make a virtualenv to install matching and healtcheck distribution packages
mkdir -p build/$INSTALL_DIR
virtualenv build/$INSTALL_DIR

build/$INSTALL_DIR/bin/pip install -U pip distribute

# install matching and healtcheck package to virtualenv
build/$INSTALL_DIR/bin/pip install ../dist/*
build/$INSTALL_DIR/bin/pip install $TEMP/healthcheck-master/dist/*

build/$INSTALL_DIR/bin/pip uninstall -y distribute

#copy over migration dir and manage.py script into base dir
cp -a ../migrations build/$INSTALL_DIR/
cp ../manage.py build/$INSTALL_DIR/

# copy gunicorn config for runing of app
cp gunicorn_config.py build/$INSTALL_DIR/

# reset virtualenv paths so that they match eventual install directory
cd build/$INSTALL_DIR
virtualenv-tools --update-path /$INSTALL_DIR
cd -

cd build

# build the deb package from the virtualenv containing matching and all dependencies
fpm \
    -t deb -s dir -a all -n matching -v $VERSION \
    --after-install ../debian/postinst \
    --after-remove ../debian/prerm \
    --url https://github.com/LandRegistry/matching \
    --deb-upstart ../upstart/matching \
    -x "*.pyc" \
    -x "*.pyo" \
    --description 'LR Matching service - used as part of GOV.UK Verify' \
    --license 'MIT' \
    --prefix / \
    .

cd -

# cleanup
mv build/*.deb .
rm -rf build
cd ../
rm -rf dist
rm -rf *.egg-info
rm -rf $TEMP

# upload the deb to apt repo
