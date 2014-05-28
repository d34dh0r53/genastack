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

from genastack.common import utils


ARGS = utils.get_role_config('openssl')
PROJECT_URL = ARGS.get(
    'project_url',
    'http://ftp.postgresql.org/pub/source/v9.2.7/postgresql-9.2.7.tar.gz'
)


TEMP_PATH = utils.return_temp_dir()
WORK_PATH = utils.return_rax_dir()
LIBS_PATH = utils.return_rax_dir(path='openstack/lib')
INCLUDE_PATH = utils.return_rax_dir(path='openstack/include')


NAME = 'postgresql-9.2.7.tgz'


INSTALL_COMMANDS = [
    './configure --prefix=%s' % WORK_PATH,
    'make install'
]


EXPORTS = [
    'CFLAGS=-I%s -I/usr/include/x86_64-linux-gnu' % INCLUDE_PATH,
    'LDFLAGS=-L%s -L/usr/lib/x86_64-linux-gnu' % LIBS_PATH,
    'LD_RUN_PATH=%s' % LIBS_PATH
]


BUILD_DATA = {
    'postgres_connector': {
        'help': 'Install upstream postgresql_connector.',
        'build': [
            {
                'get': {
                    'url': PROJECT_URL,
                    'path': TEMP_PATH,
                    'name': NAME,
                    'md5sum': 'a61a63fc08b0b27a43b6ca325f49ab4b',
                    'uncompress': True
                },
                'export': EXPORTS,
                'not_if_exists': os.path.join(LIBS_PATH, 'postgresql'),
                'build_commands': INSTALL_COMMANDS,
            },

        ],
        'package_install': {
            'apt': {
                'packages': [
                    'bison',
                    'flex'
                ]
            }
        }
    }
}
