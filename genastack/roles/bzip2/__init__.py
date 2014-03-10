# =============================================================================
# Copyright [2013] [Kevin Carter]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================
import os

from genastack import roles


TEMP_PATH = roles.return_temp_dir()
WORK_PATH = roles.return_rax_dir()
LIBS_PATH = roles.return_rax_dir(path='lib')


BZIP_URL = 'http://www.bzip.org/1.0.6/bzip2-1.0.6.tar.gz'


INSTALL_COMMANDS = [
    'make',
    'make install PREFIX=%s' % WORK_PATH
]


BUILD_DATA = {
    'bzip2': {
        'help': 'Install upstream bzip2.',
        'build': {
            'get': {
                'url': BZIP_URL,
                'path': TEMP_PATH,
                'name': 'bzip2-1.0.6.tgz',
                'md5sum': '00b516f4704d4a7cb50a1d97e6e8e15b',
                'uncompress': True
            },
            'not_if_exists': os.path.join(LIBS_PATH, 'libbz2.a'),
            'build_commands': INSTALL_COMMANDS,
        }
    }
}
