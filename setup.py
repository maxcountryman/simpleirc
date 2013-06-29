'''
    simpleirc
    ---------

    A simple IRC library.

    Links
    `````
    * `development version <https://github.com/maxcountryman/simpleirc>`_
'''

import os
import sys

from simpleirc import __version__

from setuptools import find_packages, setup

if sys.argv[-1] == 'test':
    status = os.system('make check')
    status >>= 8
    sys.exit(status)

setup(name='simpleirc',
      version=__version__,
      url='https://github.com/maxcountryman/simpleirc',
      license='BSD',
      author='Max Countryman',
      author_email='maxc@me.com',
      description='A simple IRC library.',
      long_description=__doc__,
      zip_safe=False,
      platforms='any',
      packages=find_packages(),
      classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'),
      entry_points = {'console_scripts':
                      ['simpleirc = simpleirc.connection:run']})
