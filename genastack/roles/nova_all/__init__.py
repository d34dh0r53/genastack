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
    'nova_all': {
        'help': 'Install all of Nova Compute from upstream',
        'required': [
            'nova_client',
            'nova_api_ec2',
            'nova_api_metadata',
            'nova_api_os_compute',
            'nova_cert',
            'nova_client',
            'nova_compute',
            'nova_conductor',
            'nova_consoleauth',
            'nova_novncproxy',
            'nova_scheduler'
        ]
    }
}
