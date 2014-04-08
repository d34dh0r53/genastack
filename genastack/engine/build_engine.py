# =============================================================================
# Copyright [2013] [Kevin Carter]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================
import collections
import grp
import logging
import os
import platform
import pwd
import subprocess
import shutil
import tarfile

import genastack
from genastack.common import basic_init
from genastack.common import role_loader
from genastack.common import utils


LOG = logging.getLogger('genastack-engine')


class EngineRunner(object):
    """Base class for the engine parser."""

    def __init__(self, args):
        self.args = args
        self.run_roles = []
        self.install_db = None
        self.job_dict = collections.defaultdict(list)

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

        _mode = kwargs.get('mode', '0644')
        os.chown(inode, user, group)
        os.chmod(inode, utils.octal_converter(_mode))
        LOG.info(
            'Permissions Set [ %s ] user=%s, group=%s, mode=%s',
            inode, user, group, _mode
        )

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

    def __execute_command(self, commands, env=None, execute='/bin/bash'):
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
                command, shell=True, env=env, stdout=output, executable=execute
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

        :param: args: ``dict``
        """
        for ld in args:
            contents, local_file = ld.split('=')
            LOG.info('Settings LD Config [ %s ]' % local_file)
            with open(local_file, 'wb') as f:
                f.write(contents)
        self.__execute_command(commands=['ldconfig'])

    def _pip_install(self, args):
        """Install Python Packages with pip.

        :param args: ``dict``
        """
        pip_install_all = ['pip install %s' % p for p in args]
        self.__execute_command(commands=pip_install_all)

    def _git_install(self, args):
        """Install Python Software from Git.

        While we could do this with "pip" we are providing the ability to copy
        default configuration and or exampls in place, thus raw "pip" is not
        the better choice.

        example = {
            'project_url': PROJECT_URL,
            'branch': BRANCH,
            'config_example': ['etc/nova=/etc/nova'],
        }

        :param args: ``dict``
        """
        def configure_repo():
            if 'config_example' in repo:
                relative, local_path = repo['config_example'].split('=')
                full_relative_path = os.path.realpath(relative)
                file_lists = []
                for root, source, file_name in os.walk(full_relative_path):
                    for config_file in file_name:
                        file_lists.append(os.path.join(root, config_file))

                create_files = []
                LOG.debug('local files found [ %s ]', file_lists)
                for local_file in file_lists:
                    # Open local file and read it
                    file_name = local_file.split(
                        full_relative_path
                    )
                    file_name = file_name[-1].strip(os.sep)
                    with open(local_file, 'rb') as f:
                        file_create = {
                            'path': local_path,
                            'name': file_name,
                            'contents': f.read(),
                            'group': repo.get('group_owner', 'root'),
                            'user': repo.get('user_owner', 'root'),
                            'mode': repo.get('mode', '0644')
                        }
                    create_files.append(file_create)
                else:
                    self._file_create(args=create_files)

        cwd = os.getcwd()
        for repo in args:
            temp_dir = utils.return_temp_dir()
            try:
                name = repo['name']
                os.chdir(temp_dir)
                git_setup = [
                    'git clone "%s" "%s"' % (repo['project_url'], name),
                ]
                self.__execute_command(commands=git_setup)
                clone_path = os.path.join(temp_dir, name)
                os.chdir(clone_path)
                commands = [
                    'git checkout %s' % repo['branch'],
                    'python setup.py install'
                ]
                self.__execute_command(commands=commands)
                configure_repo()
            finally:
                os.chdir(cwd)
                shutil.rmtree(temp_dir)

    def _init_script(self, args):
        """Place a generic init script on the system.

        :param args: ``dict``
        """
        for script in args:
            name = script['program']
            script['bin'] = name
            script['exec'] = ' '.join(['${DAEMON}', script.get('options', '')])
            script['pid_file'] = '/var/run/%s.pid' % name

            ssd = [
                '--start',
                '--background',
                '--make-pidfile',
                '--pidfile ${PID_FILE}'
            ]

            if 'chuid' in script:
                ssd.append('--chuid %s' % script['chuid'])

            if 'chdir' in script:
                ssd.append('--chdir %s' % script['chdir'])

            ssd.append('--exec %(exec)s')
            script['start_stop_daemon'] = ' '.join(ssd) % script

            file_create = {
                'path': script['init_path'],
                'name': script['name'],
                'contents': basic_init.INIT_SCRIPT % script,
                'group': 'root',
                'user': 'root',
                'mode': '0755'
            }

            self._file_create(args=[file_create])

            distro = self.__distro_check()
            if distro == 'apt_packages':
                command = ['update-rc.d %(name)s defaults' % script]
            elif distro == 'yum_packages':
                command = ['chkconfig on %(name)s' % script]
                #TODO(kevin) Support RHEL
                raise genastack.CantContinue('No RHEL Support at this time.')
            else:
                raise genastack.CantContinue('Unkown Init System...')

            self.__execute_command(commands=command)

    def __script_run(self, kwargs):
        """Run a script.

        :param kwargs: ``dict``
        """
        get_sources = kwargs['get']
        file_name = os.path.basename(get_sources.get('url'))
        work_path = self.__get(kwargs=get_sources)
        full_path = os.path.join(work_path, file_name)

        interpreter = kwargs.get('interpreter')
        command = '%s %s' % (interpreter, full_path)
        self.__execute_command(commands=[command])

    def _remote_script(self, args):
        """Execute a remote script on the local system.

        :param kwargs: ``dict``
        """
        for script in args:
            if not self.__not_if_exists(check=script):
                self.__script_run(kwargs=script)

    def __compiler(self, kwargs):
        """Install an application.

        :param kwargs: ``dict``
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

    def _build(self, args):
        """Confirm a package needs to be install, if so go to the compiler.

        :param: args: ``dict``
        """

        for build in args:
            if self.__not_if_exists(check=build) is False:
                self.__compiler(kwargs=build)

    def _group_create(self, args):
        """Create local file on the system.

        If the path to the file does not exist, the path will be created.

        :param: args: ``dict``
        """
        for group_create in args:
            try:
                grp.getgrnam(group_create.get('group'))
            except KeyError:
                group = ['groupadd']

                # Basic user or System user
                if group_create.get('system') is True:
                    user_type = '--system %(group)s'
                else:
                    user_type = '%(group)s'

                group.append(user_type)
                command = [' '.join(group) % group_create]
                self.__execute_command(commands=command)
                LOG.info('Group Created [ %s ]', group_create['group'])
            else:
                LOG.info(
                    'No Group Created it already Exists [ %s ]',
                    group_create['group']
                )

    def _user_create(self, args):
        """Create local file on the system.

        If the path to the file does not exist, the path will be created.

        :param: args: ``dict``
        """
        for user_create in args:
            username = user_create.get('user')
            try:
                pwd.getpwnam(username)
            except KeyError:
                user = ['useradd']
                # Group assignment
                no_group = user_create.get('no_group', False)
                group = user_create.get('group', username)
                if no_group is True or group is None:
                    user.append('--no-user-group')
                else:
                    user.append('--gid %(group)s')

                # User assignment
                no_home = user_create.get('no_home')
                home = user_create.get('home', os.path.join('/home', username))
                if no_home is True or home is None:
                    user.append('--no-create-home')
                else:
                    user.append('--create-home --home-dir %(home)s')

                # Set the user shell
                shell = user_create.get('shell', '/bin/false')
                user.append('--shell %s' % shell)

                # Basic user or System user
                if user_create.get('system') is True:
                    user_type = '--system %(user)s'
                else:
                    user_type = '%(user)s'

                user.append(user_type)
                command = [' '.join(user) % user_create]
                self.__execute_command(commands=command)
                LOG.info('User Created [ %s ]', user_create['user'])
            else:
                LOG.info(
                    'No User Created it already Exists [ %s ]',
                    user_create['user']
                )

    def _file_create(self, args):
        """Create local file on the system.

        If the path to the file does not exist, the path will be created.

        :param: args: ``dict``
        """
        for file_create in args:
            file_path = os.path.join(file_create['path'], file_create['name'])
            if not os.path.exists(file_path):
                self._directories(
                    args=[file_create],
                    mode_if='0755'
                )

                if 'from_remote' in file_create:
                    file_create['url'] = file_create['from_remote']
                    self.__get(kwargs=file_create)
                elif 'contents' in file_create:
                    with open(file_path, 'wb') as f:
                        f.write(file_create['contents'])
                else:
                    raise genastack.CantContinue('no file to create')

                LOG.info('Created file [ %s ]', file_path)
                self.__set_perms(inode=file_path, kwargs=file_create)
            else:
                LOG.info('File not created it exists [ %s ]', file_path)

    def _directories(self, args, mode_if=None):
        """Create local directories on the system.

        :param: args: ``dict``
        :param: mode_if: ``int``
        """
        for directory in args:
            path = directory['path']
            if 'name' in directory:
                full_path = os.path.join(path, directory['name'])
                path = os.path.dirname(full_path)

            if os.path.isdir(path) is False:
                utils.mkdir_p(path=path)
                if mode_if is not None:
                    directory['mode'] = mode_if
                elif 'mode' not in directory:
                    directory['mode'] = '0755'

                self.__set_perms(inode=path, kwargs=directory)

    def __distro_check(self):
        """Return True or False for the detected distro."""
        distro = platform.linux_distribution()
        distro = [d.lower() for d in distro]
        if any(['ubuntu' in distro, 'debian' in distro]) is True:
            return 'apt_packages'
        elif any(['centos' in distro, 'redhat' in distro]) is True:
            return 'yum_packages'
        else:
            raise genastack.CantContinue(
                'Distro [ %s ] is unsupported.' % distro
            )

    def _yum_packages(self, args):
        """Install operating system packages for the system.

        :param: kwargs: ``dict``
        """
        packages = ' '.join(args)
        # yum_install = 'yum -y install %s' % packages
        # commands = [yum_install]
        LOG.info('Installing Packages [ %s ]', packages)
        # self.__execute_command(commands=commands)

        #TODO(kevin) Support RHEL
        raise genastack.CantContinue('No RHEL Support at this time.')

    def _apt_packages(self, args):
        """Install operating system packages for the system.

        :param: kwargs: ``dict``
        """
        packages = ' '.join(args)
        apt_update = 'apt-get update'
        apt_install = (
            "apt-get -o Dpkg::Options:='--force-confold'"
            " -o Dpkg::Options:='--force-confdef'"
            " install -y %s" % packages
        )
        commands = [apt_update, apt_install]
        LOG.info('Installing Packages [ %s ]', packages)
        self.__execute_command(commands=commands)

    def get_required(self, args, pop):
        """Populate all required roles in the required_roles ``list``.

        :param args: ``list``
        :param pop: ``str``
        """
        force = self.args.get('force')
        for req in args:
            if req in self.run_roles:
                pass
            elif req not in self.install_db or force is True:
                self.run_roles.append(req)
                _requirement = role_loader.RoleLoad(config_type=req)
                requirement = _requirement.load_role()
                if pop in requirement:
                    required = requirement.pop(pop)
                    self.get_required(args=required, pop=pop)
                self.merge_init_items(items=requirement)
            else:
                LOG.info('Role [ %s ] already installed', req)

    def merge_init_items(self, items):
        """Build the job dict merging the dicts of other resources.

        :param items: ``dict``
        """
        for key, value in items.iteritems():
            if isinstance(value, list):
                for item in value:
                    if item not in self.job_dict[key]:
                        self.job_dict[key].append(item)
            else:
                if value not in self.job_dict[key]:
                    self.job_dict[key].append(value)

    def _execute(self, args):
        """Execute some raw commands.

        :param: args: ``list``
        """
        self.__execute_command(commands=args)

    def run(self, init_items, install_db):
        """Run the method.

        :param init_items: ``dict``
        """
        self.install_db = install_db
        LOG.info('Understanding the scope of work')
        self.merge_init_items(items=init_items)

        if 'required' in init_items:
            required_roles = init_items.pop('required')
            self.get_required(args=required_roles, pop='required')

        if 'libs' in self.job_dict:
            libs_list = self.job_dict.pop('libs')
            self.get_required(args=libs_list, pop='libs')

        LOG.info('Installation Information: %s', self.job_dict.pop('help'))
        if self.args.get('print_only') is True:
            return self.job_dict

        run_list = [
            'group_create',
            'user_create',
            'directories',
            'file_create',
            self.__distro_check(),
            'build',
            'ldconfig',
            'remote_script',
            'pip_install',
            'git_install',
            'init_script',
            'execute'
        ]

        for run in run_list:
            if run in self.job_dict:
                run_command = '_%s' % run
                if hasattr(self, run_command):
                    action = getattr(self, run_command)
                    action(args=self.job_dict.pop(run))

        for role in self.run_roles:
            utils.update_installed(db=self.install_db, method=role)

        return 'success'
