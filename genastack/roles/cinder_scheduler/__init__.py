# =============================================================================
# Copyright [2013] [Kevin Carter]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================
from genastack import roles


BIN_PATH = roles.return_rax_dir('bin')


BUILD_DATA = {
    'cinder_api': {
        'help': 'Install Cinder-Scheduler from upstream',
        'required': [
            'python',
            'cinder'
            'cinder_client'
        ],
        'init_script': [
            {
                'help': 'Start and stop cinder scheduler on boot',
                'init_path': '/etc/init.d',
                'bin_path': BIN_PATH,
                'name': 'cinder-scheduler',
                'chuid': 'cinder',
                'options': '--'
                           ' --config-file=/etc/cinder/cinder.conf'
                           ' --log-file=/var/log/cinder/cinder-scheduler.log',
                'chdir': '/var/lib/cinder',
                'program': 'cinder-scheduler'
            }
        ]
    }
}



