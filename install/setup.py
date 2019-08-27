# PyMLink installation script
# visit site www.microdaq.org
# Embedded-solutions, November 2017-2019

import platform
import os
import sys
import shutil
from setuptools import setup


def invalid_python_version():
    return sys.version_info[0] == 2 and sys.version_info[1] < 6


if invalid_python_version():
    print('Python2.6 and above are supported!')
    sys.exit(1)

PYMLINK_VERSION = 'py_mlink'
os_name = platform.system()

pack_data = {}
arch_dir = ''

linux_lib_name = 'libmlink.so'
linux_lib_path = '/usr/lib/'

darwin_lib_name = 'libmlink.dylib'
darwin_lib_path = '/usr/local/lib/'
demos_dependencies = []

if sys.version_info[0] == 2:
     demos_dependencies = ["matplotlib"]

if sys.version_info[0] == 3:
     demos_dependencies = ["numpy", "matplotlib", "pyqt5", "pyqtgraph"]

# Check python platform version
if platform.architecture()[0] == '32bit':
    win_lib_name = 'MLink32.dll'
    arch_dir = 'x86/'
elif platform.architecture()[0] == '64bit':
    win_lib_name = 'MLink64.dll'
    arch_dir = 'x64/'
else:
    print('Your platform is not supported!')
    sys.exit()

# Check OS
if os_name == 'Windows':
    pack_data = {PYMLINK_VERSION: [win_lib_name]}
    shutil.copy(
        os.path.normpath(PYMLINK_VERSION+'/'+arch_dir+win_lib_name),
        os.path.normpath(PYMLINK_VERSION+'/'+win_lib_name))

elif os_name == 'Linux':
    # in case of arm processors take another binary
    if platform.uname()[4].startswith('arm'):
       arch_dir = 'armel/'
    
    # copy lib to standard linux location
    try:
        print(
            'copying file '+PYMLINK_VERSION+'/'
            + arch_dir + linux_lib_name+' to '
            + linux_lib_path)
        shutil.copy(
            os.path.normpath(PYMLINK_VERSION+'/'+arch_dir+linux_lib_name),
            os.path.normpath(linux_lib_path+linux_lib_name)
        )
    except OSError:
        print('...failed. - try to run setup script with root privileges')
        sys.exit(1)

elif os_name == 'Darwin':
    # copy lib to standard macos location
    try:
        if not os.path.exists(darwin_lib_path):
            os.makedirs(darwin_lib_path)

        print(
            'copying file '+PYMLINK_VERSION
            + '/'+arch_dir+darwin_lib_name
            + ' to '+darwin_lib_path
        )
        shutil.copy(
            os.path.normpath(PYMLINK_VERSION+'/'+arch_dir+darwin_lib_name),
            os.path.normpath(darwin_lib_path+darwin_lib_name))
    except OSError:
        print('...failed. - try to run setup script with root privileges')
        sys.exit(1)
else:
    print('Your operating system is not supported!')
    sys.exit(1)

setup(
    name='PyMLink',
    version='1.3.0',
    author='Lukas Wit',
    author_email='support@embedded-solutions.pl',
    url='www.microdaq.org',
    description='Python 2.6 and above binding of MLink library.',
    license='BSD',
    packages=[PYMLINK_VERSION],
    package_dir={PYMLINK_VERSION: PYMLINK_VERSION},
    package_data=pack_data,
    extras_require={'demos': demos_dependencies}
)
