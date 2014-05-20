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
    'nova_novncproxy': {
        'help': 'Install nova novnc proxy from upstream',
        'required': [
            'nova'
        ],
        'init_script': [
            {
                'help': 'Start and stop nova on boot',
                'init_path': '/etc/init.d',
                'name': 'nova',
                'chuid': 'nova',
                'chdir': '/var/lib/nova',
                'options': '--'
                           ' --config-file=/etc/nova/nova.conf',
                'program': 'nova-novncproxy'
            }
        ],
        'package_install': {
            'apt': {
                'packages': [
                    'novnc',
                    'websockify'
                ]
            }
        }
    }
}
