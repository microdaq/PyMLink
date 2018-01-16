'''
Do not modify this file. Auto generated.
'''

__docformat__ =  'restructuredtext'

# Begin preamble

import ctypes, os, sys
from ctypes import *
import platform
import inspect
import py_mlink

_int_types = (c_int16, c_int32)
if hasattr(ctypes, 'c_int64'):
    # Some builds of ctypes apparently do not have c_int64
    # defined; it's a pretty good bet that these builds do not
    # have 64-bit pointers.
    _int_types += (c_int64,)
for t in _int_types:
    if sizeof(t) == sizeof(c_size_t):
        c_ptrdiff_t = t
del t
del _int_types

class c_void(Structure):
    # c_void_p is a buggy return type, converting to int, so
    # POINTER(None) == c_void_p is actually written as
    # POINTER(c_void), so it can be treated as a real pointer.
    _fields_ = [('dummy', c_int)]

def POINTER(obj):
    p = ctypes.POINTER(obj)

    # Convert None to a real NULL pointer to work around bugs
    # in how ctypes handles None on 64-bit platforms
    if not isinstance(p.from_param, classmethod):
        def from_param(cls, x):
            if x is None:
                return cls()
            else:
                return x
        p.from_param = classmethod(from_param)

    return p

class UserString:
    def __init__(self, seq):
        if isinstance(seq, basestring):
            self.data = seq
        elif isinstance(seq, UserString):
            self.data = seq.data[:]
        else:
            self.data = str(seq)
    def __str__(self): return str(self.data)
    def __repr__(self): return repr(self.data)
    def __int__(self): return int(self.data)
    def __long__(self): return long(self.data)
    def __float__(self): return float(self.data)
    def __complex__(self): return complex(self.data)
    def __hash__(self): return hash(self.data)

    def __cmp__(self, string):
        if isinstance(string, UserString):
            return cmp(self.data, string.data)
        else:
            return cmp(self.data, string)
    def __contains__(self, char):
        return char in self.data

    def __len__(self): return len(self.data)
    def __getitem__(self, index): return self.__class__(self.data[index])
    def __getslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        return self.__class__(self.data[start:end])

    def __add__(self, other):
        if isinstance(other, UserString):
            return self.__class__(self.data + other.data)
        elif isinstance(other, basestring):
            return self.__class__(self.data + other)
        else:
            return self.__class__(self.data + str(other))
    def __radd__(self, other):
        if isinstance(other, basestring):
            return self.__class__(other + self.data)
        else:
            return self.__class__(str(other) + self.data)
    def __mul__(self, n):
        return self.__class__(self.data*n)
    __rmul__ = __mul__
    def __mod__(self, args):
        return self.__class__(self.data % args)

    # the following methods are defined in alphabetical order:
    def capitalize(self): return self.__class__(self.data.capitalize())
    def center(self, width, *args):
        return self.__class__(self.data.center(width, *args))
    def count(self, sub, start=0, end=sys.maxint):
        return self.data.count(sub, start, end)
    def decode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.decode(encoding, errors))
            else:
                return self.__class__(self.data.decode(encoding))
        else:
            return self.__class__(self.data.decode())
    def encode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.encode(encoding, errors))
            else:
                return self.__class__(self.data.encode(encoding))
        else:
            return self.__class__(self.data.encode())
    def endswith(self, suffix, start=0, end=sys.maxint):
        return self.data.endswith(suffix, start, end)
    def expandtabs(self, tabsize=8):
        return self.__class__(self.data.expandtabs(tabsize))
    def find(self, sub, start=0, end=sys.maxint):
        return self.data.find(sub, start, end)
    def index(self, sub, start=0, end=sys.maxint):
        return self.data.index(sub, start, end)
    def isalpha(self): return self.data.isalpha()
    def isalnum(self): return self.data.isalnum()
    def isdecimal(self): return self.data.isdecimal()
    def isdigit(self): return self.data.isdigit()
    def islower(self): return self.data.islower()
    def isnumeric(self): return self.data.isnumeric()
    def isspace(self): return self.data.isspace()
    def istitle(self): return self.data.istitle()
    def isupper(self): return self.data.isupper()
    def join(self, seq): return self.data.join(seq)
    def ljust(self, width, *args):
        return self.__class__(self.data.ljust(width, *args))
    def lower(self): return self.__class__(self.data.lower())
    def lstrip(self, chars=None): return self.__class__(self.data.lstrip(chars))
    def partition(self, sep):
        return self.data.partition(sep)
    def replace(self, old, new, maxsplit=-1):
        return self.__class__(self.data.replace(old, new, maxsplit))
    def rfind(self, sub, start=0, end=sys.maxint):
        return self.data.rfind(sub, start, end)
    def rindex(self, sub, start=0, end=sys.maxint):
        return self.data.rindex(sub, start, end)
    def rjust(self, width, *args):
        return self.__class__(self.data.rjust(width, *args))
    def rpartition(self, sep):
        return self.data.rpartition(sep)
    def rstrip(self, chars=None): return self.__class__(self.data.rstrip(chars))
    def split(self, sep=None, maxsplit=-1):
        return self.data.split(sep, maxsplit)
    def rsplit(self, sep=None, maxsplit=-1):
        return self.data.rsplit(sep, maxsplit)
    def splitlines(self, keepends=0): return self.data.splitlines(keepends)
    def startswith(self, prefix, start=0, end=sys.maxint):
        return self.data.startswith(prefix, start, end)
    def strip(self, chars=None): return self.__class__(self.data.strip(chars))
    def swapcase(self): return self.__class__(self.data.swapcase())
    def title(self): return self.__class__(self.data.title())
    def translate(self, *args):
        return self.__class__(self.data.translate(*args))
    def upper(self): return self.__class__(self.data.upper())
    def zfill(self, width): return self.__class__(self.data.zfill(width))

