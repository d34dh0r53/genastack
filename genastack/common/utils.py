# =============================================================================
# Copyright [2013] [Kevin Carter]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================
import errno
import hashlib
import httplib
import os
import logging
import urlparse

import genastack

LOG = logging.getLogger('genastack-common')


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