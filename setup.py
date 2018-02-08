'''
Application initialization.
'''
from setuptools import setup, find_packages

APP_NAME = 'accounting-reports'
APP_DIR = 'accounting_reports'

VERSION_STRING = None

with open('%s/version.py' % APP_DIR) as f:
  for line in f:
    if line.startswith('__version__'):
      VERSION_STRING = line.strip().split('=')[1]

setup(
    name=APP_NAME,
    version=VERSION_STRING,
    packages=find_packages(),
    include_package_data=True,
    long_description=__doc__,
    entry_points={
        'console_scripts': [
            '%s = %s.%s:main' % (APP_NAME, APP_DIR, APP_DIR),
        ]
    }
)
