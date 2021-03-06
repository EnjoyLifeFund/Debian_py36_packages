# fancyopts.py - better command line parsing
#
#  Copyright 2005-2009 Matt Mackall <mpm@selenic.com> and others
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

from __future__ import absolute_import

import functools

from .i18n import _
from . import (
    error,
    pycompat,
)

# Set of flags to not apply boolean negation logic on
nevernegate = {
    # avoid --no-noninteractive
    'noninteractive',
    # These two flags are special because they cause hg to do one
    # thing and then exit, and so aren't suitable for use in things
    # like aliases anyway.
    'help',
    'version',
}

def _earlyoptarg(arg, shortlist, namelist):
    """Check if the given arg is a valid unabbreviated option

    Returns (flag_str, has_embedded_value?, embedded_value, takes_value?)

    >>> def opt(arg):
    ...     return _earlyoptarg(arg, b'R:q', [b'cwd=', b'debugger'])

    long form:

    >>> opt(b'--cwd')
    ('--cwd', False, '', True)
    >>> opt(b'--cwd=')
    ('--cwd', True, '', True)
    >>> opt(b'--cwd=foo')
    ('--cwd', True, 'foo', True)
    >>> opt(b'--debugger')
    ('--debugger', False, '', False)
    >>> opt(b'--debugger=')  # invalid but parsable
    ('--debugger', True, '', False)

    short form:

    >>> opt(b'-R')
    ('-R', False, '', True)
    >>> opt(b'-Rfoo')
    ('-R', True, 'foo', True)
    >>> opt(b'-q')
    ('-q', False, '', False)
    >>> opt(b'-qfoo')  # invalid but parsable
    ('-q', True, 'foo', False)

    unknown or invalid:

    >>> opt(b'--unknown')
    ('', False, '', False)
    >>> opt(b'-u')
    ('', False, '', False)
    >>> opt(b'-ufoo')
    ('', False, '', False)
    >>> opt(b'--')
    ('', False, '', False)
    >>> opt(b'-')
    ('', False, '', False)
    >>> opt(b'-:')
    ('', False, '', False)
    >>> opt(b'-:foo')
    ('', False, '', False)
    """
    if arg.startswith('--'):
        flag, eq, val = arg.partition('=')
        if flag[2:] in namelist:
            return flag, bool(eq), val, False
        if flag[2:] + '=' in namelist:
            return flag, bool(eq), val, True
    elif arg.startswith('-') and arg != '-' and not arg.startswith('-:'):
        flag, val = arg[:2], arg[2:]
        i = shortlist.find(flag[1:])
        if i >= 0:
            return flag, bool(val), val, shortlist.startswith(':', i + 1)
    return '', False, '', False

def earlygetopt(args, shortlist, namelist, gnu=False, keepsep=False):
    """Parse options like getopt, but ignores unknown options and abbreviated
    forms

    If gnu=False, this stops processing options as soon as a non/unknown-option
    argument is encountered. Otherwise, option and non-option arguments may be
    intermixed, and unknown-option arguments are taken as non-option.

    If keepsep=True, '--' won't be removed from the list of arguments left.
    This is useful for stripping early options from a full command arguments.

    >>> def get(args, gnu=False, keepsep=False):
    ...     return earlygetopt(args, b'R:q', [b'cwd=', b'debugger'],
    ...                        gnu=gnu, keepsep=keepsep)

    default parsing rules for early options:

    >>> get([b'x', b'--cwd', b'foo', b'-Rbar', b'-q', b'y'], gnu=True)
    ([('--cwd', 'foo'), ('-R', 'bar'), ('-q', '')], ['x', 'y'])
    >>> get([b'x', b'--cwd=foo', b'y', b'-R', b'bar', b'--debugger'], gnu=True)
    ([('--cwd', 'foo'), ('-R', 'bar'), ('--debugger', '')], ['x', 'y'])
    >>> get([b'--unknown', b'--cwd=foo', b'--', '--debugger'], gnu=True)
    ([('--cwd', 'foo')], ['--unknown', '--debugger'])

    restricted parsing rules (early options must come first):

    >>> get([b'--cwd', b'foo', b'-Rbar', b'x', b'-q', b'y'], gnu=False)
    ([('--cwd', 'foo'), ('-R', 'bar')], ['x', '-q', 'y'])
    >>> get([b'--cwd=foo', b'x', b'y', b'-R', b'bar', b'--debugger'], gnu=False)
    ([('--cwd', 'foo')], ['x', 'y', '-R', 'bar', '--debugger'])
    >>> get([b'--unknown', b'--cwd=foo', b'--', '--debugger'], gnu=False)
    ([], ['--unknown', '--cwd=foo', '--debugger'])

    stripping early options (without loosing '--'):

    >>> get([b'x', b'-Rbar', b'--', '--debugger'], gnu=True, keepsep=True)[1]
    ['x', '--', '--debugger']

    last argument:

    >>> get([b'--cwd'])
    ([], ['--cwd'])
    >>> get([b'--cwd=foo'])
    ([('--cwd', 'foo')], [])
    >>> get([b'-R'])
    ([], ['-R'])
    >>> get([b'-Rbar'])
    ([('-R', 'bar')], [])
    >>> get([b'-q'])
    ([('-q', '')], [])
    >>> get([b'-q', b'--'])
    ([('-q', '')], [])

    value passed to bool options:

    >>> get([b'--debugger=foo', b'x'])
    ([], ['--debugger=foo', 'x'])
    >>> get([b'-qfoo', b'x'])
    ([], ['-qfoo', 'x'])

    short option isn't separated with '=':

    >>> get([b'-R=bar'])
    ([('-R', '=bar')], [])

    ':' may be in shortlist, but shouldn't be taken as an option letter:

    >>> get([b'-:', b'y'])
    ([], ['-:', 'y'])

    '-' is a valid non-option argument:

    >>> get([b'-', b'y'])
    ([], ['-', 'y'])
    """
    # ignoring everything just after '--' isn't correct as '--' may be an
    # option value (e.g. ['-R', '--']), but we do that consistently.
    try:
        argcount = args.index('--')
    except ValueError:
        argcount = len(args)

    parsedopts = []
    parsedargs = []
    pos = 0
    while pos < argcount:
        arg = args[pos]
        flag, hasval, val, takeval = _earlyoptarg(arg, shortlist, namelist)
        if not hasval and takeval and pos + 1 >= argcount:
            # missing last argument
            break
        if not flag or hasval and not takeval:
            # non-option argument or -b/--bool=INVALID_VALUE
            if gnu:
                parsedargs.append(arg)
                pos += 1
            else:
                break
        elif hasval == takeval:
            # -b/--bool or -s/--str=VALUE
            parsedopts.append((flag, val))
            pos += 1
        else:
            # -s/--str VALUE
            parsedopts.append((flag, args[pos + 1]))
            pos += 2

    parsedargs.extend(args[pos:argcount])
    parsedargs.extend(args[argcount + (not keepsep):])
    return parsedopts, parsedargs

