'''
    simpleirc
    ---------

    A simple IRC library.

    Links
    `````
    * `development version
    <https://github.com/maxcountryman/simpleirc>`_
'''

import os
import sys

from setuptools import setup

module_path = os.path.join(os.path.dirname(__file__), 'simpleirc/__init__.py')
version_line = [line for line in open(module_path)
                if line.startswith('__version_info__')][0]

__version__ = '.'.join(eval(version_line.split('__version_info__ = ')[-1]))

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
      classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ))