class MutableString(UserString):
    """mutable string objects

    Python strings are immutable objects.  This has the advantage, that
    strings may be used as dictionary keys.  If this property isn't needed
    and you insist on changing string values in place instead, you may cheat
    and use MutableString.

    But the purpose of this class is an educational one: to prevent
    people from inventing their own mutable string class derived
    from UserString and than forget thereby to remove (override) the
    __hash__ method inherited from UserString.  This would lead to
    errors that would be very hard to track down.

    A faster and better solution is to rewrite your program using lists."""
    def __init__(self, string=""):
        self.data = string
    def __hash__(self):
        raise TypeError("unhashable type (it is mutable)")
    def __setitem__(self, index, sub):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + sub + self.data[index+1:]
    def __delitem__(self, index):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + self.data[index+1:]
    def __setslice__(self, start, end, sub):
        start = max(start, 0); end = max(end, 0)
        if isinstance(sub, UserString):
            self.data = self.data[:start]+sub.data+self.data[end:]
        elif isinstance(sub, basestring):
            self.data = self.data[:start]+sub+self.data[end:]
        else:
            self.data =  self.data[:start]+str(sub)+self.data[end:]
    def __delslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        self.data = self.data[:start] + self.data[end:]
    def immutable(self):
        return UserString(self.data)
    def __iadd__(self, other):
        if isinstance(other, UserString):
            self.data += other.data
        elif isinstance(other, basestring):
            self.data += other
        else:
            self.data += str(other)
        return self
    def __imul__(self, n):
        self.data *= n
        return self

class String(MutableString, Union):

    _fields_ = [('raw', POINTER(c_char)),
                ('data', c_char_p)]

    def __init__(self, obj=""):
        if isinstance(obj, (str, unicode, UserString)):
            self.data = str(obj)
        else:
            self.raw = obj

    def __len__(self):
        return self.data and len(self.data) or 0

    def from_param(cls, obj):
        # Convert None or 0
        if obj is None or obj == 0:
            return cls(POINTER(c_char)())

        # Convert from String
        elif isinstance(obj, String):
            return obj

        # Convert from str
        elif isinstance(obj, str):
            return cls(obj)

        # Convert from c_char_p
        elif isinstance(obj, c_char_p):
            return obj

        # Convert from POINTER(c_char)
        elif isinstance(obj, POINTER(c_char)):
            return obj

        # Convert from raw pointer
        elif isinstance(obj, int):
            return cls(cast(obj, POINTER(c_char)))

        # Convert from object
        else:
            return String.from_param(obj._as_parameter_)
    from_param = classmethod(from_param)

