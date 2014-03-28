# =============================================================================
# Copyright [2013] [Kevin Carter]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================
import logging
import pkgutil

import genastack
from genastack import roles


LOG = logging.getLogger('genastack-engine')


class RoleLoad(object):
    """Load a given Configuration Management role.

    :param config_type: ``str``
    """

    def __init__(self, config_type):
        self.config_type = config_type

    def get_method(self, method, name):
        """Import what is required to run the System.

        :param method:
        :param name:
        """

        to_import = '%s.%s' % (method.__name__, name)
        return __import__(to_import, fromlist="None")

    def validate_role(self):
        """Return True if a role is importable.

        :return: ``bol``
        """
        try:
            self.load_role()
        except genastack.CantContinue:
            return False
        else:
            return True

    def load_all_roles(self):
        for mod, name, package in pkgutil.iter_modules(roles.__path__):
            try:
                method = self.get_method(method=roles, name=name)
                LOG.info('Loading Role [ %s ]' % name)
                yield method.BUILD_DATA
            except Exception as exp:
                msg = 'role [ %s ] failed to load, error [ %s ]' % (name, exp)
                LOG.error(msg)
                raise genastack.CantContinue(msg)

    def load_role(self):
        """Return role dictionary map if it is importable.

        :return: ``dict``
        """
        for mod, name, package in pkgutil.iter_modules(roles.__path__):
            try:
                method = self.get_method(method=roles, name=name)
                self.config_type = self.config_type.replace('-', '_')
                if self.config_type in method.BUILD_DATA:
                    LOG.info('Loading Role [ %s ]' % name)
                    return method.BUILD_DATA[self.config_type]
            except Exception:
                msg = 'role [ %s ] failed to load correctly' % name
                LOG.error(msg)
                raise genastack.CantContinue(msg)
        else:
            msg = 'no role [ %s ] found' % self.config_type
            LOG.warn(msg)
            raise genastack.CantContinue(msg)
