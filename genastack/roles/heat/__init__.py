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


ARGS = utils.get_role_config('heat')
BRANCH = ARGS.get('branch', 'master')
PROJECT_URL = ARGS.get(
    'project_url', 'https://github.com/openstack/heat.git'
)


BUILD_DATA = {
    'heat': {
        'use_system_python': ARGS.get('use_system_python', False),
        'help': 'Install Heat from upstream on Branch "%s"' % BRANCH,
        'required': [
            'python',
            'heat_client',
            'keystone_client',
            'ceilometer_client',
            'trove_client'
        ],
        'directories': [
            {
                'path': '/var/log/heat',
                'user': 'heat',
                'group': 'heat',
                'mode': '0755'
            },
            {
                'path': '/var/lib/heat',
                'user': 'heat',
                'group': 'heat',
                'mode': '0755'
            },
            {
                'path': '/etc/heat',
                'user': 'heat',
                'group': 'heat',
                'mode': '0755'
            }
        ],
        'group_create': [
            {
                'group': 'heat',
                'system': True
            }
        ],
        'user_create': [
            {
                'user': 'heat',
                'group': 'heat',
                'home': '/var/lib/heat',
                'system': True
            }
        ],
        'git_install': [
            {
                'name': 'heat',
                'project_url': PROJECT_URL,
                'branch': BRANCH,
                'config_example': 'etc/heat=/etc/heat',
                'group_owner': 'heat',
                'user_owner': 'heat',
                'mode': '0644'
            }
        ],
        'package_install': {
            'apt': {
                'packages': [
                    'mysql-client',
                    'libmysqlclient-dev'
                ]
            }
        }
    }
}