def ReturnString(obj, func=None, arguments=None):
    return String.from_param(obj)

# As of ctypes 1.0, ctypes does not support custom error-checking
# functions on callbacks, nor does it support custom datatypes on
# callbacks, so we must ensure that all callbacks return
# primitive datatypes.
#
# Non-primitive return values wrapped with UNCHECKED won't be
# typechecked, and will be converted to c_void_p.
def UNCHECKED(type):
    if (hasattr(type, "_type_") and isinstance(type._type_, str)
        and type._type_ != "P"):
        return type
    else:
        return c_void_p

# ctypes doesn't have direct support for variadic functions, so we have to write
# our own wrapper class
class _variadic_function(object):
    def __init__(self,func,restype,argtypes):
        self.func=func
        self.func.restype=restype
        self.argtypes=argtypes
    def _as_parameter_(self):
        # So we can pass this variadic function as a function pointer
        return self.func
    def __call__(self,*args):
        fixed_args=[]
        i=0
        for argtype in self.argtypes:
            # Typecheck what we can
            fixed_args.append(argtype.from_param(args[i]))
            i+=1
        return self.func(*fixed_args+list(args[i:]))

# End preamble

_libs = {}
_libdirs = []

# Begin loader

# ----------------------------------------------------------------------------
# Copyright (c) 2008 David James
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

import os.path, re, sys, glob
import ctypes
import ctypes.util

def _environ_path(name):
    if name in os.environ:
        return os.environ[name].split(":")
    else:
        return []

class LibraryLoader(object):
    def __init__(self):
        self.other_dirs=[]

    def load_library(self,libname):
        """Given the name of a library, load it."""
        paths = self.getpaths(libname)

        for path in paths:
            if os.path.exists(path):
                return self.load(path)

        raise ImportError("%s not found." % libname)

    def load(self,path):
        """Given a path to a library, load it."""
        try:
            # Darwin requires dlopen to be called with mode RTLD_GLOBAL instead
            # of the default RTLD_LOCAL.  Without this, you end up with
            # libraries not being loadable, resulting in "Symbol not found"
            # errors
            if sys.platform == 'darwin':
                return ctypes.CDLL(path, ctypes.RTLD_GLOBAL)
            else:
                return ctypes.cdll.LoadLibrary(path)
        except OSError,e:
            raise ImportError(e)

    def getpaths(self,libname):
        """Return a list of paths where the library might be found."""
        if os.path.isabs(libname):
            yield libname

        else:
            for path in self.getplatformpaths(libname):
                yield path

            path = ctypes.util.find_library(libname)
            if path: yield path

    def getplatformpaths(self, libname):
        return []

# Darwin (Mac OS X)

class DarwinLibraryLoader(LibraryLoader):
    name_formats = ["lib%s.dylib", "lib%s.so", "lib%s.bundle", "%s.dylib",
                "%s.so", "%s.bundle", "%s"]

    def getplatformpaths(self,libname):
        if os.path.pathsep in libname:
            names = [libname]
        else:
            names = [format % libname for format in self.name_formats]

        for dir in self.getdirs(libname):
            for name in names:
                yield os.path.join(dir,name)

    def getdirs(self,libname):
        '''Implements the dylib search as specified in Apple documentation:

        http://developer.apple.com/documentation/DeveloperTools/Conceptual/
            DynamicLibraries/Articles/DynamicLibraryUsageGuidelines.html

        Before commencing the standard search, the method first checks
        the bundle's ``Frameworks`` directory if the application is running
        within a bundle (OS X .app).
        '''

        dyld_fallback_library_path = _environ_path("DYLD_FALLBACK_LIBRARY_PATH")
        if not dyld_fallback_library_path:
            dyld_fallback_library_path = [os.path.expanduser('~/lib'),
                                          '/usr/local/lib', '/usr/lib']

        dirs = []

        if '/' in libname:
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))
        else:
            dirs.extend(_environ_path("LD_LIBRARY_PATH"))
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))

        dirs.extend(self.other_dirs)
        dirs.append(".")

        if hasattr(sys, 'frozen') and sys.frozen == 'macosx_app':
            dirs.append(os.path.join(
                os.environ['RESOURCEPATH'],
                '..',
                'Frameworks'))

        dirs.extend(dyld_fallback_library_path)

        return dirs

