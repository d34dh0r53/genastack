# =============================================================================
# Copyright [2013] [Kevin Carter]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================
from cloudlib import parse_ini

# Check to see if our System Config File Exists
CONFIG = parse_ini.ConfigurationSetup(log_name='genastack-system')
ARGS = CONFIG.config_args(section='keystone')
BRANCH = ARGS.get('branch', 'master')
PROJECT_URL = ARGS['project_url']


BUILD_DATA = {
    'keystone': {
        'use_system_python': ARGS.get('use_system_python', False),
        'help': 'Install Keystone from upstream on Branch "%s"' % BRANCH,
        'required': [
            'python'
        ],
        'directories': [
            {
                'path': '/var/log/keystone',
                'user': 'keystone',
                'group': 'keystone',
                'mode': '0755'
            },
            {
                'path': '/var/lib/keystone',
                'user': 'keystone',
                'group': 'keystone',
                'mode': '0755'
            },
            {
                'path': '/etc/keystone',
                'user': 'keystone',
                'group': 'keystone',
                'mode': '0755'
            },
            {
                'path': '/etc/keystone/ssl',
                'user': 'keystone',
                'group': 'keystone',
                'mode': '0755'
            }
        ],
        'group_create': [
            {
                'group': 'keystone',
                'system': True
            }
        ],
        'user_create': [
            {
                'user': 'keystone',
                'group': 'keystone',
                'home': '/var/lib/keystone',
                'system': True
            }
        ],
        'git_install': [
            {
                'name': 'keystone',
                'project_url': PROJECT_URL,
                'branch': BRANCH,
                'config_example': 'etc=/etc/keystone',
                'group_owner': 'keystone',
                'user_owner': 'keystone',
                'mode': '0644'
            }
        ],
        'pip_install': [
            'repoze.lru',
            'pbr',
            'mysql-python'
        ],
        'package_install': {
            'apt': {
                'packages': [
                    'mysql-client',
                    'libmysqlclient-dev',
                    'libsasl2-dev debhelper',
                    'dh-apparmor',
                    'docutils-common',
                    'libjs-sphinxdoc',
                    'libjs-underscore',
                    'libxslt1.1',
                    'libxslt1-dev',
                    'libxml2-dev',
                    'libssl-dev',
                    'libldap2-dev',
                    'libffi-dev'
                ]
            }
        }
    }
}
