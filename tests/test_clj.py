#------------------------------------------------------------------------------
# test_clj.py
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

from pyz.clj import *

#------------------------------------------------------------------------------
# test classes
#------------------------------------------------------------------------------

class CoreTest(unittest.TestCase):

    #--------------------------------------------------------------------------
    # tests
    #--------------------------------------------------------------------------

    def test_is_empty(self):
        """Test checking a collection for emptiness.
        """

        self.assertTrue(is_empty([]))
        self.assertTrue(is_empty({}))
        self.assertTrue(is_empty(set([])))
        self.assertFalse(is_empty([1]))
        self.assertFalse(is_empty({'a':1}))
        self.assertFalse(is_empty(set([1])))

    #--------------------------------------------------------------------------

    def test_first(self):
        """Test retrieving the first element in list.
        """

        self.assertEqual(None, first(None))
        self.assertEqual(None, first([]))
        self.assertEqual(1, first([1]))
        self.assertEqual(1, first([1, 2, 3]))

    #--------------------------------------------------------------------------

    def test_second(self):
        """Test retrieving the second element in list.
        """

        self.assertEqual(None, second(None))
        self.assertEqual(None, second([]))
        self.assertEqual(None, second([1]))
        self.assertEqual(2, second([1, 2, 3]))

    #--------------------------------------------------------------------------

    def test_ffirst(self):
        """Test retrieving the first element of the first element in list.
        """

        self.assertEqual(None, ffirst(None))
        self.assertEqual(None, ffirst([]))
        self.assertEqual(1, ffirst([[1]]))
        self.assertEqual(1, ffirst([[1, 2]]))
        self.assertEqual(1, ffirst([[1, 2], [3, 4]]))

    #--------------------------------------------------------------------------

    def test_last(self):
        """Test retrieving the last element in list.
        """

        self.assertEqual(None, last(None))
        self.assertEqual(None, last([]))
        self.assertEqual(1, last([1]))
        self.assertEqual(3, last([1, 2, 3]))

    #--------------------------------------------------------------------------

    def test_nxt(self):
        """Test retrieving the all elements after the first, None if zero
        elements.
        """

        self.assertEqual(None, nxt(None))
        self.assertEqual(None, nxt([]))
        self.assertEqual(None, nxt([1]))
        self.assertEqual([2, 3], nxt([1, 2, 3]))

    #--------------------------------------------------------------------------

    def test_rest(self):
        """Test retrieving the all elements after the first.
        """

        self.assertEqual(None, rest(None))
        self.assertEqual([], rest([]))
        self.assertEqual([], rest([1]))
        self.assertEqual([2, 3], rest([1, 2, 3]))

    #--------------------------------------------------------------------------

    def test_merge(self):
        """Test merging multiple dictionaries into one.
        """

        a = {'a':1}
        b = {'b':2}
        c = {'a':2, 'c':3}

        self.assertEqual(None, merge())
        self.assertEqual(None, merge(None))
        self.assertEqual({}, merge({}))
        self.assertEqual({}, merge({}, None))
        self.assertEqual({}, merge(None, {}))
        self.assertEqual({'a':1, 'b':2}, merge(a, b))
        self.assertEqual({'a':1, 'b':2}, merge(a, None, b))
        self.assertEqual({'a':2, 'b':2, 'c':3}, merge(a, c, b))

    #--------------------------------------------------------------------------

    def test_select_keys(self):
        """Test creating new dict with select keys from existing dict.
        """

        a = {'a':1}
        b = {'b':2, 'c':3}

        self.assertEqual({}, select_keys({}, []))
        self.assertEqual({}, select_keys({}, ['a']))
        self.assertEqual({}, select_keys(a, []))
        self.assertEqual(a, select_keys(a, ['a']))
        self.assertEqual({}, select_keys(b, ['a']))
        self.assertEqual(b, select_keys(b, ['a', 'b', 'c']))
        self.assertEqual(b, select_keys(b, ['b', 'c']))

    #--------------------------------------------------------------------------

    def test_identity(self):
        """Test identity function.
        """

        l = lambda: None

        self.assertEqual({}, identity({}))
        self.assertEqual([], identity([]))
        self.assertEqual(set([1]), identity(set([1])))
        self.assertEqual(1, identity(1))
        self.assertEqual(1.0, identity(1.0))
        self.assertEqual('a', identity('a'))
        self.assertEqual(l, identity(l))

    #--------------------------------------------------------------------------

    def test_constantly(self):
        """Test constantly returning input value.
        """

        lst = constantly([])
        num = constantly(1)
        lmb = constantly(lambda: 'a')

        self.assertEqual([], lst())
        self.assertEqual([], lst(1))
        self.assertEqual([], lst(1, x=2))
        self.assertEqual(1, num())
        self.assertEqual(1, num(1))
        self.assertEqual(1, num(1, x=2))
        self.assertEqual('a', lmb()())
        self.assertEqual('a', lmb(1)())
        self.assertEqual('a', lmb(1, x=2)())
