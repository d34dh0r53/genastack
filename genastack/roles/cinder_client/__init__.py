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
ARGS = CONFIG.config_args(section='cinder_client')
BRANCH = ARGS.get('branch', 'master')
PROJECT_URL = ARGS['project_url']


BUILD_DATA = {
    'cinder_client': {
        'use_system_python': ARGS.get('use_system_python', False),
        'python_venv': {
            'name': 'cinder'
        },
        'help': 'Install cinder client from upstream, Branch "%s"' % BRANCH,
        'git_install': [
            {
                'name': 'cinder_client',
                'project_url': PROJECT_URL,
                'branch': BRANCH
            }
        ]
    }
}
