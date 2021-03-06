# templatekw.py - common changeset template keywords
#
# Copyright 2005-2009 Matt Mackall <mpm@selenic.com>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

from __future__ import absolute_import

from .i18n import _
from .node import (
    hex,
    nullid,
)

from . import (
    encoding,
    error,
    hbisect,
    obsutil,
    patch,
    pycompat,
    registrar,
    scmutil,
    util,
)

class _hybrid(object):
    """Wrapper for list or dict to support legacy template

    This class allows us to handle both:
    - "{files}" (legacy command-line-specific list hack) and
    - "{files % '{file}\n'}" (hgweb-style with inlining and function support)
    and to access raw values:
    - "{ifcontains(file, files, ...)}", "{ifcontains(key, extras, ...)}"
    - "{get(extras, key)}"
    - "{files|json}"
    """

    def __init__(self, gen, values, makemap, joinfmt, keytype=None):
        if gen is not None:
            self.gen = gen  # generator or function returning generator
        self._values = values
        self._makemap = makemap
        self.joinfmt = joinfmt
        self.keytype = keytype  # hint for 'x in y' where type(x) is unresolved
    def gen(self):
        """Default generator to stringify this as {join(self, ' ')}"""
        for i, x in enumerate(self._values):
            if i > 0:
                yield ' '
            yield self.joinfmt(x)
    def itermaps(self):
        makemap = self._makemap
        for x in self._values:
            yield makemap(x)
    def __contains__(self, x):
        return x in self._values
    def __getitem__(self, key):
        return self._values[key]
    def __len__(self):
        return len(self._values)
    def __iter__(self):
        return iter(self._values)
    def __getattr__(self, name):
        if name not in ('get', 'items', 'iteritems', 'iterkeys', 'itervalues',
                        'keys', 'values'):
            raise AttributeError(name)
        return getattr(self._values, name)

class _mappable(object):
    """Wrapper for non-list/dict object to support map operation

    This class allows us to handle both:
    - "{manifest}"
    - "{manifest % '{rev}:{node}'}"
    - "{manifest.rev}"

    Unlike a _hybrid, this does not simulate the behavior of the underling
    value. Use unwrapvalue() or unwraphybrid() to obtain the inner object.
    """

    def __init__(self, gen, key, value, makemap):
        if gen is not None:
            self.gen = gen  # generator or function returning generator
        self._key = key
        self._value = value  # may be generator of strings
        self._makemap = makemap

    def gen(self):
        yield pycompat.bytestr(self._value)

    def tomap(self):
        return self._makemap(self._key)

    def itermaps(self):
        yield self.tomap()

def hybriddict(data, key='key', value='value', fmt='%s=%s', gen=None):
    """Wrap data to support both dict-like and string-like operations"""
    return _hybrid(gen, data, lambda k: {key: k, value: data[k]},
                   lambda k: fmt % (k, data[k]))

def hybridlist(data, name, fmt='%s', gen=None):
    """Wrap data to support both list-like and string-like operations"""
    return _hybrid(gen, data, lambda x: {name: x}, lambda x: fmt % x)

def unwraphybrid(thing):
    """Return an object which can be stringified possibly by using a legacy
    template"""
    gen = getattr(thing, 'gen', None)
    if gen is None:
        return thing
    if callable(gen):
        return gen()
    return gen

def unwrapvalue(thing):
    """Move the inner value object out of the wrapper"""
    if not util.safehasattr(thing, '_value'):
        return thing
    return thing._value

def wraphybridvalue(container, key, value):
    """Wrap an element of hybrid container to be mappable

    The key is passed to the makemap function of the given container, which
    should be an item generated by iter(container).
    """
    makemap = getattr(container, '_makemap', None)
    if makemap is None:
        return value
    if util.safehasattr(value, '_makemap'):
        # a nested hybrid list/dict, which has its own way of map operation
        return value
    return _mappable(None, key, value, makemap)

def showdict(name, data, mapping, plural=None, key='key', value='value',
             fmt='%s=%s', separator=' '):
    c = [{key: k, value: v} for k, v in data.iteritems()]
    f = _showlist(name, c, mapping, plural, separator)
    return hybriddict(data, key=key, value=value, fmt=fmt, gen=f)

def showlist(name, values, mapping, plural=None, element=None, separator=' '):
    if not element:
        element = name
    f = _showlist(name, values, mapping, plural, separator)
    return hybridlist(values, name=element, gen=f)

