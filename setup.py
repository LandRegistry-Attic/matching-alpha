# see http://bugs.python.org/issue8876
# this is just a quick hack so we can test build in vagrant
import os
if os.environ.get('USER','') == 'vagrant':
  del os.link

from setuptools import setup, find_packages

def requirements():
    with open('./requirements.txt', 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

requirements = requirements()

setup(name='matching',
      version='0.1',
      description='LR Matching service - used as part of GOV.UK Verify',
      author='Land Registry',
      author_email='lrdev@someemail.gov.uk',
      url='https://github.com/LandRegistry/matching',
      packages=find_packages(exclude=['tests']),
      zip_safe=False,
      include_package_data=True,
      license='MIT',
      platforms='any',
      install_requires=requirements,
      classifiers=(
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Programming Language :: Python :: 2.7',
        'Private :: Do Not Upload',
        ),
)
