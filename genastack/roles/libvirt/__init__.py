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

from genastack import roles


TEMP_PATH = roles.return_temp_dir()
WORK_PATH = roles.return_rax_dir()
LIBS_PATH = roles.return_rax_dir(path='lib')
INCLUDE_PATH = roles.return_rax_dir(path='include')


LIBVIRT_URL = 'http://libvirt.org/sources/libvirt-1.2.2.tar.gz'


INSTALL_COMMANDS = [
    './configure --prefix=%s --localstatedir=/var'
    ' --sysconfdir=/etc' % WORK_PATH,
    'make',
    'make install'
]


BUILD_DATA = {
    'libvirt': {
        'help': 'Install upstream libvirt.',
        'required': [
            'base'
        ],
        'build': {
            'get': {
                'url': LIBVIRT_URL,
                'path': TEMP_PATH,
                'name': 'libvirt-1.2.2.tgz',
                'md5sum': '592958ad1ddce7574d8cb0a31e635acd',
                'uncompress': True
            },
            'export': [
                'CFLAGS=-I%s -I/usr/include/x86_64-linux-gnu' % INCLUDE_PATH,
                'LDFLAGS=-L%s -L/usr/lib/x86_64-linux-gnu' % LIBS_PATH
            ],
            'not_if_exists': os.path.join(LIBS_PATH, 'libvirt.so'),
            'build_commands': INSTALL_COMMANDS,
        },
        'packages': {
            'apt': [
                'libgnutls-dev',
                'libdevmapper-dev',
                'libcurl4-gnutls-dev',
                'libpciaccess-dev',
                'libnl-dev',
                'pm-utils',
                'ebtables',
                'dnsmasq-base'
            ]
        }
    }
}
