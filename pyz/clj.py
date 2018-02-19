#------------------------------------------------------------------------------
# clj.py - pythonic implementations of core clojure functions
#------------------------------------------------------------------------------
# BSD 3-Clause License
#
# Copyright (c) 2018, Affirm
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# module
#------------------------------------------------------------------------------

__all__ = ['is_some',
           'is_empty',
           'first',
           'second',
           'ffirst',
           'last',
           'butlast',
           'nxt',
           'rest',
           'merge',
           'select_keys',
           'identity',
           'constantly']

#------------------------------------------------------------------------------
# functions
#------------------------------------------------------------------------------

def is_some(x):
    """Returns true if x is not None, false otherwise.
    """

    return x is not None

#------------------------------------------------------------------------------

def is_empty(coll):
    """Returns true if coll has no items.
    """

    return (coll is None) or (len(coll) == 0)

#------------------------------------------------------------------------------

def first(lst):
    """Returns the first item in the list. If lst is None, returns None.
    """

    if not is_empty(lst):
        return lst[0]

#------------------------------------------------------------------------------

def second(lst):
    """Same as first(nxt(lst)).
    """

    return first(nxt(lst))

#------------------------------------------------------------------------------

def ffirst(lst):
    """Same as first(first(lst)).
    """

    return first(first(lst))

#------------------------------------------------------------------------------

def last(lst):
    """Returns the last item in the list. If lst is None, returns None.
    """

    if not is_empty(lst):
        return lst[-1]

#------------------------------------------------------------------------------

def butlast(lst):
    """Return all but the last item in lst.
    """

    if lst is not None and len(lst) > 1:
        return lst[:-1]

#------------------------------------------------------------------------------

def nxt(lst):
    """Returns a seq of the items after the first. If there are no more items,
    returns None.
    """

    if lst is not None and len(lst) > 1:
        return lst[1:]

#------------------------------------------------------------------------------

def rest(lst):
    """Returns a possibly empty seq of the items after the first.
    """

    if lst is not None:
        return lst[1:]

#------------------------------------------------------------------------------

def merge(*args):
    """Returns a dict that consists of the rest of the dict updated onto the
    first.
    """

    ds = filter(lambda x: x is not None, args)
    if not is_empty(ds):
        a = {}
        for d in ds:
            a.update(d)
        return a

#------------------------------------------------------------------------------

def select_keys(dct, keys):
    """Returns a dict containing only those entries in dict whose key is in
    keys.
    """

    return dict(filter(lambda (k,v): k in keys, dct.iteritems()))

#------------------------------------------------------------------------------

def identity(x):
    """Returns its argument.
    """

    return x

#------------------------------------------------------------------------------

def constantly(x):
    """Returns a function that takes any number of arguments and returns x.
    """

    def fn(*args, **kwargs):
        return x
    return fn