# Posix

class PosixLibraryLoader(LibraryLoader):
    _ld_so_cache = None

    def _create_ld_so_cache(self):
        # Recreate search path followed by ld.so.  This is going to be
        # slow to build, and incorrect (ld.so uses ld.so.cache, which may
        # not be up-to-date).  Used only as fallback for distros without
        # /sbin/ldconfig.
        #
        # We assume the DT_RPATH and DT_RUNPATH binary sections are omitted.

        directories = []
        for name in ("LD_LIBRARY_PATH",
                     "SHLIB_PATH", # HPUX
                     "LIBPATH", # OS/2, AIX
                     "LIBRARY_PATH", # BE/OS
                    ):
            if name in os.environ:
                directories.extend(os.environ[name].split(os.pathsep))
        directories.extend(self.other_dirs)
        directories.append(".")

        try: directories.extend([dir.strip() for dir in open('/etc/ld.so.conf')])
        except IOError: pass

        directories.extend(['/lib', '/usr/lib', '/lib64', '/usr/lib64'])

        cache = {}
        lib_re = re.compile(r'lib(.*)\.s[ol]')
        ext_re = re.compile(r'\.s[ol]$')
        for dir in directories:
            try:
                for path in glob.glob("%s/*.s[ol]*" % dir):
                    file = os.path.basename(path)

                    # Index by filename
                    if file not in cache:
                        cache[file] = path

                    # Index by library name
                    match = lib_re.match(file)
                    if match:
                        library = match.group(1)
                        if library not in cache:
                            cache[library] = path
            except OSError:
                pass

        self._ld_so_cache = cache

    def getplatformpaths(self, libname):
        if self._ld_so_cache is None:
            self._create_ld_so_cache()

        result = self._ld_so_cache.get(libname)
        if result: yield result

        path = ctypes.util.find_library(libname)
        if path: yield os.path.join("/lib",path)

# Windows

class _WindowsLibrary(object):
    def __init__(self, path):
        self.cdll = ctypes.cdll.LoadLibrary(path)
        self.windll = ctypes.windll.LoadLibrary(path)

    def __getattr__(self, name):
        try: return getattr(self.cdll,name)
        except AttributeError:
            try: return getattr(self.windll,name)
            except AttributeError:
                raise

class WindowsLibraryLoader(LibraryLoader):
    name_formats = ["%s.dll", "lib%s.dll", "%slib.dll"]

    def load_library(self, libname):
        try:
            result = LibraryLoader.load_library(self, libname)
        except ImportError:
            result = None
            if os.path.sep not in libname:
                for name in self.name_formats:
                    try:
                        result = getattr(ctypes.cdll, name % libname)
                        if result:
                            break
                    except WindowsError:
                        result = None
            if result is None:
                try:
                    result = getattr(ctypes.cdll, libname)
                except WindowsError:
                    result = None
            if result is None:
                raise ImportError("%s not found." % libname)
        return result

    def load(self, path):
        return _WindowsLibrary(path)

    def getplatformpaths(self, libname):
        if os.path.sep not in libname:
            for name in self.name_formats:
                dll_in_current_dir = os.path.abspath(name % libname)
                if os.path.exists(dll_in_current_dir):
                    yield dll_in_current_dir
                path = ctypes.util.find_library(name % libname)
                if path:
                    yield path

