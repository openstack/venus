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

"""Utilities and helper functions."""

import abc
import contextlib
import functools
import hashlib
import inspect
import logging as py_logging
import os
import pyclbr
import random
import re
import shutil
import socket
import stat
import sys
import tempfile
import time
import types
from xml.dom import minidom
from xml.parsers import expat
from xml import sax
from xml.sax import expatreader
from xml.sax import saxutils

from oslo_concurrency import lockutils
from oslo_concurrency import processutils
from oslo_config import cfg
from oslo_log import log as logging
from oslo_utils import importutils
from oslo_utils import strutils
from oslo_utils import timeutils
import retrying

from venus import exception
from venus.i18n import _, _LW


CONF = cfg.CONF
LOG = logging.getLogger(__name__)
ISO_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
PERFECT_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
VALID_TRACE_FLAGS = {'method', 'api'}
TRACE_METHOD = False
TRACE_API = False

synchronized = lockutils.synchronized_with_prefix('venus-')


def find_config(config_path):
    """Find a configuration file using the given hint.

    :param config_path: Full or relative path to the config.
    :returns: Full path of the config, if it exists.
    :raises: `venus.exception.ConfigNotFound`

    """
    possible_locations = [
        config_path,
        os.path.join(CONF.state_path, "etc", "venus", config_path),
        os.path.join(CONF.state_path, "etc", config_path),
        os.path.join(CONF.state_path, config_path),
        "/etc/venus/%s" % config_path,
    ]

    for path in possible_locations:
        if os.path.exists(path):
            return os.path.abspath(path)

    raise exception.ConfigNotFound(path=os.path.abspath(config_path))


def as_int(obj, quiet=True):
    # Try "2" -> 2
    try:
        return int(obj)
    except (ValueError, TypeError):
        pass
    # Try "2.5" -> 2
    try:
        return int(float(obj))
    except (ValueError, TypeError):
        pass
    # Eck, not sure what this is then.
    if not quiet:
        raise TypeError(_("Can not translate %s to integer.") % obj)
    return obj


def is_int_like(val):
    """Check if a value looks like an int."""
    try:
        return str(int(val)) == str(val)
    except Exception:
        return False


def check_exclusive_options(**kwargs):
    """Checks that only one of the provided options is actually not-none.

    Iterates over all the kwargs passed in and checks that only one of said
    arguments is not-none, if more than one is not-none then an exception will
    be raised with the names of those arguments who were not-none.
    """

    if not kwargs:
        return

    pretty_keys = kwargs.pop("pretty_keys", True)
    exclusive_options = {}
    for (k, v) in kwargs.items():
        if v is not None:
            exclusive_options[k] = True

    if len(exclusive_options) > 1:
        # Change the format of the names from pythonic to
        # something that is more readable.
        #
        # Ex: 'the_key' -> 'the key'
        if pretty_keys:
            names = [k.replace('_', ' ') for k in kwargs.keys()]
        else:
            names = kwargs.keys()
        names = ", ".join(sorted(names))
        msg = (_("May specify only one of %s") % names)
        raise exception.InvalidInput(reason=msg)


def execute(*cmd, **kwargs):
    """Convenience wrapper around oslo's execute() method."""
    if 'run_as_root' in kwargs and 'root_helper' not in kwargs:
        kwargs['root_helper'] = get_root_helper()
    return processutils.execute(*cmd, **kwargs)


def check_ssh_injection(cmd_list):
    ssh_injection_pattern = ['`', '$', '|', '||', ';', '&', '&&', '>', '>>',
                             '<']

    # Check whether injection attacks exist
    for arg in cmd_list:
        arg = arg.strip()

        # Check for matching quotes on the ends
        is_quoted = re.match('^(?P<quote>[\'"])(?P<quoted>.*)(?P=quote)$', arg)
        if is_quoted:
            # Check for unescaped quotes within the quoted argument
            quoted = is_quoted.group('quoted')
            if quoted:
                if (re.match('[\'"]', quoted) or
                        re.search('[^\\\\][\'"]', quoted)):
                    raise exception.SSHInjectionThreat(command=cmd_list)
        else:
            # We only allow spaces within quoted arguments, and that
            # is the only special character allowed within quotes
            if len(arg.split()) > 1:
                raise exception.SSHInjectionThreat(command=cmd_list)

        # Second, check whether danger character in command. So the shell
        # special operator must be a single argument.
        for c in ssh_injection_pattern:
            if c not in arg:
                continue

            result = arg.find(c)
            if not result == -1:
                if result == 0 or not arg[result - 1] == '\\':
                    raise exception.SSHInjectionThreat(command=cmd_list)