def _showlist(name, values, mapping, plural=None, separator=' '):
    '''expand set of values.
    name is name of key in template map.
    values is list of strings or dicts.
    plural is plural of name, if not simply name + 's'.
    separator is used to join values as a string

    expansion works like this, given name 'foo'.

    if values is empty, expand 'no_foos'.

    if 'foo' not in template map, return values as a string,
    joined by 'separator'.

    expand 'start_foos'.

    for each value, expand 'foo'. if 'last_foo' in template
    map, expand it instead of 'foo' for last key.

    expand 'end_foos'.
    '''
    templ = mapping['templ']
    strmapping = pycompat.strkwargs(mapping)
    if not plural:
        plural = name + 's'
    if not values:
        noname = 'no_' + plural
        if noname in templ:
            yield templ(noname, **strmapping)
        return
    if name not in templ:
        if isinstance(values[0], bytes):
            yield separator.join(values)
        else:
            for v in values:
                yield dict(v, **strmapping)
        return
    startname = 'start_' + plural
    if startname in templ:
        yield templ(startname, **strmapping)
    vmapping = mapping.copy()
    def one(v, tag=name):
        try:
            vmapping.update(v)
        except (AttributeError, ValueError):
            try:
                for a, b in v:
                    vmapping[a] = b
            except ValueError:
                vmapping[name] = v
        return templ(tag, **pycompat.strkwargs(vmapping))
    lastname = 'last_' + name
    if lastname in templ:
        last = values.pop()
    else:
        last = None
    for v in values:
        yield one(v)
    if last is not None:
        yield one(last, tag=lastname)
    endname = 'end_' + plural
    if endname in templ:
        yield templ(endname, **strmapping)

def getfiles(repo, ctx, revcache):
    if 'files' not in revcache:
        revcache['files'] = repo.status(ctx.p1(), ctx)[:3]
    return revcache['files']

def getlatesttags(repo, ctx, cache, pattern=None):
    '''return date, distance and name for the latest tag of rev'''

    cachename = 'latesttags'
    if pattern is not None:
        cachename += '-' + pattern
        match = util.stringmatcher(pattern)[2]
    else:
        match = util.always

    if cachename not in cache:
        # Cache mapping from rev to a tuple with tag date, tag
        # distance and tag name
        cache[cachename] = {-1: (0, 0, ['null'])}
    latesttags = cache[cachename]

    rev = ctx.rev()
    todo = [rev]
    while todo:
        rev = todo.pop()
        if rev in latesttags:
            continue
        ctx = repo[rev]
        tags = [t for t in ctx.tags()
                if (repo.tagtype(t) and repo.tagtype(t) != 'local'
                    and match(t))]
        if tags:
            latesttags[rev] = ctx.date()[0], 0, [t for t in sorted(tags)]
            continue
        try:
            ptags = [latesttags[p.rev()] for p in ctx.parents()]
            if len(ptags) > 1:
                if ptags[0][2] == ptags[1][2]:
                    # The tuples are laid out so the right one can be found by
                    # comparison in this case.
                    pdate, pdist, ptag = max(ptags)
                else:
                    def key(x):
                        changessincetag = len(repo.revs('only(%d, %s)',
                                                        ctx.rev(), x[2][0]))
                        # Smallest number of changes since tag wins. Date is
                        # used as tiebreaker.
                        return [-changessincetag, x[0]]
                    pdate, pdist, ptag = max(ptags, key=key)
            else:
                pdate, pdist, ptag = ptags[0]
        except KeyError:
            # Cache miss - recurse
            todo.append(rev)
            todo.extend(p.rev() for p in ctx.parents())
            continue
        latesttags[rev] = pdate, pdist + 1, ptag
    return latesttags[rev]

def getrenamedfn(repo, endrev=None):
    rcache = {}
    if endrev is None:
        endrev = len(repo)

    def getrenamed(fn, rev):
        '''looks up all renames for a file (up to endrev) the first
        time the file is given. It indexes on the changerev and only
        parses the manifest if linkrev != changerev.
        Returns rename info for fn at changerev rev.'''
        if fn not in rcache:
            rcache[fn] = {}
            fl = repo.file(fn)
            for i in fl:
                lr = fl.linkrev(i)
                renamed = fl.renamed(fl.node(i))
                rcache[fn][lr] = renamed
                if lr >= endrev:
                    break
        if rev in rcache[fn]:
            return rcache[fn][rev]

        # If linkrev != rev (i.e. rev not found in rcache) fallback to
        # filectx logic.
        try:
            return repo[rev][fn].renamed()
        except error.LookupError:
            return None

    return getrenamed

