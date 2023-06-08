# Copyright 2020 Inspur
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
  CLI interface for venus management.
"""

from __future__ import print_function

import os
import sys

from oslo_config import cfg
from oslo_log import log as logging

from venus.conf import CONF

from venus import context
from venus import db
from venus import i18n
from venus import objects
from venus import version

from venus.db import migration as db_migration
from venus.i18n import _
from venus.task import timer

i18n.enable_lazy()


# Decorators for actions
def args(*args, **kwargs):
    def _decorator(func):
        func.__dict__.setdefault('args', []).insert(0, (args, kwargs))
        return func

    return _decorator


class ShellCommands(object):
    def bpython(self):
        """Runs a bpython shell.

        Falls back to Ipython/python shell if unavailable
        """
        self.run('bpython')

    def ipython(self):
        """Runs an Ipython shell.

        Falls back to Python shell if unavailable
        """
        self.run('ipython')

    def python(self):
        """Runs a python shell.

        Falls back to Python shell if unavailable
        """
        self.run('python')

    @args('--shell', dest="shell",
          metavar='<bpython|ipython|python>',
          help='Python shell')
    def run(self, shell=None):
        """Runs a Python interactive interpreter."""
        if not shell:
            shell = 'bpython'

        if shell == 'bpython':
            try:
                import bpython
                bpython.embed()
            except ImportError:
                shell = 'ipython'
        if shell == 'ipython':
            try:
                from IPython import embed
                embed()
            except ImportError:
                try:
                    # Ipython < 0.11
                    # Explicitly pass an empty list as arguments, because
                    # otherwise IPython would use sys.argv from this script.
                    import IPython

                    shell = IPython.Shell.IPShell(argv=[])
                    shell.mainloop()
                except ImportError:
                    # no IPython module
                    shell = 'python'

        if shell == 'python':
            import code
            try:
                # Try activating rlcompleter, because it's handy.
                import readline
            except ImportError:
                pass
            else:
                # We don't have to wrap the following import in a 'try',
                # because we already know 'readline' was imported successfully.
                import rlcompleter  # noqa
                readline.parse_and_bind("tab:complete")
            code.interact()

            # @args('--path', required=True, help='Script path')
            # def script(self, path):


def _db_error(caught_exception):
    print('%s' % caught_exception)
    print(_("The above error may show that the database has not "
            "been created.\nPlease create a database using "
            "'venus-manage db sync' before running this command."))
    exit(1)


class VersionCommands(object):
    """Class for exposing the codebase version."""

    def __init__(self):
        pass

    def list(self):
        print(version.version_string())

    def __call__(self):
        self.list()


class ConfigCommands(object):
    """Class for exposing the flags defined by flag_file(s)."""

    def __init__(self):
        pass

    @args('param', nargs='?', default=None,
          help='Configuration parameter to display (default: %(default)s)')
    def list(self, param=None):
        """List parameters configured for venus.

        Lists all parameters configured for venus unless an optional argument
        is specified.  If the parameter is specified we only print the
        requested parameter.  If the parameter is not found an appropriate
        error is produced by .get*().
        """
        param = param and param.strip()
        if param:
            print('%s = %s' % (param, CONF.get(param)))
        else:
            for key, value in CONF.items():
                print('%s = %s' % (key, value))


class GetLogCommands(object):
    """Get logging information."""

    def errors(self):
        """Get all of the errors from the log files."""
        error_found = 0
        if CONF.log_dir:
            logs = [x for x in os.listdir(CONF.log_dir) if x.endswith('.log')]
            for file in logs:
                log_file = os.path.join(CONF.log_dir, file)
                lines = [line.strip() for line in open(log_file, "r")]
                lines.reverse()
                print_name = 0
                for index, line in enumerate(lines):
                    if line.find(" ERROR ") > 0:
                        error_found += 1
                        if print_name == 0:
                            print(log_file + ":-")
                            print_name = 1
                        print(_("Line %(dis)d : %(line)s") %
                              {'dis': len(lines) - index, 'line': line})
        if error_found == 0:
            print(_("No errors in logfiles!"))

    @args('num_entries', nargs='?', type=int, default=10,
          help='Number of entries to list (default: %(default)d)')
    def syslog(self, num_entries=10):
        """Get <num_entries> of the venus syslog events."""
        entries = int(num_entries)
        count = 0
        if os.path.exists('/var/log/syslog'):
            log_file = '/var/log/syslog'
        elif os.path.exists('/var/log/messages'):
            log_file = '/var/log/messages'
        else:
            print(_("Unable to find system log file!"))
            sys.exit(1)
        lines = [line.strip() for line in open(log_file, "r")]
        lines.reverse()
        print(_("Last %s venus syslog entries:-") % entries)
        for line in lines:
            if line.find("venus") > 0:
                count += 1
                print(_("%s") % line)
            if count == entries:
                break

        if count == 0:
            print(_("No venus entries in syslog!"))


class TaskCommands(object):
    """Class for managing the database."""

    def __init__(self):
        pass

    def start(self):
        timer.init_advanced_timer()


class DbCommands(object):
    """Class for managing the database."""

    def __init__(self):
        pass

    @args('version', nargs='?', default=None,
          help='Database version')
    def sync(self, version=None):
        """Sync the database up to the most recent version."""
        return db_migration.db_sync(version)

    def version(self):
        """Print the current database version."""
        print(db_migration.db_version())

    @args('age_in_days', type=int,
          help='Purge deleted rows older than age in days')
    def purge(self, age_in_days):
        """Purge deleted rows older than a given age from venus tables."""
        age_in_days = int(age_in_days)
        if age_in_days <= 0:
            print(_("Must supply a positive, non-zero value for age"))
            exit(1)
        ctxt = context.get_admin_context()
        db.purge_deleted_rows(ctxt, age_in_days)


CATEGORIES = {
    'config': ConfigCommands,
    'db': DbCommands,
    'logs': GetLogCommands,
    'shell': ShellCommands,
    'version': VersionCommands,
    'task': TaskCommands
}


def methods_of(obj):
    """Return non-private methods from an object.

    Get all callable methods of an object that don't start with underscore
    :return: a list of tuples of the form (method_name, method)
    """
    result = []
    for i in dir(obj):
        if callable(getattr(obj, i)) and not i.startswith('_'):
            result.append((i, getattr(obj, i)))
    return result


def add_command_parsers(subparsers):
    for category in CATEGORIES:
        command_object = CATEGORIES[category]()

        parser = subparsers.add_parser(category)
        parser.set_defaults(command_object=command_object)

        category_subparsers = parser.add_subparsers(dest='action')

        for (action, action_fn) in methods_of(command_object):
            parser = category_subparsers.add_parser(action)

            action_kwargs = []
            for args, kwargs in getattr(action_fn, 'args', []):
                parser.add_argument(*args, **kwargs)

            parser.set_defaults(action_fn=action_fn)
            parser.set_defaults(action_kwargs=action_kwargs)


category_opt = cfg.SubCommandOpt('category',
                                 title='Command categories',
                                 handler=add_command_parsers)


def get_arg_string(args):
    if args[0] == '-':
        # (Note)zhiteng: args starts with FLAGS.oparser.prefix_chars
        # is optional args. Notice that cfg module takes care of
        # actual ArgParser so prefix_chars is always '-'.
        if args[1] == '-':
            # This is long optional arg
            arg = args[2:]
        else:
            arg = args[1:]
    else:
        arg = args

    return arg


def fetch_func_args(func):
    fn_args = []
    for args, kwargs in getattr(func, 'args', []):
        arg = get_arg_string(args[0])
        fn_args.append(getattr(CONF.category, arg))

    return fn_args


def main():
    objects.register_all()
    """Parse options and call the appropriate class/method."""
    CONF.register_cli_opt(category_opt)
    script_name = sys.argv[0]
    if len(sys.argv) < 2:
        print(_("\nOpenStack Venus version: %(version)s\n") %
              {'version': version.version_string()})
        print(script_name + " category action [<args>]")
        print(_("Available categories:"))
        for category in CATEGORIES:
            print(_("\t%s") % category)
        sys.exit(2)

    try:
        CONF(sys.argv[1:], project='venus',
             version=version.version_string())
        # logdir = CONF.log_dir
        # is_exits = os.path.exists(logdir)
        # if not is_exits:
        #     os.makedirs(logdir)
        logging.setup(CONF, "venus")
    except cfg.ConfigDirNotFoundError as details:
        print(_("Invalid directory: %s") % details)
        sys.exit(2)
    except cfg.ConfigFilesNotFoundError:
        cfgfile = CONF.config_file[-1] if CONF.config_file else None
        if cfgfile and not os.access(cfgfile, os.R_OK):
            st = os.stat(cfgfile)
            print(_("Could not read %s. Re-running with sudo") % cfgfile)
            try:
                os.execvp('sudo', ['sudo', '-u', '#%s' % st.st_uid] + sys.argv)
            except Exception:
                print(_('sudo failed, continuing as if nothing happened'))

        print(_('Please re-run venus-manage as root.'))
        sys.exit(2)

    fn = CONF.category.action_fn
    fn_args = fetch_func_args(fn)
    fn(*fn_args)


if __name__ == "__main__":
    main()