def create_channel(client, width, height):
    """Invoke an interactive shell session on server."""
    channel = client.invoke_shell()
    channel.resize_pty(width, height)
    return channel


def venusdir():
    import venus
    return os.path.abspath(venus.__file__).split('venus/__init__.py')[0]


def list_of_dicts_to_dict(seq, key):
    """Convert list of dicts to a indexted dict.

    Takes a list of dicts, and converts it a nested dict
    indexed by <key>

    :param seq: list of dicts
    :param key: key in dicts to index by

    example:
      lst = [{'id': 1, ...}, {'id': 2, ...}...]
      key = 'id'
      returns {1:{'id': 1, ...}, 2:{'id':2, ...}

    """
    return {d[key]: dict(d, index=d[key]) for (i, d) in enumerate(seq)}


class ProtectedExpatParser(expatreader.ExpatParser):
    """An expat parser which disables DTD's and entities by default."""

    def __init__(self, forbid_dtd=True, forbid_entities=True,
                 *args, **kwargs):
        # Python 2.x old style class
        expatreader.ExpatParser.__init__(self, *args, **kwargs)
        self.forbid_dtd = forbid_dtd
        self.forbid_entities = forbid_entities

    def start_doctype_decl(self, name, sysid, pubid, has_internal_subset):
        raise ValueError("Inline DTD forbidden")

    def entity_decl(self, entity_name, is_parameter_entity, value, base,
                    system_id, public_id, notation_name):
        raise ValueError("<!ENTITY> forbidden")

    def unparsed_entity_decl(self, name, base, sysid, pubid, notation_name):
        # expat 1.2
        raise ValueError("<!ENTITY> forbidden")

    def reset(self):
        expatreader.ExpatParser.reset(self)
        if self.forbid_dtd:
            self._parser.StartDoctypeDeclHandler = self.start_doctype_decl
        if self.forbid_entities:
            self._parser.EntityDeclHandler = self.entity_decl
            self._parser.UnparsedEntityDeclHandler = self.unparsed_entity_decl


def safe_minidom_parse_string(xml_string):
    """Parse an XML string using minidom safely.

    """
    try:
        return minidom.parseString(xml_string, parser=ProtectedExpatParser())
    except sax.SAXParseException:
        raise expat.ExpatError()


def xhtml_escape(value):
    """Escapes a string so it is valid within XML or XHTML."""
    return saxutils.escape(value, {'"': '&quot;', "'": '&apos;'})


def get_from_path(items, path):
    """Returns a list of items matching the specified path.

    Takes an XPath-like expression e.g. prop1/prop2/prop3, and for each item
    in items, looks up items[prop1][prop2][prop3]. Like XPath, if any of the
    intermediate results are lists it will treat each list item individually.
    A 'None' in items or any child expressions will be ignored, this function
    will not throw because of None (anywhere) in items.  The returned list
    will contain no None values.

    """
    if path is None:
        raise exception.Error('Invalid mini_xpath')

    (first_token, sep, remainder) = path.partition('/')

    if first_token == '':
        raise exception.Error('Invalid mini_xpath')

    results = []

    if items is None:
        return results

    if not isinstance(items, list):
        # Wrap single objects in a list
        items = [items]

    for item in items:
        if item is None:
            continue
        get_method = getattr(item, 'get', None)
        if get_method is None:
            continue
        child = get_method(first_token)
        if child is None:
            continue
        if isinstance(child, list):
            # Flatten intermediate lists
            for x in child:
                results.append(x)
        else:
            results.append(child)

    if not sep:
        # No more tokens
        return results
    else:
        return get_from_path(results, remainder)


def is_valid_boolstr(val):
    """Check if the provided string is a valid bool string or not."""
    val = str(val).lower()
    return (val == 'true' or val == 'false' or
            val == 'yes' or val == 'no' or
            val == 'y' or val == 'n' or
            val == '1' or val == '0')


def is_none_string(val):
    """Check if a string represents a None value."""
    if not isinstance(val, str):
        return False

    return val.lower() == 'none'


