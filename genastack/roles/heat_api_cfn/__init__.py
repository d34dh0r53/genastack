# =============================================================================
# Copyright [2013] [Kevin Carter]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================

BUILD_DATA = {
    'heat_api_cfn': {
        'help': 'Install heat-API-CFN from upstream',
        'required': [
            'python',
            'heat',
            'heat_client'
        ],
        'init_script': [
            {
                'help': 'Start and stop heat-api-cfn on boot',
                'init_path': '/etc/init.d',
                'name': 'heat-api-cfn',
                'chuid': 'heat',
                'chdir': '/var/lib/heat',
                'program': 'heat-api-cfn'
            }
        ]
    }
}
