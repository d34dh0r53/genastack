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


ARGS = utils.get_role_config('nova')
BRANCH = ARGS.get('branch', 'master')
PROJECT_URL = ARGS.get(
    'project_url', 'https://github.com/openstack/nova.git'
)


BUILD_DATA = {
    'nova': {
        'use_system_python': ARGS.get('use_system_python', False),
        'help': 'Install Nova from upstream Branch "%s"' % BRANCH,
        'required': [
            'python',
            'nova_client',
            'keystone_client',
            'cinder_client'
        ],
        'directories': [
            {
                'path': '/var/log/nova',
                'user': 'nova',
                'group': 'nova',
                'mode': '0755'
            },
            {
                'path': '/var/lib/nova',
                'user': 'nova',
                'group': 'nova',
                'mode': '0755'
            },
            {
                'path': '/etc/nova',
                'user': 'nova',
                'group': 'nova',
                'mode': '0755'
            },
            {
                'path': '/var/lock/nova',
                'user': 'nova',
                'group': 'root',
                'mode': '0755'
            },
            {
                'path': '/var/run/nova',
                'user': 'nova',
                'group': 'root',
                'mode': '0755'
            }
        ],
        'group_create': [
            {
                'group': 'nova',
                'system': True
            }
        ],
        'user_create': [
            {
                'user': 'nova',
                'group': 'nova',
                'home': '/var/lib/nova',
                'system': True
            }
        ],
        'git_install': [
            {
                'name': 'nova',
                'project_url': PROJECT_URL,
                'branch': BRANCH,
                'config_example': 'etc/nova=/etc/nova',
                'group_owner': 'nova',
                'user_owner': 'nova',
                'mode': '0644'
            }
        ],
        'pip_install': [
            'python-swiftclient',
            'eventlet',
        ],
        'package_install': {
            'apt': {
                'packages': [
                    'multipath-tools',
                    'sysfsutils',
                    'sg3-utils',
                    'libvirt-bin',
                    'libvirt-dev',
                    'libvirt0',
                    'python-libvirt',
                    'pm-utils',
                    'kvm',
                    'qemu-utils',
                    'iptables'
                ]
            }
        }
    }
}