# default templates internally used for rendering of lists
defaulttempl = {
    'parent': '{rev}:{node|formatnode} ',
    'manifest': '{rev}:{node|formatnode}',
    'file_copy': '{name} ({source})',
    'envvar': '{key}={value}',
    'extra': '{key}={value|stringescape}'
}
# filecopy is preserved for compatibility reasons
defaulttempl['filecopy'] = defaulttempl['file_copy']

# keywords are callables like:
# fn(repo, ctx, templ, cache, revcache, **args)
# with:
# repo - current repository instance
# ctx - the changectx being displayed
# templ - the templater instance
# cache - a cache dictionary for the whole templater run
# revcache - a cache dictionary for the current revision
keywords = {}

templatekeyword = registrar.templatekeyword(keywords)

@templatekeyword('author')
def showauthor(repo, ctx, templ, **args):
    """String. The unmodified author of the changeset."""
    return ctx.user()

@templatekeyword('bisect')
def showbisect(repo, ctx, templ, **args):
    """String. The changeset bisection status."""
    return hbisect.label(repo, ctx.node())

@templatekeyword('branch')
def showbranch(**args):
    """String. The name of the branch on which the changeset was
    committed.
    """
    return args[r'ctx'].branch()

@templatekeyword('branches')
def showbranches(**args):
    """List of strings. The name of the branch on which the
    changeset was committed. Will be empty if the branch name was
    default. (DEPRECATED)
    """
    args = pycompat.byteskwargs(args)
    branch = args['ctx'].branch()
    if branch != 'default':
        return showlist('branch', [branch], args, plural='branches')
    return showlist('branch', [], args, plural='branches')

@templatekeyword('bookmarks')
def showbookmarks(**args):
    """List of strings. Any bookmarks associated with the
    changeset. Also sets 'active', the name of the active bookmark.
    """
    args = pycompat.byteskwargs(args)
    repo = args['ctx']._repo
    bookmarks = args['ctx'].bookmarks()
    active = repo._activebookmark
    makemap = lambda v: {'bookmark': v, 'active': active, 'current': active}
    f = _showlist('bookmark', bookmarks, args)
    return _hybrid(f, bookmarks, makemap, pycompat.identity)

@templatekeyword('children')
def showchildren(**args):
    """List of strings. The children of the changeset."""
    args = pycompat.byteskwargs(args)
    ctx = args['ctx']
    childrevs = ['%d:%s' % (cctx, cctx) for cctx in ctx.children()]
    return showlist('children', childrevs, args, element='child')

# Deprecated, but kept alive for help generation a purpose.
@templatekeyword('currentbookmark')
def showcurrentbookmark(**args):
    """String. The active bookmark, if it is associated with the changeset.
    (DEPRECATED)"""
    return showactivebookmark(**args)

@templatekeyword('activebookmark')
def showactivebookmark(**args):
    """String. The active bookmark, if it is associated with the changeset."""
    active = args[r'repo']._activebookmark
    if active and active in args[r'ctx'].bookmarks():
        return active
    return ''

@templatekeyword('date')
def showdate(repo, ctx, templ, **args):
    """Date information. The date when the changeset was committed."""
    return ctx.date()

@templatekeyword('desc')
def showdescription(repo, ctx, templ, **args):
    """String. The text of the changeset description."""
    s = ctx.description()
    if isinstance(s, encoding.localstr):
        # try hard to preserve utf-8 bytes
        return encoding.tolocal(encoding.fromlocal(s).strip())
    else:
        return s.strip()

@templatekeyword('diffstat')
def showdiffstat(repo, ctx, templ, **args):
    """String. Statistics of changes with the following format:
    "modified files: +added/-removed lines"
    """
    stats = patch.diffstatdata(util.iterlines(ctx.diff(noprefix=False)))
    maxname, maxtotal, adds, removes, binary = patch.diffstatsum(stats)
    return '%s: +%s/-%s' % (len(stats), adds, removes)

