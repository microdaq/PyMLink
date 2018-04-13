# PyMLink installation script
# visit site www.microdaq.org
# Embedded-solutions, November 2017

from distutils.core import setup
import platform
import urllib2
import os
import sys
import shutil

# check python version
if sys.version_info[0] != 2 and sys.version_info[1] < 6:
    print 'Run this script with Python2.6/2.7!'
    sys.exit(1)

PYMLINK_VERSION = 'py_mlink'
os_name = platform.system()
lib_ext = None

arch_dir = ''

# Check python platform version
linux_lib_name = 'libmlink.so'
if platform.architecture()[0] == '32bit':
    win_lib_name = 'MLink32.dll'
    arch_dir = 'x86/'
elif platform.architecture()[0] == '64bit':
    win_lib_name = 'MLink64.dll'
    arch_dir = 'x64/'
else:
    print 'Your platform is not supported!'
    sys.exit()

# Check OS
if os_name == 'Windows':
    pack_data = {PYMLINK_VERSION: [win_lib_name]}
    shutil.copy(os.path.normpath(PYMLINK_VERSION+'/'+arch_dir+win_lib_name), os.path.normpath(PYMLINK_VERSION+'/'+win_lib_name))
elif os_name == 'Linux':
    pack_data = {}
    # in case of arm processors take another binary
    if platform.uname()[4].startswith('arm'):
       arch_dir = 'armel/'
    
    # if linux then copy lib to standard location
    linux_lib_path = '/usr/lib/'
    try:
        print 'copying file '+PYMLINK_VERSION+'/'+arch_dir+linux_lib_name+' to '+linux_lib_path
        shutil.copy(os.path.normpath(PYMLINK_VERSION+'/'+arch_dir+linux_lib_name), os.path.normpath(linux_lib_path+linux_lib_name))
    except:
        print '...failed.'
        sys.exit()
else:
    print 'Your operating system is not supported!'
    exit

setup(name='PyMLink',
      version='1.2.1',
      author='Lukas Wit',
      author_email='lukas.w@embedded-solutions.pl',
      url='www.microdaq.org',
      description='Python2.6/2.7 binding of MLink library.',
      license='BSD',
      packages = [PYMLINK_VERSION],
      package_dir = {PYMLINK_VERSION: PYMLINK_VERSION},
      package_data = pack_data,
      )

try:
    print 'Removing ', os.path.abspath('build')
    shutil.rmtree('build')
    print '...done.'
except:
    print '...failed.'
