#------------------------------------------------------------------------------
# either.py - A pythonic implementation of a disjunction
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

import abc

from functools import partial

#------------------------------------------------------------------------------
# module
#------------------------------------------------------------------------------

__all__ = ['Either',
           'Left',
           'Right']

#------------------------------------------------------------------------------
# helper classes
#------------------------------------------------------------------------------

class EitherIterExcept(Exception):
    """Thrown when attempting to iterate over a left either.
    """

    def __init__(self, obj):
        self.obj = obj

#------------------------------------------------------------------------------
# Either (Monad / Functor / Applicative)
#------------------------------------------------------------------------------

class Either(object):
    """Modeled after scalaz's right-biased implementation.

    * summary from scalaz *
    Represents a disjunction: a result that is either an `A` or a `B`.
    A common use of a disjunction is to explicitly represent the possibility of
    failure in a result as opposed to throwing an exception. By convention, the
    left is used for errors and the right is reserved for successes. For
    example, a function that attempts to parse an integer from a string may
    have a return type of `Left(NumberFormatException)` | `Right(Int)`.
    However, since there is no need to actually throw an exception, the type
    (`A`) chosen for the "left" could be any type representing an error and has
    no need to actually extend `Exception`.

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

    def __init__(self, value):
        self._value = value

    #--------------------------------------------------------------------------

    def __invert__(self):
        """Unary operator `~`. Flip the left/right values in this disjunction.
        Alias for `swap`.
        """

        return self.swap()

    #--------------------------------------------------------------------------

    def __or__(self, other):
        """Operator `|`. Return the right value of this disjunction or the
        given default if left.  Alias for `get_or_else`.
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
        """Yield right disjunction's value, throw exception if left
        disjunction.
        """

        if type(self) is Left:
            raise EitherIterExcept(self)
        elif type(self) is Right:
            yield self._value

    #--------------------------------------------------------------------------
    # public methods
    #--------------------------------------------------------------------------

    @staticmethod
    def do(generator):
        """Similar to haskell's do notation.  Expects a generator which returns
        a single value.  The first left disjunction encounted will be returned,
        otherwise values are extracted from the right disjunction using the for
        notation and passed through the generator comprehension.

        ex:
            >>> do(mul2(z)
                   for x in Right(1)
                   for y in Right(2)
                   for z in add(x, y))
            >>> Right(6)

            >>> do(mul2(z)
                   for x in Left(1)
                   for y in Left(2)
                   for z in add(x, y))
            >>> Left(1)
        """

        try:
            return Right(next(generator))
        except EitherIterExcept as e:
            return e.obj

    #--------------------------------------------------------------------------

    def is_left(self):
        """Return `true` if this disjunction is left.
        """

        if type(self) is Left:
            return True
        elif type(self) is Right:
            return False

    #--------------------------------------------------------------------------

    def is_right(self):
        """Return `true` if this disjunction is right.
        """

        if type(self) is Left:
            return False
        elif type(self) is Right:
            return True

    #--------------------------------------------------------------------------

    def swap(self):
        """Flip the left/right values in this disjunction. Alias for unary `~`.
        """

        if type(self) is Left:
            return Right(self._value)
        elif type(self) is Right:
            return Left(self._value)

    #--------------------------------------------------------------------------

    def left_map(self, f):
        """Run the given function on the left value.
        """

        if type(self) is Left:
            return Left(f(self._value))
        elif type(self) is Right:
            return self

    #--------------------------------------------------------------------------

    def foreach(self, g):
        """Run the side-effect on the right of this disjunction.
        """

        if type(self) is Right:
            g(self._value)

    #--------------------------------------------------------------------------

    def exists(self, p):
        """Return `true` if this disjunction is a right value satisfying the
        given predicate.
        """

        if type(self) is Left:
            return False
        elif type(self) is Right:
            return p(self._value)

    #--------------------------------------------------------------------------

    def forall(self, p):
        """Return `true` if this disjunction is a left value or the right value
        satisfies the given predicate.
        """

        if type(self) is Left:
            return True
        elif type(self) is Right:
            return p(self._value)

    #--------------------------------------------------------------------------

    def to_list(self):
        """Return an empty list or list with one element on the right of this
        disjunction.
        """

        if type(self) is Left:
            return []
        elif type(self) is Right:
            return [self._value]

    #--------------------------------------------------------------------------

    def to_try(self):
        """Return a Success if right otherwise return error wrapped in Failure.
        Error should be an exception.
        """

        # prevent circular imports
        from .tri import Failure, Success

        if type(self) is Left:
            return Failure(self._value)
        elif type(self) is Right:
            return Success(self._value)

    #--------------------------------------------------------------------------

    def get_or_else(self, x):
        """Return the right value of this disjunction or the given default if
        left.  Alias for `|`.
        """

        if type(self) is Left:
            return x
        elif type(self) is Right:
            return self._value

    #--------------------------------------------------------------------------

    def or_else(self, x):
        """Return this if it is a right, otherwise, return the given value.
        """

        if type(self) is Left:
            return x
        elif type(self) is Right:
            return self

    #--------------------------------------------------------------------------

    def or_elsef(self, f):
        """Return this if it is a right, otherwise, return the result of
        running f.
        """

        if type(self) is Left:
            return f()
        elif type(self) is Right:
            return self

    #- Functor ----------------------------------------------------------------

    def map(self, f):
        """Map on the right of this disjunction.
        """

        if type(self) is Left:
            return self
        elif type(self) is Right:
            return Right(f(self._value))

    #- Applicative ------------------------------------------------------------

    def ap(self, f):
        """Apply a function in the environment of the right of this disjunction.
        """

        return f.flatmap(lambda ff: self.map(ff))

    #--------------------------------------------------------------------------

    def ap_partial(self, f):
        """Apply a function partially in the environment of the right of this
        disjunction.  Since currying in python is a nightmare, support for
        partials should alleviate a little pain.
        """

        return f.flatmap(lambda ff: self.map(lambda x: partial(ff, x)))

    #- Monad ------------------------------------------------------------------

    @staticmethod
    def pure(a):
        """Return 'a' wrapped in a right Either.
        """

        return Right(a)

    #--------------------------------------------------------------------------

    def flatmap(self, g):
        """Bind through the right of this disjunction.
        """

        if type(self) is Left:
            return self
        elif type(self) is Right:
            return g(self._value)

#------------------------------------------------------------------------------

class Left(Either):
    __slots__ = ('_value',)

#------------------------------------------------------------------------------

class Right(Either):
    __slots__ = ('_value',)