@templatekeyword('envvars')
def showenvvars(repo, **args):
    """A dictionary of environment variables. (EXPERIMENTAL)"""
    args = pycompat.byteskwargs(args)
    env = repo.ui.exportableenviron()
    env = util.sortdict((k, env[k]) for k in sorted(env))
    return showdict('envvar', env, args, plural='envvars')

@templatekeyword('extras')
def showextras(**args):
    """List of dicts with key, value entries of the 'extras'
    field of this changeset."""
    args = pycompat.byteskwargs(args)
    extras = args['ctx'].extra()
    extras = util.sortdict((k, extras[k]) for k in sorted(extras))
    makemap = lambda k: {'key': k, 'value': extras[k]}
    c = [makemap(k) for k in extras]
    f = _showlist('extra', c, args, plural='extras')
    return _hybrid(f, extras, makemap,
                   lambda k: '%s=%s' % (k, util.escapestr(extras[k])))

@templatekeyword('file_adds')
def showfileadds(**args):
    """List of strings. Files added by this changeset."""
    args = pycompat.byteskwargs(args)
    repo, ctx, revcache = args['repo'], args['ctx'], args['revcache']
    return showlist('file_add', getfiles(repo, ctx, revcache)[1], args,
                    element='file')

@templatekeyword('file_copies')
def showfilecopies(**args):
    """List of strings. Files copied in this changeset with
    their sources.
    """
    args = pycompat.byteskwargs(args)
    cache, ctx = args['cache'], args['ctx']
    copies = args['revcache'].get('copies')
    if copies is None:
        if 'getrenamed' not in cache:
            cache['getrenamed'] = getrenamedfn(args['repo'])
        copies = []
        getrenamed = cache['getrenamed']
        for fn in ctx.files():
            rename = getrenamed(fn, ctx.rev())
            if rename:
                copies.append((fn, rename[0]))

    copies = util.sortdict(copies)
    return showdict('file_copy', copies, args, plural='file_copies',
                    key='name', value='source', fmt='%s (%s)')

# showfilecopiesswitch() displays file copies only if copy records are
# provided before calling the templater, usually with a --copies
# command line switch.
@templatekeyword('file_copies_switch')
def showfilecopiesswitch(**args):
    """List of strings. Like "file_copies" but displayed
    only if the --copied switch is set.
    """
    args = pycompat.byteskwargs(args)
    copies = args['revcache'].get('copies') or []
    copies = util.sortdict(copies)
    return showdict('file_copy', copies, args, plural='file_copies',
                    key='name', value='source', fmt='%s (%s)')

@templatekeyword('file_dels')
def showfiledels(**args):
    """List of strings. Files removed by this changeset."""
    args = pycompat.byteskwargs(args)
    repo, ctx, revcache = args['repo'], args['ctx'], args['revcache']
    return showlist('file_del', getfiles(repo, ctx, revcache)[2], args,
                    element='file')

@templatekeyword('file_mods')
def showfilemods(**args):
    """List of strings. Files modified by this changeset."""
    args = pycompat.byteskwargs(args)
    repo, ctx, revcache = args['repo'], args['ctx'], args['revcache']
    return showlist('file_mod', getfiles(repo, ctx, revcache)[0], args,
                    element='file')

@templatekeyword('files')
def showfiles(**args):
    """List of strings. All files modified, added, or removed by this
    changeset.
    """
    args = pycompat.byteskwargs(args)
    return showlist('file', args['ctx'].files(), args)

@templatekeyword('graphnode')
def showgraphnode(repo, ctx, **args):
    """String. The character representing the changeset node in an ASCII
    revision graph."""
    wpnodes = repo.dirstate.parents()
    if wpnodes[1] == nullid:
        wpnodes = wpnodes[:1]
    if ctx.node() in wpnodes:
        return '@'
    elif ctx.obsolete():
        return 'x'
    elif ctx.closesbranch():
        return '_'
    else:
        return 'o'

@templatekeyword('graphwidth')
def showgraphwidth(repo, ctx, templ, **args):
    """Integer. The width of the graph drawn by 'log --graph' or zero."""
    # The value args['graphwidth'] will be this function, so we use an internal
    # name to pass the value through props into this function.
    return args.get('_graphwidth', 0)

@templatekeyword('index')
def showindex(**args):
    """Integer. The current iteration of the loop. (0 indexed)"""
    # just hosts documentation; should be overridden by template mapping
    raise error.Abort(_("can't use index in this context"))

