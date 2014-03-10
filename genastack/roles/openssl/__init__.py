# =============================================================================
# Copyright [2013] [Kevin Carter]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================
from genastack import roles


TEMP_PATH = roles.return_temp_dir()
WORK_PATH = roles.return_rax_dir()
OPENSSL_PATH = roles.return_rax_dir(path='openssl')


OPEN_SSL_URL = 'http://www.openssl.org/source/openssl-1.0.1f.tar.gz'


INSTALL_COMMANDS = [
    './config --prefix=%s --openssldir=%s enable-shared -no-ssl2'
    % (WORK_PATH, OPENSSL_PATH),
    'make depend',
    'make install'
]


BUILD_DATA = {
    'openssl': {
        'help': 'Install upstream openssl.',
        'build': {
            'get': {
                'url': OPEN_SSL_URL,
                'path': TEMP_PATH,
                'name': 'openssl-1.0.1f.tgz',
                'md5sum': 'f26b09c028a0541cab33da697d522b25',
                'uncompress': True
            },
            'not_if_exists': OPENSSL_PATH,
            'build_commands': INSTALL_COMMANDS,
        }
    }
}