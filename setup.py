import os
from setuptools import setup, find_packages

app_name='accounting-reports'
app_dir='accounting_reports'

version_string = None
with open('%s/version.py' % app_dir) as f:
  for line in f:
    if(line.startswith('__version__')):
      version_string = line.strip().split('=')[1]

setup(
    name = app_name,
    version = version_string,
    packages=find_packages(),
    include_package_data=True,
    long_description=__doc__,
    entry_points={
       'console_scripts': [
           '%s = %s.%s:main' % (app_name, app_dir, app_dir),
       ]
    },
)
