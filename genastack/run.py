# =============================================================================
# Copyright [2013] [Kevin Carter]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================
import sys
import json

from genastack.arguments import parser
from genastack.common import logger
from genastack.common import role_loader
from genastack.common import system_config
from genastack.common import utils
from genastack.engine import build_engine


# Check to see if our System Config File Exists
system_config.ConfigurationSetup()


def executable(debug=False):
    """Start."""
    if len(sys.argv) < 2:
        parser.return_help()
        raise SystemExit('Not command provided.')
    else:
        args = parser.return_args()
        debug = args.get('debug')

        handlers = ['genastack-system', 'genastack-common', 'genastack-engine']
        for handler in handlers:
            logger.logger_setup(name=handler, debug_logging=debug)

        method = args.get('method')
        if method is None:
            raise SystemExit('No Method Found')
        else:
            # Create our living log of what has been installed on this system
            # presently only support running the client on localhost.
            database_path = utils.dbm_create(
                db_path=utils.return_rax_dir(),
                db_name='openstack_installation',
                db_key='openstack_installation'
            )
            _run_genastack(method, database_path, args)


def _run_genastack(method, database_path, args):
    """Run genastack.

    :param method: ``str``
    :param database_path: ``str``
    :param args: ``dict``
    """
    with utils.Shelve(file_path=database_path) as db:
        host_db = db['openstack_installation']
        if method == 'installed_roles':
            print(json.dumps({'installed_roles': host_db}, indent=4))
            return

        role = role_loader.RoleLoad(config_type=method).load_role()
        if 'required' not in role:
            role['required'] = [method]
        else:
            if method not in role['required']:
                role['required'].append(method)

        # Check to see if the role is installed
        # or if force / print_only are true
        possible_args = [
            method not in host_db,
            args.get('force') is True,
            args.get('print_only') is True
        ]
        if any(possible_args):
            engine = build_engine.EngineRunner(args=args)
            run_results = engine.run(
                init_items=role, install_db=host_db
            )
            print(json.dumps(run_results, indent=4))
        else:
            print('Role [ %s ] is already installed.' % method)


if __name__ == '__main__':
    executable()
