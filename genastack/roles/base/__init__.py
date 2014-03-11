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


BZIP_URL = 'http://www.bzip.org/1.0.6/bzip2-1.0.6.tar.gz'


RAX_BIN_SCRIPT = """
#!/usr/bin/env bash
RAX_PATH="/opt/rackspace/bin"

if ! echo ${PATH} | /bin/grep -q ${RAX_PATH} ; then
PATH=${RAX_PATH}:${PATH}
fi
"""


INSTALL_COMMANDS = [
    'make',
    'make install PREFIX=%s' % WORK_PATH
]


BUILD_DATA = {
    'base': {
        'help': 'Install base packages.',
        'packages': {
            'apt': [
                'libmysqlclient-dev',
                'gettext',
                'help2man',
                'html2text',
                'libxml2-dev',
                'intltool-debian',
                'git-core',
                'curl',
                'openssl',
                'build-essential',
                'bridge-utils',
                'cgroup-lite',
                'gawk'
            ]
        },
        'directories': [
            {
                'path': '/etc/profile.d',
                'user': 'root',
                'group': 'root',
                'mode': 0755
            },
            {
                'path': LIBS_PATH,
                'user': 'root',
                'group': 'root',
                'mode': 0755
            },
            {
                'path': WORK_PATH,
                'user': 'root',
                'group': 'root',
                'mode': 0755
            }
        ],
        'file_create': [
            {
                'path': '/etc/profile.d',
                'name': 'rackspace_default.sh',
                'contents': RAX_BIN_SCRIPT,
                'user': 'root',
                'group': 'root',
                'mode': 0755
            }
        ]
    }
}