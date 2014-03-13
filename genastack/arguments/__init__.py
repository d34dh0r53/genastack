# =============================================================================
# Copyright [2013] [Kevin Carter]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================


DEFAULT_ARGS = {
    '--debug': {
        'help': 'Make the script debug',
        'action': 'store_true',
        'default': False,
    },
    '--print-only': {
        'help': 'Print the build map ONLY',
        'action': 'store_true',
        'default': False,
    },
    '--force': {
        'help': 'For the installation no matter any constraints',
        'action': 'store_true',
        'default': False,
    }
}
