# =============================================================================
# Copyright [2013] [Kevin Carter]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================
from genastack.common import utils


ARGS = utils.get_role_config('openssl')
PROJECT_URL = ARGS.get(
    'project_url', 'http://www.openssl.org/source/openssl-1.0.1g.tar.gz'
)

TEMP_PATH = utils.return_temp_dir()
WORK_PATH = utils.return_rax_dir()
OPENSSL_PATH = utils.return_rax_dir(path='openstack/openssl')


INSTALL_COMMANDS = [
    './config --prefix=%s --openssldir=%s enable-shared -no-ssl2'
    % (WORK_PATH, OPENSSL_PATH),
    'make depend',
    'make install'
]


BUILD_DATA = {
    'openssl': {
        'help': 'Install upstream openssl.',
        'build': [
            {
                'get': {
                    'url': PROJECT_URL,
                    'path': TEMP_PATH,
                    'name': 'openssl-1.0.1g.tgz',
                    'md5sum': 'de62b43dfcd858e66a74bee1c834e959',
                    'uncompress': True
                },
                'not_if_exists': OPENSSL_PATH,
                'build_commands': INSTALL_COMMANDS,
            }
        ]
    }
}