# Platform switching

# If your value of sys.platform does not appear in this dict, please contact
# the Ctypesgen maintainers.

loaderclass = {
    "darwin":   DarwinLibraryLoader,
    "cygwin":   WindowsLibraryLoader,
    "win32":    WindowsLibraryLoader
}

loader = loaderclass.get(sys.platform, PosixLibraryLoader)()

def add_library_search_dirs(other_dirs):
    loader.other_dirs = other_dirs

load_library = loader.load_library

del loaderclass

# End loader

add_library_search_dirs([])

# Begin libraries
if platform.architecture()[0] == '32bit':
        libname_ver = 'MLink32'
elif platform.architecture()[0] == '64bit':
        libname_ver = 'MLink64'
else:
        libname_ver = 'MLink'+platform.architecture()[0]

libpath = ''
if platform.system() == 'Windows':
    libpath = os.path.dirname(inspect.getfile(py_mlink))+'/'

libname_ver = libpath+libname_ver
_libs["MLink"] = load_library(libname_ver)


# 1 libraries
# End libraries

# No modules

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 36
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_error'):
        continue
    mlink_error = _lib.mlink_error
    mlink_error.argtypes = [c_int]
    if sizeof(c_int) == sizeof(c_void_p):
        mlink_error.restype = ReturnString
    else:
        mlink_error.restype = String
        mlink_error.errcheck = ReturnString
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 37
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_version'):
        continue
    mlink_version = _lib.mlink_version
    mlink_version.argtypes = [POINTER(c_int)]
    if sizeof(c_int) == sizeof(c_void_p):
        mlink_version.restype = ReturnString
    else:
        mlink_version.restype = String
        mlink_version.errcheck = ReturnString
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 38
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_hwid'):
        continue
    mlink_hwid = _lib.mlink_hwid
    mlink_hwid.argtypes = [POINTER(c_int), POINTER(c_int)]
    mlink_hwid.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 40
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_connect'):
        continue
    mlink_connect = _lib.mlink_connect
    mlink_connect.argtypes = [String, c_uint16, POINTER(c_int)]
    mlink_connect.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 41
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_disconnect'):
        continue
    mlink_disconnect = _lib.mlink_disconnect
    mlink_disconnect.argtypes = [c_int]
    mlink_disconnect.restype = c_int

    break

for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_disconnect_all'):
        continue
    mlink_disconnect_all = _lib.mlink_disconnect_all
    mlink_disconnect_all.restype = c_void
    break

for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_dsp_run'):
        continue
    mlink_dsp_load = _lib.mlink_dsp_load
    mlink_dsp_load.argtypes = [POINTER(c_int), String, String]
    mlink_dsp_load.restype = c_int
    break


#EXTERNC MDAQ_API int mlink_dsp_run(int *link_fd,  const char *dsp_binary_path, double period);
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_dsp_run'):
        continue
    mlink_dsp_run = _lib.mlink_dsp_run
    mlink_dsp_run.argtypes = [POINTER(c_int), String, c_double]
    mlink_dsp_run.restype = c_int
    break

#EXTERNC MDAQ_API int mlink_dsp_signal_read(int signal_id, int signal_size, double *data, int data_size, int timeout);
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_dsp_signal_read'):
        continue
    mlink_dsp_signal_read = _lib.mlink_dsp_signal_read
    mlink_dsp_signal_read.argtypes = [c_int, c_int, POINTER(c_double), c_int, c_int]
    mlink_dsp_signal_read.restype = c_int
    break

#EXTERNC MDAQ_API int mlink_dsp_mem_write(int *link_fd, int start_idx, int len, float *data);
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_dsp_mem_write'):
        continue
    mlink_dsp_mem_write = _lib.mlink_dsp_mem_write
    mlink_dsp_mem_write.argtypes = [POINTER(c_int), c_int, c_int, POINTER(c_float)]
    mlink_dsp_mem_write.restype = c_int
    break

