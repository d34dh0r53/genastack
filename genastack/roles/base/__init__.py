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
LIBEXEC_PATH = utils.return_rax_dir(path='libexec')
BIN_PATH = utils.return_rax_dir(path='bin')
SBIN_PATH = utils.return_rax_dir(path='sbin')


BZIP_URL = 'http://www.bzip.org/1.0.6/bzip2-1.0.6.tar.gz'


RAX_BIN_SCRIPT = """
#!/usr/bin/env bash
RAX_PATH="%s:%s:%s"

if ! echo ${PATH} | /bin/grep -q ${RAX_PATH} ; then
PATH=${PATH}:${RAX_PATH}
fi
""" % (BIN_PATH, SBIN_PATH, LIBEXEC_PATH)


INSTALL_COMMANDS = [
    'make',
    'make install PREFIX=%s' % WORK_PATH
]


BUILD_DATA = {
    'base': {
        'help': 'Install base packages.',
        'execute': [
            'source /etc/profile.d/openstack_default.sh'
        ],
        'directories': [
            {
                'path': '/etc/profile.d',
                'user': 'root',
                'group': 'root',
                'mode': '0755'
            },
            {
                'path': SBIN_PATH,
                'user': 'root',
                'group': 'root',
                'mode': '0755'
            },
            {
                'path': LIBEXEC_PATH,
                'user': 'root',
                'group': 'root',
                'mode': '0755'
            },
            {
                'path': BIN_PATH,
                'user': 'root',
                'group': 'root',
                'mode': '0755'
            },
            {
                'path': LIBS_PATH,
                'user': 'root',
                'group': 'root',
                'mode': '0755'
            },
            {
                'path': WORK_PATH,
                'user': 'root',
                'group': 'root',
                'mode': '0755'
            }
        ],
        'file_create': [
            {
                'path': '/etc/profile.d',
                'name': 'openstack_default.sh',
                'contents': RAX_BIN_SCRIPT,
                'user': 'root',
                'group': 'root',
                'mode': '0755'
            }
        ],
        'apt_packages': [
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
    }
}
