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


ARGS = utils.get_role_config('swift_client')
BRANCH = ARGS.get('branch', 'master')
PROJECT_URL = ARGS.get(
    'project_url', 'https://github.com/openstack/python-swiftclient.git'
)


BUILD_DATA = {
    'swift_client': {
        'use_system_python': ARGS.get('use_system_python', False),
        'python_venv': {
            'name': 'swift'
        },
        'help': 'Install Swift client from upstream, Branch "%s"' % BRANCH,
        'git_install': [
            {
                'name': 'swift_client',
                'project_url': PROJECT_URL,
                'branch': BRANCH
            }
        ]
    }
}
