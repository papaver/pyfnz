#------------------------------------------------------------------------------
# tri.py - A pythonic implementation of a specialized disjunction
#------------------------------------------------------------------------------
# BSD 3-Clause License
#
# Copyright (c) 2018, Affirm
# Copyright (c) 2018, Moiz Merchant
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

import abc

from either import Left, Right

#------------------------------------------------------------------------------
# module
#------------------------------------------------------------------------------

__all__ = ['Try']

#------------------------------------------------------------------------------
# helper classes
#------------------------------------------------------------------------------

class TryIterExcept(Exception):
    """Thrown when attempting to iterate over a failure try.
    """

    def __init__(self, obj):
        self.obj = obj

#------------------------------------------------------------------------------
# Try (Monad / Functor)
#------------------------------------------------------------------------------

class Try(object):
    """Modeled after scala's Try.

    * summary from scala *
    The Try type represents a computation that may either result in an
    exception, or return a successfully computed value. It's similar to, but
    semantically different from the Either type.

    Always construct a Try using the Try constructor and not the Failure and
    Success classes.

    Note: This class is currently experimental and the implementation will
    change, but the interface will stay consistent.
    """

    #--------------------------------------------------------------------------
    # fields
    #--------------------------------------------------------------------------

    __metaclass__ = abc.ABCMeta
    __slots__     = ()

    #--------------------------------------------------------------------------
    # base
    #--------------------------------------------------------------------------

    def __new__(cls, f, *args, **kwargs):
        """Run f and wrap in Failure on exception otherwise in a Success.
        """

        try:
            value = f(*args, **kwargs)
            instance = object.__new__(Success)
            instance._value = value
        except Exception, e:
            instance = object.__new__(Failure)
            instance._value = e

        return instance

    #--------------------------------------------------------------------------

    def __init__(self, value, *args, **kwargs):
        """If class constructed from Try ignore the value passed in.
        """

        if not hasattr(self, '_value'):
            self._value = value

    #--------------------------------------------------------------------------

    def __or__(self, other):
        """Operator `|`.  Returns the value from this Success or the given
        default argument if this is a Failure.
        """

        return self.get_or_else(other)

    #--------------------------------------------------------------------------

    def __eq__(self, other):
        """Operator `==`.  Test both disjunctions are of the same type and
        hold the same value.
        """

        return type(self) is type(other) and self._value == other._value

    #--------------------------------------------------------------------------

    def __repr__(self):
        return "{cls}({value!r})".format(**{
            'cls' : self.__class__.__name__,
            'value' : self._value})

    #--------------------------------------------------------------------------

    def __iter__(self):
        """Yield successful value, throw exception if failure.
        """

        if type(self) is Failure:
            raise TryIterExcept(self)
        elif type(self) is Success:
            yield self._value

    #--------------------------------------------------------------------------
    # public methods
    #--------------------------------------------------------------------------

    @staticmethod
    def do(generator):
        """Similar to haskell's do notation.  Expects a generator which returns
        a single value.  The first failure encounted will be returned,
        otherwise values are extracted from the success using the for notation
        and passed through the generator comprehension.

        ex:
            >>> do([z] * z
                   for x in Try(lambda: 1)
                   for y in Try(lambda: 2 + x)
                   for z in Try(lambda: [y]))
            >>> Success([3 3 3])

            >>> do([z] * z
                   for x in Try(lambda: 1)
                   for y in Try(lambda: [x / 0])
                   for z in Try(lambda: y[1])
            >>> Failure(ZeroDivisionError('integer division or modulo by zero',)
        """

        try:
            return Success(next(generator))
        except TryIterExcept as e:
            return e.obj

    #--------------------------------------------------------------------------

    def is_failure(self):
        """Returns true if the Try is a Failure, false otherwise.
        """

        if type(self) is Failure:
            return True
        elif type(self) is Success:
            return False

    #--------------------------------------------------------------------------

    def is_success(self):
        """Returns true if the Try is a Success, false otherwise.
        """

        if type(self) is Failure:
            return False
        elif type(self) is Success:
            return True

    #--------------------------------------------------------------------------

    def foreach(self, g):
        """Applies the given function f if this is a Success, otherwise does
        nothing.
        """

        if type(self) is Success:
            g(self._value)

    #--------------------------------------------------------------------------

    def to_either(self):
        """Convert this Try into an Either. Failure becomes a Left and a
        Success a Right.
        """

        if type(self) is Failure:
            return Left(self._value)
        elif type(self) is Success:
            return Right(self._value)

    #--------------------------------------------------------------------------

    def get(self):
        """Returns the value from this Success or throws the exception if this
        is a Failure.
        """

        if type(self) is Failure:
            raise self._value
        elif type(self) is Success:
            return self._value

    #--------------------------------------------------------------------------

    def get_or_else(self, x):
        """Returns the value from this Success or the given default argument if
        this is a Failure.  Alias for `|`.
        """

        if type(self) is Failure:
            return x
        elif type(self) is Success:
            return self._value

    #--------------------------------------------------------------------------

    def or_else(self, x):
        """Returns this Try if it's a Success or the given default argument if
        this is a Failure.
        """

        if type(self) is Failure:
            return x
        elif type(self) is Success:
            return self

    #--------------------------------------------------------------------------

    def recover(self, f):
        """Applies the given function f if this is a Failure, otherwise returns
        this if this is a Success. Like map, f should return a value.
        """

        if type(self) is Failure:
            return Try(f, self._value)
        elif type(self) is Success:
            return self

    #--------------------------------------------------------------------------

    def recover_with(self, f):
        """Applies the given function f if this is a Failure, otherwise returns
        this if this is a Success. Like flatmap, f should return a Try.
        """

        if type(self) is Failure:
            return f(self._value)
        elif type(self) is Success:
            return self

    #- Functor ----------------------------------------------------------------

    def map(self, f):
        """Maps the given function to the value from this Success or returns
        this if this is a Failure.
        """

        if type(self) is Failure:
            return self
        elif type(self) is Success:
            return Try(f, self._value)

    #- Monad ------------------------------------------------------------------

    @staticmethod
    def pure(a):
        """Return 'a' wrapped in a success Try.
        """

        return Success(a)

    #--------------------------------------------------------------------------

    def flatmap(self, g):
        """Returns the given function applied to the value from this Success or
        returns this if this is a Failure.
        """

        if type(self) is Failure:
            return self
        elif type(self) is Success:
            return g(self._value)

#------------------------------------------------------------------------------

class Failure(Try):

    #--------------------------------------------------------------------------
    # fields
    #--------------------------------------------------------------------------

    __slots__ = ('_value',)

    #--------------------------------------------------------------------------
    # base
    #--------------------------------------------------------------------------

    def __new__(cls, *args, **kargs):
        """Normal initialization, don't inherit Try's implementation.
        """

        return object.__new__(Failure)

#------------------------------------------------------------------------------

class Success(Try):

    #--------------------------------------------------------------------------
    # fields
    #--------------------------------------------------------------------------

    __slots__ = ('_value',)

    #--------------------------------------------------------------------------
    # base
    #--------------------------------------------------------------------------

    def __new__(cls, *args, **kargs):
        """Normal initialization, don't inherit Try's implementation.
        """

        return object.__new__(Success)
