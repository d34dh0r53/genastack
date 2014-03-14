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


TEMP_PATH = utils.return_temp_dir()
WORK_PATH = utils.return_rax_dir()
LIBS_PATH = utils.return_rax_dir(path='lib')
BIN_PATH = utils.return_rax_dir(path='bin')
INCLUDE_PATH = utils.return_rax_dir(path='include')


PYTHON_URL = 'http://www.python.org/ftp/python/2.7.6/Python-2.7.6.tgz'
PIP_URL = 'https://raw.github.com/pypa/pip/master/contrib/get-pip.py'


RAX_SOURCE_SCRIPT = """
#!/usr/bin/env bash
VENV_PATH="%s"
if [[ -f "${VENV_PATH}" ]]; then
  source ${VENV_PATH}
fi
""" % os.path.join(BIN_PATH, 'activate')


INSTALL_COMMANDS = [
    './configure --prefix=%s --enable-unicode=ucs4'
    ' --with-threads --with-signal-module' % WORK_PATH,
    'make -j4',
    'make install'
]


EXPORTS = [
    'CFLAGS=-I%s -I/usr/include/x86_64-linux-gnu' % INCLUDE_PATH,
    'LDFLAGS=-L%s -L/usr/lib/x86_64-linux-gnu' % LIBS_PATH
]


BUILD_DATA = {
    'python': {
        'help': 'Install Python.',
        'required': [
            'base'
        ],
        'remote_script': [
            {
                'help': 'Install pip.',
                'get': {
                    'url': PIP_URL,
                    'path': TEMP_PATH,
                    'name': 'get-pip.py',
                    'uncompress': False
                },
                'not_if_exists': os.path.join(BIN_PATH, 'pip'),
                'interpreter': os.path.join(BIN_PATH, 'python'),
            }
        ],
        'pip_install': [
            'bz2file',
            'd2to1',
            'distribute',
            'mysql-python',
            'pbr',
            'pysqlite',
            'virtualenv',
            'pep8',
            'flake8',
            'hacking',
            'iso8601',
            'lockfile',
            'amqplib',
            'kombu',
            'psycopg2',
            'sqlalchemy'
        ],
        'apt_packages': [
            'zlib1g-dev',
            'libdb-dev',
            'libxml2',
            'libxml2-dev',
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
            'libxslt1.1',
            'tk-dev',
            'libmysqlclient-dev',
            'libpq-dev',
            'libxft-dev',
            'tcl8.5-dev',
            'tk8.5-dev',
            'libffi-dev',
            'python-libvirt',
            'python-dev'
        ],
        'file_create': [
            {
                'path': '/etc/profile.d',
                'name': 'openstack_venv.sh',
                'contents': RAX_SOURCE_SCRIPT,
                'user': 'root',
                'group': 'root',
                'mode': '0755'
            }
        ],
        'execute': [
            'virtualenv --system-site-packages %s' % BIN_PATH
        ]
    }
}
