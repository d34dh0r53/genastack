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


ARGS = utils.get_role_config('mysql-connector')
BRANCH = ARGS.get('branch', 'master')
PROJECT_URL = ARGS.get(
    'project_url',
    'http://dev.mysql.com/get/Downloads/Connector-C'
    '/mysql-connector-c-6.1.3-src.tar.gz'
)


TEMP_PATH = utils.return_temp_dir()
WORK_PATH = utils.return_rax_dir()
LIBS_PATH = utils.return_rax_dir(path='openstack/lib')


NAME = 'mysql-connector-c-6.1.3-src.tgz'


INSTALL_COMMANDS = [
    'cmake -G "Unix Makefiles"',
    'cmake -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Debug',
    'cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX=%s' % WORK_PATH,
    'make install'
]


BUILD_DATA = {
    'mysql_connector': {
        'help': 'Install upstream mysql_connector_c.',
        'build': [
            {
                'get': {
                    'url': PROJECT_URL,
                    'path': TEMP_PATH,
                    'name': NAME,
                    'md5sum': '490e2dd5d4f86a20a07ba048d49f36b2',
                    'uncompress': True
                },
                'export': [
                    'LD_RUN_PATH=%s' % LIBS_PATH
                ],
                'not_if_exists': os.path.join(LIBS_PATH, 'libmysqlclient.so'),
                'build_commands': INSTALL_COMMANDS,
            }
        ],
        'package_install': {
            'apt': {
                'packages': [
                    'cmake'
                ]
            }
        }
    }
}
