
[![Build Status](https://magnum.travis-ci.com/LandRegistry/matching.svg?token=N9pcG7F7VybLxV2xrpVh&branch=master)](https://magnum.travis-ci.com/LandRegistry/matching)


Matching service
================

Identity matching service


### To create a matching record for a service frontend user

Locally:
```
/create_matching_record.sh 'A Name' DateOfBirth [format = YYYY-MM-DD] gender [M/F] 'Current address' 'Previous address'
```

### Environment variables needed for this appication

For local development
```
SETTINGS='config.DevelopmentConfig'
DATABASE_URL='postgresql://localhost/matching'
```
Note in local dev port is assigned by dev env scripts

For production
```
PORT=[SOME NUMBER]
SETTINGS='config.Config'
DATABASE_URL='postgresql://user:password@db_host:port:db_name'
```

### To build an installer package

#### Prerequisites 

The machine that is being used to build this packages should have the following packages

* python
* pip 
* virtualenv
* virtualenv-tools
* ruby
* [fpm](https://github.com/jordansissel/fpm)


##### Create Python package

In base directory (where setup.py is)
```
python setup.py sdist
```

This creates a source distribution of the matching flask app in a subdirectory called dist. We'll install this into a virtualenv that will then be packaged into a deb.

##### Create Debian package

```
cd packaging
./build.sh
```

This will create a virtualenv, install matching into that env. Then it will set virtualenv paths to match the eventual installation directory of the debian package that is the output of build.sh.

**Note** 
The packaging of a virtualenv using fpm may soon be much easier depending on [outcome of this](https://github.com/jordansissel/fpm/issues/697)

An oddity of build.sh is that it needs to download a package that is listed in requirements, build it locally and install to the matching virtualenv as well.

The reason for this is that pip and setup.py dependency_links do not seem to play well. The package in question is [healthcheck](https://github.com/runscope/healthcheck). 

I will create a pull request with the maintainers of that package so that the package can be uploaded to pypi and this part of the script can be removed.

The result of running ./build.sh is debian package will be created in packaging called matching. The package has a basic upstart config, empty pre and post install and remove scripts. For the moment the installer is set to install to /opt/alpha/matching. Change as required. Also post install does not set ownership or permissions on the installed package.

**Before installing in a production box you should:**

* Set the environment variables as listed in environnment.sh 
* Create a no login user account that the matching service be owned and run as (at the moment in a dev vagrant it runs as root)

##### To install the debian package

```
sudo dpkg -i matching_0.1_all.deb
``` 

Then run

```
sudo start matching
```

Note that this assumes you have set all the correct environment variables.

To uninstall

```
sudo dpkg -r matching
```

##### Database migrations

At the moment the migration version files and manage.py are included in packages and live in installation directory. I would for the moment run these manually after install and before running the service.

```
cd /opt/alpha/matching
python manage.py db upgrade
```
