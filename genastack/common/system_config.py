# =============================================================================
# Copyright [2013] [Kevin Carter]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================
import ConfigParser
import logging
import os
import stat
import sys

import genastack
from genastack import info


LOG = logging.getLogger('genastack-system')


def is_int(value):
    """Return int if the value can be an int.

    :param value: ``str``
    :return: ``int`` :return: ``str``
    """
    try:
        return int(value)
    except ValueError:
        return value


class ConfigurationSetup(object):
    """Parse arguments from a Configuration file.

    Note that anything can be set as a "Section" in the argument file.
    """
    def __init__(self):
        self.args = {}
        # System configuration file
        sys_config = os.path.join('/etc', info.__appname__, 'genastack.conf')

        # User configuration file
        home = os.getenv('HOME')
        user_config = os.path.join(home, 'genastack.conf')

        if os.path.exists(user_config):
            self.config_file = user_config
        elif os.path.exists(sys_config):
            self.config_file = sys_config
        else:
            msg = (
                'Configuration file for genastack was not found. Valid'
                ' configuration files are [ %s ] or [ %s ]'
                % (user_config, sys_config)
            )
            LOG.error(msg)
            raise genastack.CantContinue(msg)

    def config_args(self, section='default'):
        """Loop through the configuration file and set all of our values.

        :param section: ``str``
        :return: ``dict``
        """
        if sys.version_info >= (2, 7, 0):
            parser = ConfigParser.SafeConfigParser(allow_no_value=True)
        else:
            parser = ConfigParser.SafeConfigParser()

        # Set to preserve Case
        parser.optionxform = str

        try:
            parser.read(self.config_file)
            for name, value in parser.items(section):
                name = name.encode('utf8')
                if any([value == 'False', value == 'false']):
                    value = False
                elif any([value == 'True', value == 'true']):
                    value = True
                else:
                    value = is_int(value=value)
                self.args[name] = value
        except Exception as exp:
            LOG.error(
                'Failure Reading in the configuration file. %s' % exp
            )
            return {}
        else:
            return self.args
