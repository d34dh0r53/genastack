# =============================================================================
# Copyright [2013] [Kevin Carter]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================


class CantContinue(Exception):
    """Exception class when the application can't continue."""
    pass


class MD5CheckMismatch(Exception):
    """Exception class when the md5 sum of a file is not what is expected."""
    pass
