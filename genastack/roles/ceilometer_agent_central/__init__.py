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
    'ceilometer_agent_central': {
        'help': 'Install ceilometer_agent_central from upstream',
        'required': [
            'python',
            'ceilometer',
            'ceilometer_client'
        ],
        'init_script': [
            {
                'help': 'Start and stop ceilometer-agent-central on boot',
                'init_path': '/etc/init.d',
                'name': 'ceilometer-agent-central',
                'chuid': 'ceilometer',
                'chdir': '/var/lib/ceilometer',
                'program': 'ceilometer-agent-central'
            }
        ]
    }
}
