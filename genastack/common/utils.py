# =============================================================================
# Copyright [2013] [Kevin Carter]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================
import datetime
import errno
import hashlib
import httplib
import logging
import os
import shelve
import tempfile
import urlparse

import genastack

LOG = logging.getLogger('genastack-common')


RAX_BASE = 'openstack'


def update_installed(db, method):
    """Write a method to the installed DB.

    :param db: ``dict``
    :param method: ``str``
    """
    db[method] = str(datetime.datetime.utcnow())


def octal_converter(num):
    """Return an octal value from a string.

    :param num: ``str``
    """
    return int(num, 8)


def return_rax_dir(path=None):
    """Return python installation path.

    :return: ``str``
    """
    if path is None:
        return os.path.join('/opt', RAX_BASE)
    else:
        return os.path.join('/opt', RAX_BASE, path)


def return_temp_dir():
    """Return a securely created temp directory.

    :return: ``str``
    """
    temp = tempfile.gettempdir()
    rax = os.path.join(temp, '%s_build' % RAX_BASE)
    mkdir_p(rax)
    return tempfile.mkdtemp(prefix='build_temp_', dir=rax)


def dbm_create(db_path, db_name, db_key):
    """Create a DBM.

    :param db_path: Path to a directory
    :param db_name: Name of DBM
    """
    db_path = os.path.expanduser(db_path)
    if not os.path.exists(db_path):
        os.mkdir(db_path)

    database_path = os.path.join(db_path, '%s.dbm' % db_name)
    with Shelve(file_path=database_path) as db:
        host = db.get(db_key)
        if host is None:
            db[db_key] = {}

    return database_path


def get_db_section(dbk, section):
    """Return a section of the local DBM.

    :param dbk: ``dict``
    :param section: ``str``
    """
    db_section = dbk.get(section)
    if db_section is None:
        db_section = dbk[section] = {}
    return db_section


def job_status_saver(db_path, db_key, section, args, status):
    """Open a dbm and write out the status of an action.

    :param db_path: ``str``
    :param db_key: ``str``
    :param section: ``str``
    :param args: ``dict``
    :param status: ``str``
    """
    with Shelve(file_path=db_path) as db:
        dbk = db.get(db_key)
        db_section = get_db_section(dbk=dbk, section=section)
        db_section['complete'] = status
        db_section['args'] = args


def load_saved_args(db_path, db_key, section, args):
    """Return new section from the local DB.

    :param db_path: ``str``
    :param db_key: ``str``
    :param section: ``str``
    :param args: ``dict``
    :return: ``dict``
    """
    with Shelve(file_path=db_path) as db:
        dbk = db.get(db_key)
        db_section = get_db_section(dbk=dbk, section=section)
        if 'args' in db_section:
            new_args = section.copy()
            new_args.update(args)
            return new_args
        else:
            return args


class Shelve(object):
    """Context Manager for opening and closing access to the DBM."""
    def __init__(self, file_path):
        """Set the Path to the DBM to create/Open.

        :param file_path: Full path to file
        """

        self.shelve = file_path
        self.open_shelve = None

    def __enter__(self):
        """Open the DBM in r/w mode.

        :return: Open DBM
        """

        self.open_shelve = shelve.open(self.shelve, writeback=True)
        return self.open_shelve

    def __exit__(self, type, value, traceback):
        """Close DBM Connection."""

        self.open_shelve.sync()
        self.open_shelve.close()


class OpenConnection(object):
    """Open an Http Connection and return the connection object.

    :param url:
    :return conn:
    """
    def __init__(self, url):
        self.url = url
        self.conn = None

    def __enter__(self):
        try:
            if self.url.scheme == 'https':
                self.conn = httplib.HTTPSConnection(self.url.netloc)
            else:
                self.conn = httplib.HTTPConnection(self.url.netloc)
        except httplib.InvalidURL as exc:
            msg = 'ERROR: %s - Connection: %s' % (exc, self.url)
            raise httplib.CannotSendRequest(msg)
        else:
            return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


def download(url, headers, local_file, depth=0):
    """Perform Object GET.

    This will save the object contents in the local file.

    :param url: ``str``
    :param headers: ``dict``
    :param local_file: ``dict``
    """
    if depth > 10:
        raise httplib.HTTPException("Too many redirects...")

    encoded_url = urlparse.urlparse(url)
    with OpenConnection(url=encoded_url) as conn:
        conn.request('GET', encoded_url.path, headers=headers)
        resp = conn.getresponse()
        LOG.info('REQUEST: %s %s %s', resp.status, resp.reason, resp.msg)

        return_headers = dict(resp.getheaders())
        location = return_headers.get('location')
        if location is not None and location != url:
            depth += 1
            return download(
                return_headers['location'],
                headers=headers,
                local_file=local_file,
                depth=depth
            )
        else:
            with open(local_file, 'w') as f_name:
                while True:
                    chunk = resp.read(2048)
                    if not chunk:
                        break
                    else:
                        f_name.write(chunk)


def mkdir_p(path):
    """'mkdir -p' in Python

    :param path: ``str``
    """
    try:
        if not os.path.isdir(path):
            os.makedirs(path)
            LOG.info('Created Directory [ %s ]', path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise OSError(
                'The provided path can not be turned into a directory.'
            )


def md5_checker(md5sum, local_file):
    """Return True if the MD5sum of a downloaded file is expected.

    Additionally, if md5sum is None Return True.

    :param md5sum: ``str``
    :param local_file: ``str``
    :return: ``bol``
    """
    def calc_hash():
        """Read the hash.

        :return data_hash.read():
        """
        return data_hash.read(128 * md5.block_size)

    if md5sum is None:
        LOG.warn(
            'No md5sum provided for the downloaded file [ %s ]' % local_file
        )
        return True

    if os.path.isfile(local_file) is True:
        md5 = hashlib.md5()

        with open(local_file, 'rb') as data_hash:
            for chk in iter(calc_hash, ''):
                md5.update(chk)

        lmd5sum = md5.hexdigest()
        if md5sum != lmd5sum:
            msg = (
                'CheckSumm Mis-Match "%s" != "%s" for [ %s ]'
                % (md5sum, lmd5sum, local_file)
            )
            LOG.critical(msg)
            raise genastack.MD5CheckMismatch(msg)
        else:
            LOG.info(
                'Download Successful, md5sum verified for [ %s ]' % local_file
            )
            return True