def monkey_patch():
    """Patches decorators for all functions in a specified module.

    If the CONF.monkey_patch set as True,
    this function patches a decorator
    for all functions in specified modules.

    You can set decorators for each modules
    using CONF.monkey_patch_modules.
    The format is "Module path:Decorator function".
    Example: 'venus.api.ec2.cloud:' \
     venus.openstack.common.notifier.api.notify_decorator'

    Parameters of the decorator is as follows.
    (See venus.openstack.common.notifier.api.notify_decorator)

    :param name: name of the function
    :param function: object of the function
    """
    # If CONF.monkey_patch is not True, this function do nothing.
    if not CONF.monkey_patch:
        return
    # Get list of modules and decorators
    for module_and_decorator in CONF.monkey_patch_modules:
        module, decorator_name = module_and_decorator.split(':')
        # import decorator function
        decorator = importutils.import_class(decorator_name)
        __import__(module)
        # Retrieve module information using pyclbr
        module_data = pyclbr.readmodule_ex(module)
        for key in module_data.keys():
            # set the decorator for the class methods
            if isinstance(module_data[key], pyclbr.Class):
                clz = importutils.import_class("%s.%s" % (module, key))
                for method, func in inspect.getmembers(clz, inspect.ismethod):
                    setattr(
                        clz, method,
                        decorator("%s.%s.%s" % (module, key, method), func))
            # set the decorator for the function
            if isinstance(module_data[key], pyclbr.Function):
                func = importutils.import_class("%s.%s" % (module, key))
                setattr(sys.modules[module], key,
                        decorator("%s.%s" % (module, key), func))


def make_dev_path(dev, partition=None, base='/dev'):
    """Return a path to a particular device.

    >>> make_dev_path('xvdc')
    /dev/xvdc

    >>> make_dev_path('xvdc', 1)
    /dev/xvdc1
    """
    path = os.path.join(base, dev)
    if partition:
        path += str(partition)
    return path


def sanitize_hostname(hostname):
    """Return a hostname which conforms to RFC-952 and RFC-1123 specs."""
    hostname = hostname.encode('latin-1', 'ignore')
    hostname = hostname.decode('latin-1')

    hostname = re.sub('[ _]', '-', hostname)
    hostname = re.sub('[^\\w.-]+', '', hostname)
    hostname = hostname.lower()
    hostname = hostname.strip('.-')

    return hostname


def hash_file(file_like_object):
    """Generate a hash for the contents of a file."""
    checksum = hashlib.sha1()
    any(map(checksum.update, iter(lambda: file_like_object.read(32768), b'')))
    return checksum.hexdigest()


def service_is_up(service):
    """Check whether a service is up based on last heartbeat."""
    last_heartbeat = service['updated_at'] or service['created_at']
    # Timestamps in DB are UTC.
    elapsed = (timeutils.utcnow(with_timezone=True) -
               last_heartbeat).total_seconds()
    return abs(elapsed) <= CONF.service_down_time


def read_file_as_root(file_path):
    """Secure helper to read file as root."""
    try:
        out, _err = execute('cat', file_path, run_as_root=True)
        return out
    except processutils.ProcessExecutionError:
        raise exception.FileNotFound(file_path=file_path)


@contextlib.contextmanager
def temporary_chown(path, owner_uid=None):
    """Temporarily chown a path.

    :params owner_uid: UID of temporary owner (defaults to current user)
    """
    if owner_uid is None:
        owner_uid = os.getuid()

    orig_uid = os.stat(path).st_uid

    if orig_uid != owner_uid:
        execute('chown', owner_uid, path, run_as_root=True)
    try:
        yield
    finally:
        if orig_uid != owner_uid:
            execute('chown', orig_uid, path, run_as_root=True)


@contextlib.contextmanager
def tempdir(**kwargs):
    tmpdir = tempfile.mkdtemp(**kwargs)
    try:
        yield tmpdir
    finally:
        try:
            shutil.rmtree(tmpdir)
        except OSError as e:
            LOG.debug('Could not remove tmpdir: %s', str(e))


