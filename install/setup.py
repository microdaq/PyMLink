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
if sys.version_info.major != 2 and sys.version_info.minor != 7:
    print 'Run this script with Python2.7!'
    sys.exit(1)

PYMLINK_VERSION = 'py_mlink'
os_name = platform.system()
lib_ext = None

# Check OS
lib_prefix = ''
if os_name == 'Windows':
    lib_ext = '.dll'
elif os_name == 'Linux':
    lib_ext = '.so'
    lib_prefix = 'lib'
else:
    print 'This operating system is not supported!'
    exit

# Check python platform version
if platform.architecture()[0] == '32bit':
    lib_ver = 'MLink32'
elif platform.architecture()[0] == '64bit':
    lib_ver = 'MLink64'
else:
    print 'This platform is not supported!'
    sys.exit()

mlink_lib = lib_ver+lib_ext
pack_data = {PYMLINK_VERSION: [mlink_lib]}

# if linux then copy lib to standard location
if os_name == 'Linux':
    pack_data = {}
    linux_lib_path = '/usr/lib/'
    try:
        print 'copying file '+PYMLINK_VERSION+'/'+mlink_lib+' to '+linux_lib_path
        shutil.copy(os.path.normpath(PYMLINK_VERSION+'/'+mlink_lib), os.path.normpath(linux_lib_path+'lib'+mlink_lib))
    except:
        print '...failed.'
        sys.exit()

tmp_dir = ''
setup(name='PyMLink',
      version='1.1.1',
      author='Lukas Wit',
      author_email='lukas.w@embedded-solutions.pl',
      url='www.microdaq.org',
      description='Python2.7 binding of MLink library.',
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
