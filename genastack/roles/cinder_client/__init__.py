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


BRANCH = '1.0.8'


PROJECT_URL = 'https://github.com/openstack'
CLIENT = '%s/python-cinderclient.git' % PROJECT_URL


BUILD_DATA = {
    'cinder_client': {
        'help': 'Install cinder client from upstream, Branch "%s"' % BRANCH,
        'pip_install': {
            'pip_bin': '%s/pip' % BIN_PATH,
            'pip_packages': [
                'git+%s@%s' % (CLIENT, BRANCH)
            ]
        }
    }
}