@templatekeyword('latesttag')
def showlatesttag(**args):
    """List of strings. The global tags on the most recent globally
    tagged ancestor of this changeset.  If no such tags exist, the list
    consists of the single string "null".
    """
    return showlatesttags(None, **args)

def showlatesttags(pattern, **args):
    """helper method for the latesttag keyword and function"""
    args = pycompat.byteskwargs(args)
    repo, ctx = args['repo'], args['ctx']
    cache = args['cache']
    latesttags = getlatesttags(repo, ctx, cache, pattern)

    # latesttag[0] is an implementation detail for sorting csets on different
    # branches in a stable manner- it is the date the tagged cset was created,
    # not the date the tag was created.  Therefore it isn't made visible here.
    makemap = lambda v: {
        'changes': _showchangessincetag,
        'distance': latesttags[1],
        'latesttag': v,   # BC with {latesttag % '{latesttag}'}
        'tag': v
    }

    tags = latesttags[2]
    f = _showlist('latesttag', tags, args, separator=':')
    return _hybrid(f, tags, makemap, pycompat.identity)

@templatekeyword('latesttagdistance')
def showlatesttagdistance(repo, ctx, templ, cache, **args):
    """Integer. Longest path to the latest tag."""
    return getlatesttags(repo, ctx, cache)[1]

@templatekeyword('changessincelatesttag')
def showchangessincelatesttag(repo, ctx, templ, cache, **args):
    """Integer. All ancestors not in the latest tag."""
    latesttag = getlatesttags(repo, ctx, cache)[2][0]

    return _showchangessincetag(repo, ctx, tag=latesttag, **args)

def _showchangessincetag(repo, ctx, **args):
    offset = 0
    revs = [ctx.rev()]
    tag = args[r'tag']

    # The only() revset doesn't currently support wdir()
    if ctx.rev() is None:
        offset = 1
        revs = [p.rev() for p in ctx.parents()]

    return len(repo.revs('only(%ld, %s)', revs, tag)) + offset

@templatekeyword('manifest')
def showmanifest(**args):
    repo, ctx, templ = args[r'repo'], args[r'ctx'], args[r'templ']
    mnode = ctx.manifestnode()
    if mnode is None:
        # just avoid crash, we might want to use the 'ff...' hash in future
        return
    mrev = repo.manifestlog._revlog.rev(mnode)
    mhex = hex(mnode)
    args = args.copy()
    args.update({r'rev': mrev, r'node': mhex})
    f = templ('manifest', **args)
    # TODO: perhaps 'ctx' should be dropped from mapping because manifest
    # rev and node are completely different from changeset's.
    return _mappable(f, None, f, lambda x: {'rev': mrev, 'node': mhex})

@templatekeyword('obsfate')
def showobsfate(**args):
    # this function returns a list containing pre-formatted obsfate strings.
    #
    # This function will be replaced by templates fragments when we will have
    # the verbosity templatekw available.
    succsandmarkers = showsuccsandmarkers(**args)

    ui = args['ui']

    values = []

    for x in succsandmarkers:
        values.append(obsutil.obsfateprinter(x['successors'], x['markers'], ui))

    return showlist("fate", values, args)

def shownames(namespace, **args):
    """helper method to generate a template keyword for a namespace"""
    args = pycompat.byteskwargs(args)
    ctx = args['ctx']
    repo = ctx.repo()
    ns = repo.names[namespace]
    names = ns.names(repo, ctx.node())
    return showlist(ns.templatename, names, args, plural=namespace)

@templatekeyword('namespaces')
def shownamespaces(**args):
    """Dict of lists. Names attached to this changeset per
    namespace."""
    args = pycompat.byteskwargs(args)
    ctx = args['ctx']
    repo = ctx.repo()

    namespaces = util.sortdict()
    def makensmapfn(ns):
        # 'name' for iterating over namespaces, templatename for local reference
        return lambda v: {'name': v, ns.templatename: v}

    for k, ns in repo.names.iteritems():
        names = ns.names(repo, ctx.node())
        f = _showlist('name', names, args)
        namespaces[k] = _hybrid(f, names, makensmapfn(ns), pycompat.identity)

    f = _showlist('namespace', list(namespaces), args)

    def makemap(ns):
        return {
            'namespace': ns,
            'names': namespaces[ns],
            'builtin': repo.names[ns].builtin,
            'colorname': repo.names[ns].colorname,
        }

    return _hybrid(f, namespaces, makemap, pycompat.identity)

