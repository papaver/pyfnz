#------------------------------------------------------------------------------
# test_try.py
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

import re
import unittest

from functools import partial

from pyz.tri import *

#------------------------------------------------------------------------------
# test classes
#------------------------------------------------------------------------------

class TryTest(unittest.TestCase):

    #--------------------------------------------------------------------------
    # tests
    #--------------------------------------------------------------------------

    def test_slots(self):
        """Test slots directive is correctly working.
        """

        failure = Try(lambda: 1 / 0)
        success = Try(lambda: 1 + 1)

        self.assertTrue(failure.is_failure)
        with self.assertRaises(AttributeError):
            failure.a = 1

        self.assertTrue(success.is_success)
        with self.assertRaises(AttributeError):
            success.a = 1

    #--------------------------------------------------------------------------

    def test_repr(self):
        """Test string representation.
        """

        failure = Try(lambda: 1 / 0)
        success = Try(lambda: 1 + 1)

        self.assertTrue(re.match("Failure\(.+\)", repr(failure)) is not None)
        self.assertEqual("Success(2)", repr(success))

    #--------------------------------------------------------------------------

    def test_do(self):
        """Test do notation.
        """

        failure  = Try(lambda: 1 / 0)
        success1 = Try(lambda: 1 + 1)
        success2 = Try(lambda: 2 * 2)

        failure_result = Try.do(f * s
                                for f in failure
                                for s in success1)

        success_result = Try.do(s1 * s2
                                for s1 in success1
                                for s2 in success2)

        self.assertEqual(0, failure_result | 0)
        self.assertEqual(8, success_result | 0)

    #--------------------------------------------------------------------------

    def test_is_failure(self):
        """Test checking if try is a failure.
        """

        failure = Try(lambda: 1 / 0)
        success = Try(lambda: 1 + 1)

        self.assertTrue(failure.is_failure())
        self.assertFalse(success.is_failure())

    #--------------------------------------------------------------------------

    def test_is_success(self):
        """Test checking if try is a success.
        """

        failure = Try(lambda: 1 / 0)
        success = Try(lambda: 1 + 1)

        self.assertTrue(success.is_success())
        self.assertFalse(failure.is_success())

    #--------------------------------------------------------------------------

    def test_foreach(self):
        """Test running a function with a side-effects on a success.
        """

        cache      = []
        cache_elem = lambda x: cache.append(x)

        failure = Try(lambda: 1 / 0)
        success = Try(lambda: 1 + 1)

        failure.foreach(cache_elem)
        success.foreach(cache_elem)

        self.assertEqual(1, len(cache))
        self.assertEqual(2, cache[0])

    #--------------------------------------------------------------------------

    def test_to_either(self):
        """Test converting to an either.
        """

        failure = Try(lambda: 1 / 0)
        success = Try(lambda: 1 + 1)

        failure_either = failure.to_either()
        success_either = success.to_either()

        self.assertTrue(failure_either.is_left())
        self.assertTrue(success_either.is_right())

    #--------------------------------------------------------------------------

    def test_get_success(self):
        """Test retrieving value contained in a successful Try.
        """

        success = Try(lambda: 1 + 1)
        failure = Try(lambda: 1 / 0)

        success_result = success.get()

        self.assertEqual(2, success_result)
        with self.assertRaises(ZeroDivisionError):
            failure.get()

    #--------------------------------------------------------------------------

    def test_get_or_else(self):
        """Test retrieving a value from a success else return default for
        failure.
        """

        failure = Try(lambda: 1 / 0)
        success = Try(lambda: 1 + 1)

        failure1_result = failure.get_or_else(0)
        success1_result = success.get_or_else(0)
        failure2_result = failure | 0
        success2_result = success | 0

        self.assertEqual(0, failure1_result)
        self.assertEqual(2, success1_result)
        self.assertEqual(0, failure2_result)
        self.assertEqual(2, success2_result)

    #--------------------------------------------------------------------------

    def test_or_else(self):
        """Test retrieving self or other either if failure.
        """

        default_4 = Try(lambda: 2 + 2)
        more_fail = Try(lambda: [][0])

        failure = Try(lambda: 1 / 0)
        success = Try(lambda: 1 + 1)

        failure1_result = failure.or_else(more_fail)
        success1_result = success.or_else(more_fail)
        failure2_result = failure.or_else(default_4)
        success2_result = success.or_else(default_4)

        self.assertEqual(0, failure1_result | 0)
        self.assertEqual(2, success1_result | 0)
        self.assertEqual(4, failure2_result | 0)
        self.assertEqual(2, success2_result | 0)

    #--------------------------------------------------------------------------

    def test_recover(self):
        """Test recovering from a failure.
        """

        default_9 = lambda e: 9 if isinstance(e, ZeroDivisionError) else None

        failure = Try(lambda: 1 / 0)
        success = Try(lambda: 1 + 1)

        failure_result = failure.recover(default_9)
        success_result = success.recover(default_9)

        self.assertEqual(9, failure_result | 0)
        self.assertEqual(2, success_result | 0)

    #--------------------------------------------------------------------------

    def test_recover_with(self):
        """Test recovering from a failure.
        """

        default_9 = lambda e: Try(lambda: 9 if isinstance(e, ZeroDivisionError) else None)
        more_fail = lambda e: Try(lambda: [][0])

        failure = Try(lambda: 1 / 0)
        success = Try(lambda: 1 + 1)

        failure1_result = failure.recover_with(default_9)
        success1_result = success.recover_with(default_9)
        failure2_result = failure.recover_with(more_fail)
        success2_result = success.recover_with(more_fail)

        self.assertEqual(9, failure1_result | 0)
        self.assertEqual(2, success1_result | 0)
        self.assertEqual(0, failure2_result | 0)
        self.assertEqual(2, success2_result | 0)

    #--------------------------------------------------------------------------

    def test_map(self):
        """Test running a function on a success.
        """

        plus_5 = lambda x: x + 5
        fail   = lambda x: x[0]

        failure = Try(lambda: 1 / 0)
        success = Try(lambda: 1 + 1)

        failure1_plus = failure.map(plus_5)
        success1_plus = success.map(plus_5)
        failure2_fail = failure.map(fail)
        success2_fail = success.map(fail)

        self.assertEqual(0, failure1_plus | 0)
        self.assertEqual(7, success1_plus | 0)
        self.assertEqual(0, failure2_fail | 0)
        self.assertEqual(0, success2_fail | 0)

    #--------------------------------------------------------------------------

    def test_pure(self):
        """Test turning a value into an Either.
        """

        success1 = Try.pure(4)
        success2 = Try.pure('a')

        self.assertEqual(4, success1 | 0)
        self.assertEqual('a', success2 | 'b')

    #--------------------------------------------------------------------------

    def test_flatmap(self):
        """Test binding through a success.
        """

        plus_5_maybe = lambda x: Try(lambda: x + 5)
        fail_maybe   = lambda x: Try(lambda: [][0])

        failure = Try(lambda: 1 / 0)
        success = Try(lambda: 1 + 1)

        failure1_result = failure.flatmap(plus_5_maybe)
        success1_result = success.flatmap(plus_5_maybe)
        failure2_result = failure.flatmap(fail_maybe)
        success2_result = success.flatmap(fail_maybe)

        self.assertEqual(0, failure1_result | 0)
        self.assertEqual(7, success1_result | 0)
        self.assertEqual(0, failure2_result | 0)
        self.assertEqual(0, success2_result | 0)

    #--------------------------------------------------------------------------

    def test_monad_laws(self):
        """Test the monad laws holds for Try.
        """

        sub2 = lambda b: Try(lambda: b - 2)
        div2 = lambda b: Try(lambda: b / 2)

        # left unit | (unit >>= a) == a
        self.assertEqual(Try.pure(6).flatmap(sub2), sub2(6))

        # right unit | (a >>= unit) == a
        self.assertEqual(sub2(6).flatmap(Try.pure), sub2(6))

        # associative | ((a >>= b) >>= c) == (a >>= (b >>= c))
        self.assertEqual(Try.pure(6).flatmap(lambda b: sub2(b).flatmap(div2)),
                         Try.pure(6).flatmap(sub2).flatmap(div2))
