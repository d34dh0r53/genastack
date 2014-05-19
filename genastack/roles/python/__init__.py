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


TEMP_PATH = utils.return_temp_dir()


PIP_URL = 'https://raw.github.com/pypa/pip/master/contrib/get-pip.py'


BUILD_DATA = {
    'python': {
        'help': 'Configure Python.',
        'required': [
            'base'
        ],
        'remote_script': [
            {
                'help': 'Install pip.',
                'get': {
                    'url': PIP_URL,
                    'path': TEMP_PATH,
                    'name': 'get-pip.py',
                    'uncompress': False
                },
                'interpreter': 'python',
            }
        ],
        'pip_install': [
            'virtualenv'
        ],
        'package_install': {
            'apt': [
                'zlib1g-dev',
                'libdb-dev',
                'libxml2',
                'libxml2-dev',
                'libncurses5-dev',
                'libbz2-dev',
                'liblz-dev',
                'libexpat1',
                'libncursesw5-dev',
                'libreadline6',
                'libreadline6-dev',
                'libreadline-dev',
                'libcroco3',
                'libgettextpo0',
                'libssl-dev',
                'libgdbm-dev',
                'libc6-dev',
                'libsqlite3-dev',
                'libxslt1-dev',
                'libxslt1.1',
                'tk-dev',
                'libmysqlclient-dev',
                'libpq-dev',
                'libxft-dev',
                'tcl8.5-dev',
                'tk8.5-dev',
                'libffi-dev',
                'python-libvirt',
                'python-dev'
            ]
        }
    }
}