def gnugetopt(args, options, longoptions):
    """Parse options mostly like getopt.gnu_getopt.

    This is different from getopt.gnu_getopt in that an argument of - will
    become an argument of - instead of vanishing completely.
    """
    extraargs = []
    if '--' in args:
        stopindex = args.index('--')
        extraargs = args[stopindex + 1:]
        args = args[:stopindex]
    opts, parseargs = pycompat.getoptb(args, options, longoptions)
    args = []
    while parseargs:
        arg = parseargs.pop(0)
        if arg and arg[0:1] == '-' and len(arg) > 1:
            parseargs.insert(0, arg)
            topts, newparseargs = pycompat.getoptb(parseargs,\
                                            options, longoptions)
            opts = opts + topts
            parseargs = newparseargs
        else:
            args.append(arg)
    args.extend(extraargs)
    return opts, args


def fancyopts(args, options, state, gnu=False, early=False):
    """
    read args, parse options, and store options in state

    each option is a tuple of:

      short option or ''
      long option
      default value
      description
      option value label(optional)

    option types include:

      boolean or none - option sets variable in state to true
      string - parameter string is stored in state
      list - parameter string is added to a list
      integer - parameter strings is stored as int
      function - call function with parameter

    non-option args are returned
    """
    namelist = []
    shortlist = ''
    argmap = {}
    defmap = {}
    negations = {}
    alllong = set(o[1] for o in options)

    for option in options:
        if len(option) == 5:
            short, name, default, comment, dummy = option
        else:
            short, name, default, comment = option
        # convert opts to getopt format
        oname = name
        name = name.replace('-', '_')

        argmap['-' + short] = argmap['--' + oname] = name
        defmap[name] = default

        # copy defaults to state
        if isinstance(default, list):
            state[name] = default[:]
        elif callable(default):
            state[name] = None
        else:
            state[name] = default

        # does it take a parameter?
        if not (default is None or default is True or default is False):
            if short:
                short += ':'
            if oname:
                oname += '='
        elif oname not in nevernegate:
            if oname.startswith('no-'):
                insert = oname[3:]
            else:
                insert = 'no-' + oname
            # backout (as a practical example) has both --commit and
            # --no-commit options, so we don't want to allow the
            # negations of those flags.
            if insert not in alllong:
                assert ('--' + oname) not in negations
                negations['--' + insert] = '--' + oname
                namelist.append(insert)
        if short:
            shortlist += short
        if name:
            namelist.append(oname)

    # parse arguments
    if early:
        parse = functools.partial(earlygetopt, gnu=gnu)
    elif gnu:
        parse = gnugetopt
    else:
        parse = pycompat.getoptb
    opts, args = parse(args, shortlist, namelist)

    # transfer result to state
    for opt, val in opts:
        boolval = True
        negation = negations.get(opt, False)
        if negation:
            opt = negation
            boolval = False
        name = argmap[opt]
        obj = defmap[name]
        t = type(obj)
        if callable(obj):
            state[name] = defmap[name](val)
        elif t is type(1):
            try:
                state[name] = int(val)
            except ValueError:
                raise error.Abort(_('invalid value %r for option %s, '
                                   'expected int') % (val, opt))
        elif t is type(''):
            state[name] = val
        elif t is type([]):
            state[name].append(val)
        elif t is type(None) or t is type(False):
            state[name] = boolval

    # return unparsed args
    return args
