# =============================================================================
# Copyright [2013] [Kevin Carter]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================
import grp
import logging
import os
import platform
import pwd
import subprocess
import tarfile

import genastack
from genastack.common import utils
from genastack.common import role_loader
from genastack.common import basic_init

LOG = logging.getLogger('genastack-engine')


class EngineRunner(object):
    """Base class for the engine parser."""

    def __init__(self, args):
        self.args = args

    def __execute_command(self, commands, env=None):
        """Execute a list of commands.

        All commands executed will check for a return code of non-Zero.
        If a non-Zero return code is found an exception will be raised.

        :param commands: ``list``
        :param env: ``dict``
        """

        if self.args.get('debug'):
            output = None
        else:
            output = open(os.devnull, 'wb')

        for command in commands:
            LOG.info('COMMAND: [ %s ]' % command)
            subprocess.check_call(
                command, shell=True, env=env, stdout=output
            )

    def __not_if_exists(self, check):
        """Return False if the constraint is Met otherwise return True.

        :param check: ``dict``
        :return: ``bol``
        """
        if 'not_if_exists' in check and self.args['force'] is False:
            exist = os.path.exists(check['not_if_exists'])
            if exist is True:
                LOG.info(
                    'Build Step skipped due to "not_if_exists"'
                    ' constraint [ %s ]' % check['not_if_exists']
                )
                return True
        return False

    def _ldconfig(self, args):
        """Create lib links on the system.

        :param: args: ``list``
        """
        for ld in args:
            contents, local_file = ld.split('=')
            LOG.info('Settings LD Config [ %s ]' % local_file)
            with open(local_file, 'wb') as f:
                f.write(contents)
        self.__execute_command(commands=['ldconfig'])

    @staticmethod
    def __get(kwargs):
        """Download a remote file to a local place on the system.

        :param kwargs: ``dict``
        """
        url = kwargs.get('url')
        headers = kwargs.get('headers')
        if headers is None:
            headers = {}
        local_path = kwargs.get('path')
        file_name = kwargs.get('name')
        local_file = os.path.join(local_path, file_name)

        LOG.info('Downloading [ %s ] to [ %s ]', url, local_path)
        utils.download(url, headers=headers, local_file=local_file)
        utils.md5_checker(md5sum=kwargs.get('md5sum'), local_file=local_file)
        if kwargs.get('uncompress') is True:
            local_path = kwargs.get('path')

            LOG.info('Uncompressing [ %s ] to [ %s ]', file_name, local_path)
            tarball = os.path.join(local_path, file_name)
            tar = tarfile.open(tarball)
            tar.extractall(path=local_path)
            tar.close()
            file_dir = os.path.splitext(file_name)
            return os.path.join(local_path, file_dir[0])
        else:
            return local_path

    def _pip_install(self, kwargs):
        """Install Python Packages with pip.

        :param kwargs: ``dict``
        """
        pip_packages = kwargs['pip_packages']
        pip_bin = kwargs['pip_bin']
        pip_install_all = ['%s install %s' % (pip_bin, p) for p in pip_packages]
        self.__execute_command(commands=pip_install_all)

    def _init_script(self, kwargs):
        """Place a generic init script on the system.

        :param kwargs: ``dict``
        """
        path = kwargs['path']
        name = kwargs['name']
        kwargs['user'] = 'root'
        kwargs['group'] = 'root'
        kwargs['mode'] = 755
        full_path = os.path.join(path, name)
        kwargs['bin'] = full_path

        script = basic_init.INIT_SCRIPT % kwargs
        kwargs['contents'] = script
        self._file_create(args=[kwargs])

        debian_based, rhel_based = self.__distro_check()
        if debian_based:
            command = ['update-rc.d %(name)s defaults' % kwargs]
        elif rhel_based:
            #TODO(kevin) Support RHEL
            raise genastack.CantContinue('No RHEL Support at this time.')

        self.__execute_command(commands=command)

    def _remote_script(self, kwargs):
        """Execute a remote script on the local system.

        :param kwargs: ``dict``
        """
        get_sources = kwargs['get']
        file_name = os.path.basename(get_sources.get('url'))
        work_path = self.__get(kwargs=get_sources)
        full_path = os.path.join(work_path, file_name)

        interpreter = kwargs.get('interpreter')
        command = '%s %s' % (interpreter, full_path)
        self.__execute_command(commands=[command])

    def _build(self, kwargs):
        """Install a package from source.

        :param: kwargs: ``dict``
        """
        get_sources = kwargs['get']
        work_path = self.__get(kwargs=get_sources)
        cwd = os.getcwd()
        try:
            os.chdir(work_path)
            export_flags = kwargs.get('export')
            file_name = os.path.basename(get_sources.get('url'))

            environment = os.environ.copy()
            if export_flags is not None:
                for export in export_flags:
                    env, contents = export.split('=')
                    environment[env] = contents

            commands = kwargs.get('build_commands')
            if not commands:
                LOG.error(
                    'No configuration script found in [ %s ] for [ %s ]'
                    % (work_path, file_name)
                )
                raise genastack.CantContinue('No configuration script found')

            LOG.info('Building package [ %s ]' % file_name)
            self.__execute_command(commands=commands, env=environment)
        finally:
            os.chdir(cwd)

    def _file_create(self, args):
        """Create local file on the system.

        If the path to the file does not exist, the path will be created.

        :param: args: ``list``
        """
        for file_create in args:
            path = file_create['path']
            name = file_create['name']
            file_path = os.path.join(path, name)
            if not os.path.exists(file_path):
                self._directories(args=[file_create])

                if 'from_remote' in file_create:
                    file_create['url'] = file_create['from_remote']
                    self.__get(kwargs=file_create)
                elif 'contents' in file_create:
                    with open(file_path, 'wb') as local_file:
                        local_file.write(file_create['contents'])

                LOG.info('Created file [ %s ]', file_path)
                self.__set_perms(inode=file_path, kwargs=file_create)


    @staticmethod
    def __set_perms(inode, kwargs):
        """Set the permissions on a local inode.

        :param inode: ``str``
        :param kwargs: ``dict``
        """
        # Get User ID
        _user = kwargs.get('user', 'root')
        user = pwd.getpwnam(_user).pw_uid

        # Get Group ID
        _group = kwargs.get('group', 'root')
        group = grp.getgrnam(_group).gr_gid

        mode = kwargs.get('mode', 0644)
        os.chown(inode, user, group)
        os.chmod(inode, int(mode))
        LOG.info(
            'Permissions Set [ %s ] user=%s, group=%s, mode=%s',
            inode, user, group, mode
        )

    def _directories(self, args):
        """Create local directories on the system.

        :param: args: ``list``
        """
        for directory in args:
            path = directory['path']
            if not os.path.exists(path):
                utils.mkdir_p(path=path)
                self.__set_perms(inode=path, kwargs=directory)

    def __distro_check(self):
        """Return True or False for the detected distro."""
        distro = platform.linux_distribution()
        distro = [d.lower() for d in distro]
        debian_based = any(['ubuntu' in distro, 'debian' in distro])
        rhel_based = any(['centos' in distro, 'redhat' in distro])
        return debian_based, rhel_based

    def _packages(self, kwargs):
        """Install operating system packages for the system.

        :param: kwargs: ``dict``
        """
        debian_based, rhel_based = self.__distro_check()
        if debian_based:
            _packages = kwargs.get('apt')
            packages = ' '.join(_packages)
            apt_update = 'apt-get update'
            apt_install = (
                "apt-get -o Dpkg::Options:='--force-confold'"
                " -o Dpkg::Options:='--force-confdef'"
                " install -y %s" % packages
            )
            commands = [apt_update, apt_install]
            LOG.info('Installing Packages [ %s ]', packages)
            self.__execute_command(commands=commands)
        elif rhel_based:
            #TODO(kevin) Support RHEL
            raise genastack.CantContinue('No RHEL Support at this time.')

    def run(self, init_items):
        """Run the method."""

        if 'required' in init_items:
            libs_list = init_items.pop('required')
            for requirement in libs_list:
                _requirement = role_loader.RoleLoad(config_type=requirement)
                requirement_init = _requirement.load_role()
                self.run(init_items=requirement_init)

        if 'file_create' in init_items:
            self._file_create(args=init_items.pop('file_create'))

        if 'directories' in init_items:
            self._directories(args=init_items.pop('directories'))

        if 'packages' in init_items:
            self._packages(kwargs=init_items.pop('packages'))

        if 'libs' in init_items:
            libs_list = init_items.pop('libs')
            for lib in libs_list:
                lib_init = role_loader.RoleLoad(config_type=lib).load_role()
                build_kwargs = lib_init.pop('build')
                if not self.__not_if_exists(check=build_kwargs):
                    self._build(kwargs=build_kwargs)

        if 'build' in init_items:
            build_kwargs = init_items.pop('build')
            if not self.__not_if_exists(check=build_kwargs):
                self._build(kwargs=build_kwargs)

        if 'ldconfig' in init_items:
            self._ldconfig(args=init_items.pop('ldconfig'))

        if 'remote_script' in init_items:
            self._remote_script(kwargs=init_items.pop('remote_script'))

        if 'pip_install' in init_items:
            self._pip_install(kwargs=init_items.pop('pip_install'))

        if 'init_script' in init_items:
            self._init_script(kwargs=init_items.pop('init_script'))