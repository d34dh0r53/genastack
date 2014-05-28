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


ARGS = utils.get_role_config('glance')
BRANCH = ARGS.get('branch', 'master')
PROJECT_URL = ARGS.get(
    'project_url', 'https://github.com/openstack/glance.git'
)


BUILD_DATA = {
    'glance': {
        'use_system_python': ARGS.get('use_system_python', False),
        'help': 'Install Glance from upstream Branch "%s"' % BRANCH,
        'required': [
            'python',
            'swift_client'
        ],
        'directories': [
            {
                'path': '/var/log/glance',
                'user': 'glance',
                'group': 'glance',
                'mode': '0755'
            },
            {
                'path': '/var/lib/glance',
                'user': 'glance',
                'group': 'glance',
                'mode': '0755'
            },
            {
                'path': '/etc/glance',
                'user': 'glance',
                'group': 'glance',
                'mode': '0755'
            }
        ],
        'group_create': [
            {
                'group': 'glance',
                'system': True
            }
        ],
        'user_create': [
            {
                'user': 'glance',
                'group': 'glance',
                'home': '/var/lib/glance',
                'system': True
            }
        ],
        'git_install': [
            {
                'name': 'glance',
                'project_url': PROJECT_URL,
                'branch': BRANCH,
                'config_example': 'etc/glance=/etc/glance',
                'group_owner': 'glance',
                'user_owner': 'glance',
                'mode': '0644'
            }
        ],
        'pip_install': [
            'warlock'
        ],
        'package_install': {
            'apt': {
                'packages': [
                    'sqlite3'
                ]
            }
        }
    }
}
