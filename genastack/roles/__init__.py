# =============================================================================
# Copyright [2013] [Kevin Carter]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================
import os
import tempfile

from genastack.common import utils


RAX_BASE = 'rackspace'


def return_rax_dir(path=None):
    """Return python installation path.

    :return: ``str``
    """
    if path is None:
        return os.path.join('/opt', 'rackspace')
    else:
        return os.path.join('/opt', 'rackspace', path)


def return_temp_dir():
    """Return a securely created temp directory.

    :return: ``str``
    """
    temp = tempfile.gettempdir()
    rax = os.path.join(temp, 'rackspace_build')
    utils.mkdir_p(rax)
    return tempfile.mkdtemp(prefix='build_temp_', dir=rax)
