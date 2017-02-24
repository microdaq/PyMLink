# PyMLink installation script
# visit site www.microdaq.org
# author Witczenko
# email witczenko@gmail.com

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

# Download needed binaries
mlink_lib = lib_ver+lib_ext
pack_data = {PYMLINK_VERSION: [mlink_lib]}


# TODO: Dont forget to change url after tests!
try:
    url = "https://github.com/microdaq/MLink/raw/upgrade_test/bin/"+os_name+"/"+mlink_lib

    print 'Downloading MLink library from ' + url
    bin = urllib2.urlopen(url)

    mlink_lib = lib_prefix + mlink_lib
    with open(os.path.normpath(PYMLINK_VERSION+'/'+mlink_lib), 'wb') as output:
        output.write(bin.read())
    print '...done.'

    #if linux then copy lib to standard location
    if os_name == 'Linux':
        pack_data = {}
        linux_lib_path = '/usr/lib/'
        try:
            print 'Moving file '+PYMLINK_VERSION+'/'+mlink_lib+' to '+linux_lib_path
            shutil.move(os.path.normpath(PYMLINK_VERSION+'/'+mlink_lib), os.path.normpath(linux_lib_path+mlink_lib))
        except:
            print '...failed.'
            sys.exit()
except:
    print 'Cannot download MLink library. Try run setup script again.'
    sys.exit()

tmp_dir = ''

# TODO: Fill metadata
setup(name='PyMLink',
      version='1.0',
      author='Witczenko',
      author_email='witczenko@gmail.com',
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