#------------------------------------------------------------------------------
# test_either.py
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

import unittest

from pyfnz.either import *

#------------------------------------------------------------------------------
# test classes
#------------------------------------------------------------------------------

class EitherTest(unittest.TestCase):

    #--------------------------------------------------------------------------
    # tests
    #--------------------------------------------------------------------------

    def test_slots(self):
        """Test slots directive is correctly working.
        """

        left  = Left(1)
        right = Right(1)

        with self.assertRaises(AttributeError):
            left.a = 1

        with self.assertRaises(AttributeError):
            right.a = 1

    #--------------------------------------------------------------------------


    def test_repr(self):
        """Test string representation.
        """

        left  = Left(1)
        right = Right(1)

        self.assertEqual("Left(1)", repr(left))
        self.assertEqual("Right(1)", repr(right))

    #--------------------------------------------------------------------------

    def test_do(self):
        """Test do notation.
        """

        left   = Left(1)
        right1 = Right(2)
        right2 = Right(4)

        left_result = Either.do(l * r
                                for l in left
                                for r in right)

        right_result = Either.do(r1 * r2
                                 for r1 in right1
                                 for r2 in right2)

        self.assertEqual(1, ~left_result | 0)
        self.assertEqual(8, right_result | 0)

    #--------------------------------------------------------------------------

    def test_is_left(self):
        """Test checking if an either is a left.
        """

        left  = Left(1)
        right = Right(1)

        self.assertTrue(left.is_left())
        self.assertFalse(right.is_left())

    #--------------------------------------------------------------------------

    def test_is_right(self):
        """Test checking if an either is a right.
        """

        left  = Left(1)
        right = Right(1)

        self.assertTrue(right.is_right())
        self.assertFalse(left.is_right())

    #--------------------------------------------------------------------------


    def test_swap(self):
        """Test swapping an either from left to right and right to left.
        """

        left  = Left(1)
        right = Right(1)

        left1_swapped  = left.swap()
        right1_swapped = right.swap()
        left2_swapped  = ~left
        right2_swapped = ~right

        self.assertTrue(left1_swapped.is_right())
        self.assertTrue(right1_swapped.is_left())
        self.assertTrue(left2_swapped.is_right())
        self.assertTrue(right2_swapped.is_left())

    #--------------------------------------------------------------------------

    def test_left_map(self):
        """Test running a function on a left.
        """

        plus_5 = lambda x: x + 5

        left  = Left(1)
        right = Right(9)

        left_plus  = left.left_map(plus_5)
        right_plus = right.left_map(plus_5)

        self.assertEqual(6, ~left_plus | 0)
        self.assertEqual(9, right_plus | 0)

    #--------------------------------------------------------------------------

    def test_foreach(self):
        """Test running a function with a side-effects on a right.
        """

        cache      = []
        cache_elem = lambda x: cache.append(x)

        left  = Left(1)
        right = Right(9)

        left.foreach(cache_elem)
        right.foreach(cache_elem)

        self.assertEqual(1, len(cache))
        self.assertEqual(9, cache[0])

    #--------------------------------------------------------------------------

    def test_exists(self):
        """Test running a predicate on a right.
        """

        predicate = lambda x: x == 9

        left   = Left(1)
        right1 = Right(9)
        right2 = Right(5)

        left_result   = left.exists(predicate)
        right1_result = right1.exists(predicate)
        right2_result = right2.exists(predicate)

        self.assertFalse(left_result)
        self.assertTrue(right1_result)
        self.assertFalse(right2_result)

    #--------------------------------------------------------------------------

    def test_forall(self):
        """Test running a predicate on a right.
        """

        predicate = lambda x: x == 9

        left   = Left(1)
        right1 = Right(9)
        right2 = Right(5)

        left_result   = left.forall(predicate)
        right1_result = right1.forall(predicate)
        right2_result = right2.forall(predicate)

        self.assertTrue(left_result)
        self.assertTrue(right1_result)
        self.assertFalse(right2_result)

    #--------------------------------------------------------------------------

    def test_to_list(self):
        """Test converting to list.
        """

        left  = Left(1)
        right = Right(9)

        left_result  = left.to_list()
        right_result = right.to_list()

        self.assertEqual([], left_result)
        self.assertEqual([9], right_result)

    #--------------------------------------------------------------------------

    def test_to_try(self):
        """Test converting to try.
        """

        left  = Left(Exception("fail"))
        right = Right(9)

        left_result  = left.to_try()
        right_result = right.to_try()

        self.assertEqual(9, right_result.get())
        with self.assertRaises(Exception):
            left_result.get()

    #--------------------------------------------------------------------------

    def test_get_or_else(self):
        """Test retrieving a value from the right else return default for left.
        """

        left  = Left(1)
        right = Right(9)

        left1_result  = left.get_or_else(0)
        right1_result = right.get_or_else(0)
        left2_result  = left | 0
        right2_result = right | 0

        self.assertEqual(0, left1_result)
        self.assertEqual(9, right1_result)
        self.assertEqual(0, left2_result)
        self.assertEqual(9, right2_result)

    #--------------------------------------------------------------------------

    def test_or_else(self):
        """Test retrieving self or other either if left.
        """

        left  = Left(1)
        right = Right(9)

        left_result  = left.or_else(Right(2))
        right_result = right.or_else(Right(2))

        self.assertEqual(2, left_result | 0)
        self.assertEqual(9, right_result | 0)

    #--------------------------------------------------------------------------

    def test_or_elsef(self):
        """Test retrieving self or run f returning an either if left.
        """

        other_f = lambda: Right(5)

        left  = Left(1)
        right = Right(9)

        left_result  = left.or_elsef(other_f)
        right_result = right.or_elsef(other_f)

        self.assertEqual(5, left_result | 0)
        self.assertEqual(9, right_result | 0)

    #--------------------------------------------------------------------------

    def test_map(self):
        """Test running a function on a right.
        """

        plus_5 = lambda x: x + 5

        left  = Left(1)
        right = Right(9)

        left_plus  = left.map(plus_5)
        right_plus = right.map(plus_5)

        self.assertEqual(1, ~left_plus | 0)
        self.assertEqual(14, right_plus | 0)

    #--------------------------------------------------------------------------

    def test_ap(self):
        """Test applying a function on a right.
        """

        left    = Left(1)
        right   = Right(9)
        right_f = Right(lambda x: x + 5)

        left_result  = left.ap(right_f)
        right_result = right.ap(right_f)

        self.assertEqual(1, ~left_result | 0)
        self.assertEqual(14, right_result | 0)

    #--------------------------------------------------------------------------

    def test_ap_partial(self):
        """Test partially applying a function on a right.
        """

        left    = Left(1)
        right   = Right(9)
        right_f = Right(lambda x: x + 5)

        left_result  = left.ap_partial(right_f)
        right_result = right.ap_partial(right_f)

        self.assertEqual(1, ~left_result | 0)
        self.assertEqual(14, (right_result | 0)())

    #--------------------------------------------------------------------------

    def test_pure(self):
        """Test turning a value into an Either.
        """

        right1 = Either.pure(4)
        right2 = Either.pure('a')

        self.assertEqual(4, right1 | 0)
        self.assertEqual('a', right2 | 'b')

    #--------------------------------------------------------------------------

    def test_flatmap(self):
        """Test binding through a right.
        """

        plus_5_maybe = lambda x: Right(x + 5) if x == 9 else Left(7)

        left   = Left(1)
        right1 = Right(9)
        right2 = Right(3)

        left_result   = left.flatmap(plus_5_maybe)
        right1_result = right1.flatmap(plus_5_maybe)
        right2_result = right2.flatmap(plus_5_maybe)

        self.assertEqual(1, ~left_result | 0)
        self.assertEqual(14, right1_result | 0)
        self.assertEqual(7, ~right2_result | 0)

    #--------------------------------------------------------------------------

    def test_monad_laws(self):
        """Test the monad laws holds for Either.
        """

        sub2 = lambda b: Right(b - 2)
        div2 = lambda b: Right(b / 2)

        # left unit | (unit >>= a) == a
        self.assertEqual(Either.pure(6).flatmap(sub2), sub2(6))

        # right unit | (a >>= unit) == a
        self.assertEqual(sub2(6).flatmap(Either.pure), sub2(6))

        # associative | ((a >>= b) >>= c) == (a >>= (b >>= c))
        self.assertEqual(Either.pure(6).flatmap(lambda b: sub2(b).flatmap(div2)),
                         Either.pure(6).flatmap(sub2).flatmap(div2))
