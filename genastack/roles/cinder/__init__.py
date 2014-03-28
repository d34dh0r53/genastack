# =============================================================================
# Copyright [2013] [Kevin Carter]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================

from genastack.common import system_config


CONFIG = system_config.ConfigurationSetup()
ARGS = CONFIG.config_args(section='cinder')
BRANCH = ARGS.get('branch', 'master')
PROJECT_URL = ARGS['project_url']


BUILD_DATA = {
    'cinder': {
        'use_system_python': ARGS.get('use_system_python', False),
        'help': 'Install cinder from upstream Branch "%s"' % BRANCH,
        'required': [
            'python'
        ],
        'directories': [
            {
                'path': '/var/log/cinder',
                'user': 'cinder',
                'group': 'cinder',
                'mode': '0755'
            },
            {
                'path': '/var/lib/cinder',
                'user': 'cinder',
                'group': 'cinder',
                'mode': '0755'
            },
            {
                'path': '/etc/cinder/rootwrap.d',
                'user': 'cinder',
                'group': 'cinder',
                'mode': '0755'
            },
            {
                'path': '/var/lock/cinder',
                'user': 'cinder',
                'group': 'root',
                'mode': '0755'
            },
            {
                'path': '/var/run/cinder',
                'user': 'cinder',
                'group': 'cinder',
                'mode': '0755'
            },
            {
                'path': '/etc/cinder',
                'user': 'cinder',
                'group': 'cinder',
                'mode': '0755'
            }
        ],
        'group_create': [
            {
                'group': 'cinder',
                'system': True
            }
        ],
        'user_create': [
            {
                'user': 'cinder',
                'group': 'cinder',
                'home': '/var/lib/cinder',
                'system': True
            }
        ],
        'git_install': [
            {
                'name': 'cinder',
                'project_url': PROJECT_URL,
                'branch': BRANCH,
                'config_example': 'etc/cinder=/etc/cinder',
                'group_owner': 'cinder',
                'user_owner': 'cinder',
                'mode': '0644'
            }
        ],
        'pip_install': [
            '--allow-all-external pywbem'
        ],
        'apt_packages': [
            'lvm2',
            'tgt',
            'open-iscsi',
            'qemu-utils',
            'sysfsutils',
            'nfs-common'
        ]
    }
}
