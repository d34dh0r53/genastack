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
    'glance_all': {
        'help': 'Install all of Glance from upstream',
        'required': [
            'glance_client',
            'glance_api',
            'glance_registry'
        ]
    }
}