def walk_class_hierarchy(clazz, encountered=None):
    """Walk class hierarchy, yielding most derived classes first."""
    if not encountered:
        encountered = []
    for subclass in clazz.__subclasses__():
        if subclass not in encountered:
            encountered.append(subclass)
            # drill down to leaves first
            for subsubclass in walk_class_hierarchy(subclass, encountered):
                yield subsubclass
            yield subclass


def get_root_helper():
    return 'sudo venus-rootwrap %s' % CONF.rootwrap_config


def get_file_mode(path):
    """This primarily exists to make unit testing easier."""
    return stat.S_IMODE(os.stat(path).st_mode)


def get_file_gid(path):
    """This primarily exists to make unit testing easier."""
    return os.stat(path).st_gid


def get_file_size(path):
    """Returns the file size."""
    return os.stat(path).st_size


def get_bool_param(param_string, params):
    param = params.get(param_string, False)
    if not is_valid_boolstr(param):
        msg = _('Value %(param)s for %(param_string)s is not a '
                'boolean.') % {'param': param, 'param_string': param_string}
        raise exception.InvalidParameterValue(err=msg)

    return strutils.bool_from_string(param, strict=True)


def check_string_length(value, name, min_length=0, max_length=None):
    """Check the length of specified string.

    :param value: the value of the string
    :param name: the name of the string
    :param min_length: the min_length of the string
    :param max_length: the max_length of the string
    """
    if not isinstance(value, str):
        msg = _("%s is not a string or unicode") % name
        raise exception.InvalidInput(message=msg)

    if len(value) < min_length:
        msg = _("%(name)s has a minimum character requirement of "
                "%(min_length)s.") % {'name': name, 'min_length': min_length}
        raise exception.InvalidInput(message=msg)

    if max_length and len(value) > max_length:
        msg = _("%(name)s has more than %(max_length)s "
                "characters.") % {'name': name, 'max_length': max_length}
        raise exception.InvalidInput(message=msg)


def remove_invalid_filter_options(context, filters,
                                  allowed_search_options):
    """Remove search options that are not valid for non-admin API/context."""

    if context.is_admin:
        # Allow all options
        return
    # Otherwise, strip out all unknown options
    unknown_options = [opt for opt in filters
                       if opt not in allowed_search_options]
    bad_options = ", ".join(unknown_options)
    LOG.debug("Removing options '%s' from query.", bad_options)
    for opt in unknown_options:
        del filters[opt]


def retry(exceptions, interval=1, retries=3, backoff_rate=2,
          wait_random=False):

    def _retry_on_exception(e):
        return isinstance(e, exceptions)

    def _backoff_sleep(previous_attempt_number, delay_since_first_attempt_ms):
        exp = backoff_rate ** previous_attempt_number
        wait_for = interval * exp

        if wait_random:
            random.seed()
            wait_val = random.randrange(interval * 1000.0, wait_for * 1000.0)
        else:
            wait_val = wait_for * 1000.0

        LOG.debug("Sleeping for %s seconds", (wait_val / 1000.0))

        return wait_val

    def _print_stop(previous_attempt_number, delay_since_first_attempt_ms):
        delay_since_first_attempt = delay_since_first_attempt_ms / 1000.0
        LOG.debug("Failed attempt %s", previous_attempt_number)
        LOG.debug("Have been at this for %s seconds",
                  delay_since_first_attempt)
        return previous_attempt_number == retries

    if retries < 1:
        raise ValueError('Retries must be greater than or '
                         'equal to 1 (received: %s). ' % retries)

    def _decorator(f):

        @functools.wraps(f)
        def _wrapper(*args, **kwargs):
            r = retrying.Retrying(retry_on_exception=_retry_on_exception,
                                  wait_func=_backoff_sleep,
                                  stop_func=_print_stop)
            return r.call(f, *args, **kwargs)

        return _wrapper

    return _decorator


def convert_str(text):
    """Convert to native string.

    Convert bytes and Unicode strings to native strings:

    * convert to bytes on Python 2:
      encode Unicode using encodeutils.safe_encode()
    * convert to Unicode on Python 3: decode bytes from UTF-8
    """
    if isinstance(text, bytes):
        return text.decode('utf-8')
    else:
        return text


def trace_method(f):
    """Decorates a function if TRACE_METHOD is true."""
    @functools.wraps(f)
    def trace_method_logging_wrapper(*args, **kwargs):
        if TRACE_METHOD:
            return trace(f)(*args, **kwargs)
        return f(*args, **kwargs)
    return trace_method_logging_wrapper


