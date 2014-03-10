# =============================================================================
# Copyright [2013] [Kevin Carter]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================
import argparse

from genastack import arguments
from genastack.common import role_loader


def argument_parser():
    """Setup argument Parsing."""

    parser = argparse.ArgumentParser(
        usage='%(prog)s',
        description='Rackspace Embeded Openstack System Installer',
        epilog='Licensed UNKNOWN')

    args = arguments.DEFAULT_ARGS.items()
    for arg, items in args:
        parser.add_argument(arg, **items)

    subpar = parser.add_subparsers()
    for role in role_loader.RoleLoad(config_type=None).load_all_roles():
        for key, value in role.items():
            base = subpar.add_parser(key)
            base.set_defaults(method=key)
    return parser


def return_args():
    """Return dict of all parsed arguments.

    :return: ``dict``
    """
    args = argument_parser()
    return vars(args.parse_args())


def return_help():
    """Print Help for all available arguments."""
    args = argument_parser()
    args.print_help()