@templatekeyword('node')
def shownode(repo, ctx, templ, **args):
    """String. The changeset identification hash, as a 40 hexadecimal
    digit string.
    """
    return ctx.hex()

@templatekeyword('obsolete')
def showobsolete(repo, ctx, templ, **args):
    """String. Whether the changeset is obsolete. (EXPERIMENTAL)"""
    if ctx.obsolete():
        return 'obsolete'
    return ''

@templatekeyword('peerurls')
def showpeerurls(repo, **args):
    """A dictionary of repository locations defined in the [paths] section
    of your configuration file."""
    # see commands.paths() for naming of dictionary keys
    paths = repo.ui.paths
    urls = util.sortdict((k, p.rawloc) for k, p in sorted(paths.iteritems()))
    def makemap(k):
        p = paths[k]
        d = {'name': k, 'url': p.rawloc}
        d.update((o, v) for o, v in sorted(p.suboptions.iteritems()))
        return d
    return _hybrid(None, urls, makemap, lambda k: '%s=%s' % (k, urls[k]))

@templatekeyword("predecessors")
def showpredecessors(repo, ctx, **args):
    """Returns the list if the closest visible successors. (EXPERIMENTAL)"""
    predecessors = sorted(obsutil.closestpredecessors(repo, ctx.node()))
    predecessors = map(hex, predecessors)

    return _hybrid(None, predecessors,
                   lambda x: {'ctx': repo[x], 'revcache': {}},
                   lambda x: scmutil.formatchangeid(repo[x]))

@templatekeyword("successorssets")
def showsuccessorssets(repo, ctx, **args):
    """Returns a string of sets of successors for a changectx. Format used
    is: [ctx1, ctx2], [ctx3] if ctx has been splitted into ctx1 and ctx2
    while also diverged into ctx3. (EXPERIMENTAL)"""
    if not ctx.obsolete():
        return ''
    args = pycompat.byteskwargs(args)

    ssets = obsutil.successorssets(repo, ctx.node(), closest=True)
    ssets = [[hex(n) for n in ss] for ss in ssets]

    data = []
    for ss in ssets:
        h = _hybrid(None, ss, lambda x: {'ctx': repo[x], 'revcache': {}},
                    lambda x: scmutil.formatchangeid(repo[x]))
        data.append(h)

    # Format the successorssets
    def render(d):
        t = []
        for i in d.gen():
            t.append(i)
        return "".join(t)

    def gen(data):
        yield "; ".join(render(d) for d in data)

    return _hybrid(gen(data), data, lambda x: {'successorset': x},
                   pycompat.identity)

@templatekeyword("succsandmarkers")
def showsuccsandmarkers(repo, ctx, **args):
    """Returns a list of dict for each final successor of ctx. The dict
    contains successors node id in "successors" keys and the list of
    obs-markers from ctx to the set of successors in "markers".
    (EXPERIMENTAL)
    """

    values = obsutil.successorsandmarkers(repo, ctx)

    if values is None:
        values = []

    # Format successors and markers to avoid exposing binary to templates
    data = []
    for i in values:
        # Format successors
        successors = i['successors']

        successors = [hex(n) for n in successors]
        successors = _hybrid(None, successors,
                             lambda x: {'ctx': repo[x], 'revcache': {}},
                             lambda x: scmutil.formatchangeid(repo[x]))

        # Format markers
        finalmarkers = []
        for m in i['markers']:
            hexprec = hex(m[0])
            hexsucs = tuple(hex(n) for n in m[1])
            hexparents = None
            if m[5] is not None:
                hexparents = tuple(hex(n) for n in m[5])
            newmarker = (hexprec, hexsucs) + m[2:5] + (hexparents,) + m[6:]
            finalmarkers.append(newmarker)

        data.append({'successors': successors, 'markers': finalmarkers})

    f = _showlist('succsandmarkers', data, args)
    return _hybrid(f, data, lambda x: x, pycompat.identity)

@templatekeyword('p1rev')
def showp1rev(repo, ctx, templ, **args):
    """Integer. The repository-local revision number of the changeset's
    first parent, or -1 if the changeset has no parents."""
    return ctx.p1().rev()

@templatekeyword('p2rev')
def showp2rev(repo, ctx, templ, **args):
    """Integer. The repository-local revision number of the changeset's
    second parent, or -1 if the changeset has no second parent."""
    return ctx.p2().rev()