def trace_api(f):
    """Decorates a function if TRACE_API is true."""
    @functools.wraps(f)
    def trace_api_logging_wrapper(*args, **kwargs):
        if TRACE_API:
            return trace(f)(*args, **kwargs)
        return f(*args, **kwargs)
    return trace_api_logging_wrapper


def trace(f):
    """Trace calls to the decorated function.

    This decorator should always be defined as the outermost decorator so it
    is defined last. This is important so it does not interfere
    with other decorators.

    Using this decorator on a function will cause its execution to be logged at
    `DEBUG` level with arguments, return values, and exceptions.

    :returns a function decorator
    """

    func_name = f.__name__

    @functools.wraps(f)
    def trace_logging_wrapper(*args, **kwargs):
        if len(args) > 0:
            maybe_self = args[0]
        else:
            maybe_self = kwargs.get('self', None)

        if maybe_self and hasattr(maybe_self, '__module__'):
            logger = logging.getLogger(maybe_self.__module__)
        else:
            logger = LOG

        # NOTE(ameade): Don't bother going any further if DEBUG log level
        # is not enabled for the logger.
        if not logger.isEnabledFor(py_logging.DEBUG):
            return f(*args, **kwargs)

        all_args = inspect.getcallargs(f, *args, **kwargs)
        logger.debug('==> %(func)s: call %(all_args)r',
                     {'func': func_name, 'all_args': all_args})

        start_time = time.time() * 1000
        try:
            result = f(*args, **kwargs)
        except Exception as exc:
            total_time = int(round(time.time() * 1000)) - start_time
            logger.debug('<== %(func)s: exception (%(time)dms) %(exc)r',
                         {'func': func_name,
                          'time': total_time,
                          'exc': exc})
            raise
        total_time = int(round(time.time() * 1000)) - start_time

        logger.debug('<== %(func)s: return (%(time)dms) %(result)r',
                     {'func': func_name,
                      'time': total_time,
                      'result': result})
        return result
    return trace_logging_wrapper


class TraceWrapperMetaclass(type):
    """Metaclass that wraps all methods of a class with trace_method.

    This metaclass will cause every function inside of the class to be
    decorated with the trace_method decorator.

    To use the metaclass you define a class like so:
    class MyClass(object, metaclass=utils.TraceWrapperMetaclass):
    """
    def __new__(meta, classname, bases, class_dict):
        new_class_dict = {}
        for attributeName, attribute in class_dict.items():
            if isinstance(attribute, types.FunctionType):
                # replace it with a wrapped version
                attribute = functools.update_wrapper(trace_method(attribute),
                                                     attribute)
            new_class_dict[attributeName] = attribute

        return type.__new__(meta, classname, bases, new_class_dict)


class TraceWrapperWithABCMetaclass(abc.ABCMeta, TraceWrapperMetaclass):
    """Metaclass that wraps all methods of a class with trace."""
    pass


def setup_tracing(trace_flags):
    """Set global variables for each trace flag.

    Sets variables TRACE_METHOD and TRACE_API, which represent
    whether to log method and api traces.

    :param trace_flags: a list of strings
    """
    global TRACE_METHOD
    global TRACE_API
    try:
        trace_flags = [flag.strip() for flag in trace_flags]
    except TypeError:  # Handle when trace_flags is None or a test mock
        trace_flags = []
    for invalid_flag in (set(trace_flags) - VALID_TRACE_FLAGS):
        LOG.warning(_LW('Invalid trace flag: %s'), invalid_flag)
    TRACE_METHOD = 'method' in trace_flags
    TRACE_API = 'api' in trace_flags


def resolve_hostname(hostname):
    """Resolves host name to IP address.

    Resolves a host name (my.data.point.com) to an IP address (10.12.143.11).
    This routine also works if the data passed in hostname is already an IP.
    In this case, the same IP address will be returned.

    :param hostname:  Host name to resolve.
    :return:          IP Address for Host name.
    """
    result = socket.getaddrinfo(hostname, None)[0]
    (family, socktype, proto, canonname, sockaddr) = result
    LOG.debug('Asked to resolve hostname %(host)s and got IP %(ip)s.',
              {'host': hostname, 'ip': sockaddr[0]})
    return sockaddr[0]
