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

from genastack.common import logger
from genastack.arguments import parser
from genastack.common import role_loader
from genastack.common import build_engine


def executable():
    """Start."""
    if len(sys.argv) < 2:
        parser.return_help()
        raise SystemExit('Not command provided.')
    else:
        args = parser.return_args()
        debug = args.get('debug')

        handlers = ['genastack-common', 'genastack-engine']
        for handler in handlers:
            logger.logger_setup(name=handler, debug_logging=debug)

        method = args.get('method')
        if method is None:
            raise SystemExit('No Method Found')
        else:
            build_data = role_loader.RoleLoad(config_type=method).load_role()
            if args.get('print_only') is True:
                print json.dumps(build_data, indent=2)
            else:
                engine = build_engine.EngineRunner(args=args)
                engine.run(init_items=build_data)


if __name__ == '__main__':
    executable()