@templatekeyword('p1node')
def showp1node(repo, ctx, templ, **args):
    """String. The identification hash of the changeset's first parent,
    as a 40 digit hexadecimal string. If the changeset has no parents, all
    digits are 0."""
    return ctx.p1().hex()

@templatekeyword('p2node')
def showp2node(repo, ctx, templ, **args):
    """String. The identification hash of the changeset's second
    parent, as a 40 digit hexadecimal string. If the changeset has no second
    parent, all digits are 0."""
    return ctx.p2().hex()

@templatekeyword('parents')
def showparents(**args):
    """List of strings. The parents of the changeset in "rev:node"
    format. If the changeset has only one "natural" parent (the predecessor
    revision) nothing is shown."""
    args = pycompat.byteskwargs(args)
    repo = args['repo']
    ctx = args['ctx']
    pctxs = scmutil.meaningfulparents(repo, ctx)
    prevs = [p.rev() for p in pctxs]
    parents = [[('rev', p.rev()),
                ('node', p.hex()),
                ('phase', p.phasestr())]
               for p in pctxs]
    f = _showlist('parent', parents, args)
    return _hybrid(f, prevs, lambda x: {'ctx': repo[x], 'revcache': {}},
                   lambda x: scmutil.formatchangeid(repo[x]), keytype=int)

@templatekeyword('phase')
def showphase(repo, ctx, templ, **args):
    """String. The changeset phase name."""
    return ctx.phasestr()

@templatekeyword('phaseidx')
def showphaseidx(repo, ctx, templ, **args):
    """Integer. The changeset phase index."""
    return ctx.phase()

@templatekeyword('rev')
def showrev(repo, ctx, templ, **args):
    """Integer. The repository-local changeset revision number."""
    return scmutil.intrev(ctx)

def showrevslist(name, revs, **args):
    """helper to generate a list of revisions in which a mapped template will
    be evaluated"""
    args = pycompat.byteskwargs(args)
    repo = args['ctx'].repo()
    f = _showlist(name, ['%d' % r for r in revs], args)
    return _hybrid(f, revs,
                   lambda x: {name: x, 'ctx': repo[x], 'revcache': {}},
                   pycompat.identity, keytype=int)

@templatekeyword('subrepos')
def showsubrepos(**args):
    """List of strings. Updated subrepositories in the changeset."""
    args = pycompat.byteskwargs(args)
    ctx = args['ctx']
    substate = ctx.substate
    if not substate:
        return showlist('subrepo', [], args)
    psubstate = ctx.parents()[0].substate or {}
    subrepos = []
    for sub in substate:
        if sub not in psubstate or substate[sub] != psubstate[sub]:
            subrepos.append(sub) # modified or newly added in ctx
    for sub in psubstate:
        if sub not in substate:
            subrepos.append(sub) # removed in ctx
    return showlist('subrepo', sorted(subrepos), args)

# don't remove "showtags" definition, even though namespaces will put
# a helper function for "tags" keyword into "keywords" map automatically,
# because online help text is built without namespaces initialization
@templatekeyword('tags')
def showtags(**args):
    """List of strings. Any tags associated with the changeset."""
    return shownames('tags', **args)

def loadkeyword(ui, extname, registrarobj):
    """Load template keyword from specified registrarobj
    """
    for name, func in registrarobj._table.iteritems():
        keywords[name] = func

@templatekeyword('termwidth')
def showtermwidth(repo, ctx, templ, **args):
    """Integer. The width of the current terminal."""
    return repo.ui.termwidth()

@templatekeyword('troubles')
def showtroubles(repo, **args):
    """List of strings. Evolution troubles affecting the changeset.
    (DEPRECATED)
    """
    msg = ("'troubles' is deprecated, "
           "use 'instabilities'")
    repo.ui.deprecwarn(msg, '4.4')

    return showinstabilities(repo=repo, **args)

@templatekeyword('instabilities')
def showinstabilities(**args):
    """List of strings. Evolution instabilities affecting the changeset.
    (EXPERIMENTAL)
    """
    args = pycompat.byteskwargs(args)
    return showlist('instability', args['ctx'].instabilities(), args,
                    plural='instabilities')

# tell hggettext to extract docstrings from these functions:
i18nfunctions = keywords.values()