#EXTERNC MDAQ_API int mlink_dsp_stop(int *link_fd );
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_dsp_stop'):
        continue
    mlink_dsp_stop = _lib.mlink_dsp_stop
    mlink_dsp_stop.argtypes = [POINTER(c_int)]
    mlink_dsp_stop.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 50
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_dio_set_func'):
        continue
    mlink_dio_set_func = _lib.mlink_dio_set_func
    mlink_dio_set_func.argtypes = [POINTER(c_int), c_uint8, c_uint8]
    mlink_dio_set_func.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 51
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_dio_set_dir'):
        continue
    mlink_dio_set_dir = _lib.mlink_dio_set_dir
    mlink_dio_set_dir.argtypes = [POINTER(c_int), c_uint8, c_uint8, c_uint8]
    mlink_dio_set_dir.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 52
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_dio_write'):
        continue
    mlink_dio_write = _lib.mlink_dio_write
    mlink_dio_write.argtypes = [POINTER(c_int), c_uint8, c_uint8]
    mlink_dio_write.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 53
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_dio_read'):
        continue
    mlink_dio_read = _lib.mlink_dio_read
    mlink_dio_read.argtypes = [POINTER(c_int), c_uint8, POINTER(c_uint8)]
    mlink_dio_read.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 54
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_led_write'):
        continue
    mlink_led_write = _lib.mlink_led_write
    mlink_led_write.argtypes = [POINTER(c_int), c_uint8, c_uint8]
    mlink_led_write.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 55
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_func_read'):
        continue
    mlink_func_read = _lib.mlink_func_read
    mlink_func_read.argtypes = [POINTER(c_int), c_uint8, POINTER(c_uint8)]
    mlink_func_read.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 58
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_enc_read'):
        continue
    mlink_enc_read = _lib.mlink_enc_read
    mlink_enc_read.argtypes = [POINTER(c_int), c_uint8, POINTER(c_uint8), POINTER(c_int32)]
    mlink_enc_read.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 59
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_enc_init'):
        continue
    mlink_enc_init = _lib.mlink_enc_init
    mlink_enc_init.argtypes = [POINTER(c_int), c_uint8, c_int32]
    mlink_enc_init.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 62
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_pwm_init'):
        continue
    mlink_pwm_init = _lib.mlink_pwm_init
    mlink_pwm_init.argtypes = [POINTER(c_int), c_uint8, c_uint32, c_uint8, c_float, c_float]
    mlink_pwm_init.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 63
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_pwm_write'):
        continue
    mlink_pwm_write = _lib.mlink_pwm_write
    mlink_pwm_write.argtypes = [POINTER(c_int), c_uint8, c_float, c_float]
    mlink_pwm_write.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 66
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_pru_exec'):
        continue
    mlink_pru_exec = _lib.mlink_pru_exec
    mlink_pru_exec.argtypes = [POINTER(c_int), String, c_uint8, c_uint8]
    mlink_pru_exec.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 67
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_pru_stop'):
        continue
    mlink_pru_stop = _lib.mlink_pru_stop
    mlink_pru_stop.argtypes = [POINTER(c_int), c_uint8]
    mlink_pru_stop.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 68
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_pru_reg_get'):
        continue
    mlink_pru_reg_get = _lib.mlink_pru_reg_get
    mlink_pru_reg_get.argtypes = [POINTER(c_int), c_uint8, c_uint8, POINTER(c_uint32)]
    mlink_pru_reg_get.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 69
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_pru_reg_set'):
        continue
    mlink_pru_reg_set = _lib.mlink_pru_reg_set
    mlink_pru_reg_set.argtypes = [POINTER(c_int), c_uint8, c_uint8, c_uint32]
    mlink_pru_reg_set.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 72
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_uart_config'):
        continue
    mlink_uart_config = _lib.mlink_uart_config
    mlink_uart_config.argtypes = [POINTER(c_int), c_uint8, c_uint8, c_uint8, c_uint8, c_uint32]
    mlink_uart_config.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 73
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_uart_read'):
        continue
    mlink_uart_read = _lib.mlink_uart_read
    mlink_uart_read.argtypes = [POINTER(c_int), c_uint8, String, c_uint32, c_int32]
    mlink_uart_read.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 74
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_uart_write'):
        continue
    mlink_uart_write = _lib.mlink_uart_write
    mlink_uart_write.argtypes = [POINTER(c_int), c_uint8, String, c_uint32]
    mlink_uart_write.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 75
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_uart_close'):
        continue
    mlink_uart_close = _lib.mlink_uart_close
    mlink_uart_close.argtypes = [POINTER(c_int), c_uint8]
    mlink_uart_close.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 78
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_hs_ai_init'):
        continue
    mlink_hs_ai_init = _lib.mlink_hs_ai_init
    mlink_hs_ai_init.argtypes = [POINTER(c_int)]
    mlink_hs_ai_init.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 79
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_hs_ai_read'):
        continue
    mlink_hs_ai_read = _lib.mlink_hs_ai_read
    mlink_hs_ai_read.argtypes = [POINTER(c_int), c_uint32, c_uint32, c_uint32, POINTER(c_double)]
    mlink_hs_ai_read.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 82
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_ai_read'):
        continue
    mlink_ai_read = _lib.mlink_ai_read
    # mlink_ai_read(int * link_fd, uint8_t * ch, uint8_t ch_count, double * range, uint8_t * mode, double * data );
    mlink_ai_read.argtypes = [POINTER(c_int), POINTER(c_uint8), c_uint8, POINTER(c_double), POINTER(c_uint8),
                              POINTER(c_double)]
    mlink_ai_read.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 83
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_ao_write'):
        continue
    mlink_ao_write = _lib.mlink_ao_write
    # int mlink_ao_write( int *link_fd, uint8_t *ch, uint8_t ch_count, double *range, uint8_t mode, double *data );
    mlink_ao_write.argtypes = [POINTER(c_int), POINTER(c_uint8), c_uint8, POINTER(c_double), c_uint8, POINTER(c_double)]
    mlink_ao_write.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 84
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_ao_ch_config'):
        continue
    mlink_ao_ch_config = _lib.mlink_ao_ch_config
    mlink_ao_ch_config.argtypes = [POINTER(c_int), POINTER(c_uint8), c_uint8, POINTER(c_uint8)]
    mlink_ao_ch_config.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 86
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_ai_scan_init'):
        continue
    mlink_ai_scan_init = _lib.mlink_ai_scan_init
    # mlink_ai_scan_init(int *link_fd, uint8_t *ch, uint8_t ch_count, double *range, uint8_t *mode, float *rate, float duration);
    mlink_ai_scan_init.argtypes = [POINTER(c_int), POINTER(c_uint8), c_uint8, POINTER(c_double), POINTER(c_uint8),
                                   POINTER(c_float), c_float]
    mlink_ai_scan_init.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 87
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_ai_scan'):
        continue
    mlink_ai_scan = _lib.mlink_ai_scan
    mlink_ai_scan.argtypes = [POINTER(c_double), c_uint32, c_int32]
    mlink_ai_scan.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 88
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_ai_scan_stop'):
        continue
    mlink_ai_scan_stop = _lib.mlink_ai_scan_stop
    mlink_ai_scan_stop.argtypes = []
    mlink_ai_scan_stop.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 90
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_pru_mem_set'):
        continue
    mlink_pru_mem_set = _lib.mlink_pru_mem_set
    mlink_pru_mem_set.argtypes = [POINTER(c_int), c_uint8, c_uint32, POINTER(c_uint8), c_uint32]
    mlink_pru_mem_set.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 91
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_pru_mem_get'):
        continue
    mlink_pru_mem_get = _lib.mlink_pru_mem_get
    mlink_pru_mem_get.argtypes = [POINTER(c_int), c_uint8, c_uint32, POINTER(c_char), c_uint32]
    mlink_pru_mem_get.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 92
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_get_obj_size'):
        continue
    mlink_get_obj_size = _lib.mlink_get_obj_size
    mlink_get_obj_size.argtypes = [POINTER(c_int), String, POINTER(c_uint32)]
    mlink_get_obj_size.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 93
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_get_obj'):
        continue
    mlink_get_obj = _lib.mlink_get_obj
    mlink_get_obj.argtypes = [POINTER(c_int), String, POINTER(None), c_uint32]
    mlink_get_obj.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 94
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_set_obj'):
        continue
    mlink_set_obj = _lib.mlink_set_obj
    mlink_set_obj.argtypes = [POINTER(c_int), String, POINTER(None), c_uint32]
    mlink_set_obj.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 95
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_mem_open'):
        continue
    mlink_mem_open = _lib.mlink_mem_open
    mlink_mem_open.argtypes = [POINTER(c_int), c_uint32, c_uint32]
    mlink_mem_open.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 96
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_mem_close'):
        continue
    mlink_mem_close = _lib.mlink_mem_close
    mlink_mem_close.argtypes = [POINTER(c_int), c_uint32, c_uint32]
    mlink_mem_close.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 97
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_mem_set'):
        continue
    mlink_mem_set = _lib.mlink_mem_set
    mlink_mem_set.argtypes = [POINTER(c_int), c_uint32, POINTER(c_int8), c_uint32]
    mlink_mem_set.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 98
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_mem_get'):
        continue
    mlink_mem_get = _lib.mlink_mem_get
    mlink_mem_get.argtypes = [POINTER(c_int), c_uint32, POINTER(c_int8), c_uint32]
    mlink_mem_get.restype = c_int
    break

