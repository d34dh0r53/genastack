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


BIN_PATH = utils.return_rax_dir('bin')


BRANCH = 'stable/havana'


NOVA_PROJECT = 'https://github.com/openstack/nova.git'
PROJECT_URL = 'https://raw.github.com/openstack/nova/%s' % BRANCH
URL_PATH = '%s/etc/nova' % PROJECT_URL


NOVA_API_PASTE = '%s/api-paste.ini' % URL_PATH
NOVA_CELLS_JSON = '%s/cells.json' % URL_PATH
NOVA_LOGGING = '%s/logging_sample.conf' % URL_PATH
NOVA_CONF = '%s/nova.conf.sample' % URL_PATH
NOVA_POLICY_JSON = '%s/policy.json' % URL_PATH
NOVA_RELEASE = '%s/release.sample' % URL_PATH
NOVA_ROOTWRAP = '%s/rootwrap.conf' % URL_PATH
NOVA_METADATA_RW = '%s/rootwrap.d/api-metadata.filters' % URL_PATH
NOVA_IPMI_RW = '%s/rootwrap.d/baremetal-compute-ipmi.filters' % URL_PATH
NOVA_DEPLOY_RW = '%s/rootwrap.d/baremetal-deploy-helper.filters' % URL_PATH
NOVA_COMPUTE_RW = '%s/rootwrap.d/compute.filters' % URL_PATH
NOVA_DOCKER_RW = '%s/rootwrap.d/docker.filters' % URL_PATH
NOVA_NETWORK_RW = '%s/rootwrap.d/network.filters' % URL_PATH


BUILD_DATA = {
    'nova': {
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
        'file_create': [
            {
                'path': '/etc/nova',
                'name': 'api-paste.ini',
                'from_remote': NOVA_API_PASTE,
                'user': 'nova',
                'group': 'nova',
                'mode': '0644'
            },
            {
                'path': '/etc/nova',
                'name': 'cells.json',
                'from_remote': NOVA_CELLS_JSON,
                'user': 'nova',
                'group': 'nova',
                'mode': '0644'
            },
            {
                'path': '/etc/nova',
                'name': 'logging.conf',
                'from_remote': NOVA_LOGGING,
                'user': 'nova',
                'group': 'nova',
                'mode': '0644'
            },
            {
                'path': '/etc/nova',
                'name': 'nova.conf',
                'from_remote': NOVA_CONF,
                'user': 'nova',
                'group': 'nova',
                'mode': '0644'
            },
            {
                'path': '/etc/nova',
                'name': 'policy.json',
                'from_remote': NOVA_POLICY_JSON,
                'user': 'nova',
                'group': 'nova',
                'mode': '0644'
            },
            {
                'path': '/etc/nova',
                'name': 'release',
                'from_remote': NOVA_RELEASE,
                'user': 'nova',
                'group': 'nova',
                'mode': '0644'
            },
            {
                'path': '/etc/nova',
                'name': 'rootwrap.conf',
                'from_remote': NOVA_ROOTWRAP,
                'user': 'nova',
                'group': 'nova',
                'mode': '0644'
            },
            {
                'path': '/etc/nova/rootwrap.d',
                'name': 'api-metadata.filters',
                'from_remote': NOVA_METADATA_RW,
                'user': 'nova',
                'group': 'nova',
                'mode': '0644'
            },
            {
                'path': '/etc/nova/rootwrap.d',
                'name': 'baremetal-compute-ipmi.filters',
                'from_remote': NOVA_IPMI_RW,
                'user': 'nova',
                'group': 'nova',
                'mode': '0644'
            },
            {
                'path': '/etc/nova/rootwrap.d',
                'name': 'baremetal-deploy-helper.filters',
                'from_remote': NOVA_DEPLOY_RW,
                'user': 'nova',
                'group': 'nova',
                'mode': '0644'
            },
            {
                'path': '/etc/nova/rootwrap.d',
                'name': 'compute.filters',
                'from_remote': NOVA_COMPUTE_RW,
                'user': 'nova',
                'group': 'nova',
                'mode': '0644'
            },
            {
                'path': '/etc/nova/rootwrap.d',
                'name': 'docker.filters',
                'from_remote': NOVA_DOCKER_RW,
                'user': 'nova',
                'group': 'nova',
                'mode': '0644'
            },
            {
                'path': '/etc/nova/rootwrap.d',
                'name': 'network.filters',
                'from_remote': NOVA_NETWORK_RW,
                'user': 'nova',
                'group': 'nova',
                'mode': '0644'
            },
        ],
        'pip_install': [
            'git+%s@%s' % (NOVA_PROJECT, BRANCH),
            'python-swiftclient',
            'eventlet',
            'libvirt-python',
        ],
        'apt_packages': [
            'multipath-tools',
            'sysfsutils',
            'sg3-utils',
            'libvirt-bin',
            'pm-utils',
            'libvirt-dev'
        ]
    }
}
