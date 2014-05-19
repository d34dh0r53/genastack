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
from cloudlib import parse_ini

# Check to see if our System Config File Exists
CONFIG = parse_ini.ConfigurationSetup(log_name='genastack-system')
ARGS = CONFIG.config_args(section='berkeley-db')
PROJECT_URL = ARGS.get(
    'project_url', 'http://download.oracle.com/berkeley-db/db-6.0.30.tar.gz'
)

TEMP_PATH = utils.return_temp_dir()
WORK_PATH = utils.return_rax_dir()
LIBS_PATH = utils.return_rax_dir(path='openstack/lib')


INSTALL_COMMANDS = [
    './dist/configure --prefix=%s --with-sql'
    ' --enable-tcl --with-tcl=/usr/lib' % WORK_PATH,
    'make',
    'make install'
]


BUILD_DATA = {
    'berkeley_db': {
        'help': 'Install upstream berkeley DBM.',
        'build': [
            {
                'get': {
                    'url': PROJECT_URL,
                    'path': TEMP_PATH,
                    'name': 'db-6.0.30.tgz',
                    'md5sum': 'ad28eb86ad3203b5422844db179c585b',
                    'uncompress': True
                },
                'not_if_exists': '%s/libdb.so' % LIBS_PATH,
                'build_commands': INSTALL_COMMANDS,
                'export': [
                    'LD_RUN_PATH=%s' % LIBS_PATH,
                ],
            }
        ],
        'package_install': {
            'apt': [
                'libxft-dev',
                'tcl8.5-dev',
                'tk8.5-dev'
            ]
        }
    }
}
