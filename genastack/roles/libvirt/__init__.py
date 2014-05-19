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
from cloudlib import parse_ini

# Check to see if our System Config File Exists
CONFIG = parse_ini.ConfigurationSetup(log_name='genastack-system')
ARGS = CONFIG.config_args(section='libvirt')
PROJECT_URL = ARGS.get(
    'project_url', 'http://libvirt.org/sources/libvirt-1.2.2.tar.gz'
)

TEMP_PATH = utils.return_temp_dir()
WORK_PATH = utils.return_rax_dir()
LIBS_PATH = utils.return_rax_dir(path='openstack/lib')
INCLUDE_PATH = utils.return_rax_dir(path='openstack/include')


INSTALL_COMMANDS = [
    './configure --prefix=%s --localstatedir=/var'
    ' --sysconfdir=/etc' % WORK_PATH,
    'make',
    'make install'
]


EXPORTS = [
    'CFLAGS=-I%s -I/usr/include/x86_64-linux-gnu' % INCLUDE_PATH,
    'LDFLAGS=-L%s -L/usr/lib/x86_64-linux-gnu' % LIBS_PATH
]


BUILD_DATA = {
    'libvirt': {
        'help': 'Install upstream libvirt.',
        'required': [
            'base'
        ],
        'build': [
            {
                'get': {
                    'url': PROJECT_URL,
                    'path': TEMP_PATH,
                    'name': 'libvirt-1.2.2.tgz',
                    'md5sum': '592958ad1ddce7574d8cb0a31e635acd',
                    'uncompress': True
                },
                'export': EXPORTS,
                'not_if_exists': os.path.join(LIBS_PATH, 'libvirt.so'),
                'build_commands': INSTALL_COMMANDS,
            }
        ],
        'pip_install': [
            'libvirt-python'
        ],
        'package_install': {
            'apt': [
                'libgnutls-dev',
                'libdevmapper-dev',
                'libcurl4-gnutls-dev',
                'libpciaccess-dev',
                'libnl-dev',
                'pm-utils',
                'ebtables',
                'dnsmasq-base',
                'libyajl-dev',
                'uuid-dev'
            ]
        },
        'init_script': [
            {
                'help': 'Start and stop libvirt on boot',
                'path': '/opt/rackspace/sbin',
                'name': 'libvirtd',
                'program': 'libvirt-bin',
                'options': '-d'
            }
        ]
    }
}