for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_ao_scan_init'):
        continue
    # mlink_ao_scan_init(int *link_fd, uint8_t *ch, uint8_t ch_count, float *data, int data_size, double *range,
    # uint8_t stream_mode, float rate, float duration);
    mlink_ao_scan_init = _lib.mlink_ao_scan_init
    mlink_ao_scan_init.argtypes = [POINTER(c_int), POINTER(c_uint8), c_uint8, POINTER(c_float), c_int,
                                   POINTER(c_double), c_uint8, c_float, c_float]
    mlink_ao_scan_init.restype = c_int
    break

for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_ao_scan_data'):
        continue
    mlink_ao_scan_data = _lib.mlink_ao_scan_data
    # mlink_ao_scan_data(int *link_fd, uint8_t *ch, int ch_count, float *data, int data_size, uint8_t opt);
    mlink_ao_scan_data.argtypes = [POINTER(c_int), POINTER(c_uint8), c_int, POINTER(c_float), c_int, c_uint8]
    mlink_ao_scan_data.restype = c_int
    break

for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_ao_scan'):
        continue
    mlink_ao_scan = _lib.mlink_ao_scan
    mlink_ao_scan.argtypes = [POINTER(c_int)]
    mlink_ao_scan.restype = c_int
    break

for _lib in _libs.itervalues():
    if not hasattr(_lib, 'mlink_ao_scan_stop'):
        continue
    mlink_ao_scan_stop = _lib.mlink_ao_scan_stop
    mlink_ao_scan_stop.argtypes = [POINTER(c_int)]
    mlink_ao_scan_stop.restype = c_int
    break

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 15
try:
    AO_0_TO_5V = 0
except:
    pass

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 16
try:
    AO_0_TO_10V = 1
except:
    pass

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 17
try:
    AO_PLUS_MINUS_5V = 2
except:
    pass

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 18
try:
    AO_PLUS_MINUS_10V = 3
except:
    pass

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 19
try:
    AO_PLUS_MINUS_2V5 = 4
except:
    pass

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 22
try:
    AI_10V = 0
except:
    pass

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 23
try:
    AI_5V = 1
except:
    pass

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 27
try:
    AI_BIPOLAR = 0
except:
    pass

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 28
try:
    AI_UNIPOLAR = 1
except:
    pass

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 31
try:
    AI_SINGLE = 0
except:
    pass

# /home/witczenko/Downloads/Scilab-master/microdaq/etc/mlink/MLink/MLink2.h: 32
try:
    AI_DIFF = 1
except:
    pass

# No inserted files

