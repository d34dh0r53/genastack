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


BIN_PATH = roles.return_rax_dir('bin')


BRANCH = 'stable/havana'


GLANCE_PROJECT = 'https://github.com/openstack/glance.git'
PROJECT_URL = 'https://raw.github.com/openstack/glance/%s' % BRANCH
URL_PATH = '%s/etc' % PROJECT_URL


GLANCE_REGISTRY_PASTE = '%s/glance-registry-paste.ini' % URL_PATH
GLANCE_REGISTRY_CONF = '%s/glance-registry.conf' % URL_PATH
GLANCE_LOGGING_CNF = '%s/logging.cnf.sample' % URL_PATH
GLANCE_POLICY_JSON = '%s/policy.json' % URL_PATH


BUILD_DATA = {
    'glance-api': {
        'help': 'Install Keystone from upstream on Branch "%s"' % BRANCH,
        'required': [
            'python',
            'glance_client'
        ],
        'directories': [
            {
                'path': '/var/log/glance',
                'user': 'glance',
                'group': 'glance',
                'mode': 0755
            },
            {
                'path': '/var/lib/glance',
                'user': 'glance',
                'group': 'glance',
                'mode': 0755
            },
            {
                'path': '/etc/glance',
                'user': 'glance',
                'group': 'glance',
                'mode': 0755
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
        'file_create': [
            {
                'path': '/etc/glance',
                'name': 'glance-registry-paste.ini',
                'from_remote': GLANCE_REGISTRY_PASTE,
                'user': 'glance',
                'group': 'glance',
                'mode': 0644
            },
            {
                'path': '/etc/glance',
                'name': 'glance-registry.conf',
                'from_remote': GLANCE_REGISTRY_CONF,
                'user': 'glance',
                'group': 'glance',
                'mode': 0644
            },
            {
                'path': '/etc/glance',
                'name': 'logging.cnf',
                'from_remote': GLANCE_LOGGING_CNF,
                'user': 'glance',
                'group': 'glance',
                'mode': 0644
            },
            {
                'path': '/etc/glance',
                'name': 'policy.json',
                'from_remote': GLANCE_POLICY_JSON,
                'user': 'glance',
                'group': 'glance',
                'mode': 0644
            }
        ],
        'pip_install': {
            'pip_bin': '%s/pip' % BIN_PATH,
            'pip_packages': [
                'git+%s@%s' % (GLANCE_PROJECT, BRANCH)
            ],
        },
        'packages': {
            'apt': [
                'sqlite3'
            ]
        },
        'init_script': [
            {
                'help': 'Start and stop glance on boot',
                'init_path': '/etc/init.d',
                'bin_path': BIN_PATH,
                'name': 'glance-registry',
                'chuid': 'glance',
                'chdir': '/var/lib/glance',
                'program': 'glance-registry'
            }
        ]
    }
}
