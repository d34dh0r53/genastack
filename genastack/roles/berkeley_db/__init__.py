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


TEMP_PATH = utils.return_temp_dir()
WORK_PATH = utils.return_rax_dir()
LIBS_PATH = utils.return_rax_dir(path='lib')


BDBM_URL = 'http://download.oracle.com/berkeley-db/db-6.0.30.tar.gz'


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
                    'url': BDBM_URL,
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
        'apt_packages': [
            'tcl8.5-dev',
            'tk8.5-dev'
        ]
    }
}