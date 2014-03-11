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


CINDER_PROJECT = 'https://github.com/openstack/cinder.git'
PROJECT_URL = 'https://raw.github.com/openstack/cinder/%s' % BRANCH
URL_PATH = '%s/etc/cinder' % PROJECT_URL


CINDER_API_PASTE = '%s/api-paste.ini' % URL_PATH
CINDER_CONF = '%s/cinder.conf.sample' % URL_PATH
CINDER_LOGGING_CONF = '%s/logging_sample.conf' % URL_PATH
CINDER_POLICY_JSON = '%s/policy.json' % URL_PATH
CINDER_ROOTWRAP_CONF = '%s/rootwrap.conf' % URL_PATH
CINDER_ROOTWRAP_VOLUME = '%s/rootwrap.d/volume.filters' % URL_PATH


BUILD_DATA = {
    'cinder': {
        'help': 'Install cinder from upstream Branch "%s"' % BRANCH,
        'required': [
            'python'
        ],
        'directories': [
            {
                'path': '/var/log/cinder',
                'user': 'cinder',
                'group': 'cinder',
                'mode': 0755
            },
            {
                'path': '/var/lib/cinder',
                'user': 'cinder',
                'group': 'cinder',
                'mode': 0755
            },
            {
                'path': '/etc/cinder/rootwrap.d',
                'user': 'cinder',
                'group': 'cinder',
                'mode': 0755
            },
            {
                'path': '/var/lock/cinder',
                'user': 'cinder',
                'group': 'root',
                'mode': 0755
            },
            {
                'path': '/var/run/cinder',
                'user': 'cinder',
                'group': 'cinder',
                'mode': 0755
            },
            {
                'path': '/etc/cinder',
                'user': 'cinder',
                'group': 'cinder',
                'mode': 0755
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
        'file_create': [
            {
                'path': '/etc/cinder',
                'name': 'api-paste.ini',
                'from_remote': CINDER_API_PASTE,
                'user': 'cinder',
                'group': 'cinder',
                'mode': 0644
            },
            {
                'path': '/etc/cinder',
                'name': 'cinder.conf',
                'from_remote': CINDER_CONF,
                'user': 'cinder',
                'group': 'cinder',
                'mode': 0644
            },
            {
                'path': '/etc/cinder',
                'name': 'logging.conf',
                'from_remote': CINDER_LOGGING_CONF,
                'user': 'cinder',
                'group': 'cinder',
                'mode': 0644
            },
            {
                'path': '/etc/cinder',
                'name': 'policy.json',
                'from_remote': CINDER_POLICY_JSON,
                'user': 'cinder',
                'group': 'cinder',
                'mode': 0644
            },
            {
                'path': '/etc/cinder',
                'name': 'rootwrap.conf',
                'from_remote': CINDER_ROOTWRAP_CONF,
                'user': 'cinder',
                'group': 'cinder',
                'mode': 0644
            },
            {
                'path': '/etc/cinder',
                'name': 'rootwrap.d/volume.filters',
                'from_remote': CINDER_ROOTWRAP_VOLUME,
                'user': 'cinder',
                'group': 'cinder',
                'mode': 0644
            }
        ],
        'pip_install': {
            'pip_bin': '%s/pip' % BIN_PATH,
            'pip_packages': [
                'git+%s@%s' % (CINDER_PROJECT, BRANCH),
                'pywbem'
            ],
        },
        'packages': {
            'apt': [
                'lvm2',
                'tgt',
                'open-iscsi',
                'qemu-utils',
                'sysfsutils',
                'nfs-common'
            ]
        }
    }
}
