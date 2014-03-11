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
LIBS_PATH = roles.return_rax_dir(path='lib')
BIN_PATH = roles.return_rax_dir(path='bin')
INCLUDE_PATH = roles.return_rax_dir(path='include')


PYTHON_URL = 'http://www.python.org/ftp/python/2.7.6/Python-2.7.6.tgz'
PIP_URL = 'https://raw.github.com/pypa/pip/master/contrib/get-pip.py'


INSTALL_COMMANDS = [
    './configure --prefix=%s --enable-unicode=ucs4'
    ' --with-threads --with-signal-module' % WORK_PATH,
    'make -j4',
    'make install'
]


BUILD_DATA = {
    'python': {
        'required': [
            'base'
        ],
        'libs': [
            'openssl',
            'berkeley_db',
            'postgres_connector',
            'mysql_connector'
        ],
        'help': 'Install the python packages and python on a system.',
        'remote_script': {
            'help': 'Install pip.',
            'get': {
                'url': PIP_URL,
                'path': TEMP_PATH,
                'name': 'get-pip.py',
                'uncompress': False
            },
            'not_if_exists': '%s/bin/pip' % WORK_PATH,
            'interpreter': '%s/bin/python' % WORK_PATH,
        },
        'build': {
            'get': {
                'url': PYTHON_URL,
                'path': TEMP_PATH,
                'name': 'Python-2.7.6.tgz',
                'md5sum': '1d8728eb0dfcac72a0fd99c17ec7f386',
                'uncompress': True
            },
            'not_if_exists': '%s/bin/python' % WORK_PATH,
            'build_commands': INSTALL_COMMANDS,
            'export': [
                'CFLAGS=-I%s -I/usr/include/x86_64-linux-gnu' % INCLUDE_PATH,
                'LDFLAGS=-L%s -L/usr/lib/x86_64-linux-gnu' % LIBS_PATH
            ],
        },
        'ldconfig': [
            '/opt/python27/lib=/etc/ld.so.conf.d/python27.conf'
        ],
        'pip_install': {
            'pip_bin': '%s/pip' % BIN_PATH,
            'pip_packages': [
                'bz2file',
                'd2to1',
                'distribute',
                'mysql-python',
                'pbr',
                'pysqlite',
                'virtualenv',
                'pep8',
                'flake8',
                'hacking'
            ],
        },
        'packages': {
            'apt': [
                'zlib1g-dev',
                'libdb-dev',
                'libncurses5-dev',
                'libbz2-dev',
                'liblz-dev',
                'libexpat1',
                'libncursesw5-dev',
                'libreadline6',
                'libreadline6-dev',
                'libreadline-dev',
                'libcroco3',
                'libgettextpo0',
                'libssl-dev',
                'libgdbm-dev',
                'libc6-dev',
                'libsqlite3-dev',
                'libxslt1-dev',
                'tk-dev'
            ]
        }
    }
}
