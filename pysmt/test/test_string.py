#
# This file is part of pySMT.
#
#   Copyright 2015 Andrea Micheli and Marco Gario
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
from pysmt.test import TestCase, skipIfNoSolverForLogic
from pysmt.shortcuts import (Not, Implies, Equals, Symbol, GE, GT, LT, And,
                             Int, Plus)
from pysmt.shortcuts import (String, StrConcat, StrLength, StrContains,
                             StrIndexOf, StrReplace, StrSubstr,
                             StrPrefixOf, StrSuffixOf, StrToInt, IntToStr,
                             StrToUint16, StrToUint32, StrCharAt)
from pysmt.typing import INT, STRING
from pysmt.logics import QF_SLIA


class TestString(TestCase):
    #MG: This test suit overlaps with examples.py
    #    we might want to include tests of more things like:
    #    - Simplifications at construction time
    #    - Simplifications by the simplifier
    #    - Infix notation
    #    - Constants and unicode support

    @skipIfNoSolverForLogic(QF_SLIA)
    def test_str_length(self):
        s1 = Symbol("s1", STRING)
        s2 = Symbol("s2", STRING)
        f = Not(Implies(Equals(s1, s2),
                        Equals(StrLength(s2), StrLength(s1))))
        self.assertUnsat(f)

    @skipIfNoSolverForLogic(QF_SLIA)
    def test_str_concat(self):
        s1 = Symbol("s1", STRING)
        s2 = Symbol("s2", STRING)
        f = Not(And(GE(StrLength(StrConcat(s1, s2)),
                       StrLength(s1)),
                    GE(StrLength(StrConcat(s1, s2)),
                       StrLength(s2))))
        self.assertUnsat(f)

    @skipIfNoSolverForLogic(QF_SLIA)
    def test_str_contains(self):
        s1 = Symbol("s1", STRING)
        s2 = Symbol("s2", STRING)
        f = Not(Implies(And(StrContains(s1, s2),
                            StrContains(s2, s1)),
                        Equals(s1, s2)))
        self.assertUnsat(f)

    @skipIfNoSolverForLogic(QF_SLIA)
    def test_str_indexof(self):
        s1 = String("Hello World")
        t1 = String("o")
        f = Not(Equals(StrIndexOf(s1, t1, Int(0)), Int(4)))
        self.assertUnsat(f)

    @skipIfNoSolverForLogic(QF_SLIA)
    def test_str_replace(self):
        s1 = Symbol("s1", STRING)
        s2 = Symbol("s2", STRING)
        s3 = Symbol("s3", STRING)
        f = And(GT(StrLength(s1), Int(0)),
                GT(StrLength(s2), Int(0)),
                GT(StrLength(s3), Int(0)),
                Not(StrContains(s1, s2)),
                Not(StrContains(s1, s3)),
                Not(Equals(StrReplace(StrReplace(s1, s2,s3), s3, s2), s1)))
        self.assertUnsat(f)

    @skipIfNoSolverForLogic(QF_SLIA)
    def test_str_substr(self):
        s1 = Symbol("s1", STRING)
        i = Symbol("index", INT)
        f = And(GT(i, Int(0)),
                GT(StrLength(s1), Int(1)),
                LT(i, StrLength(s1)),
                Equals(StrConcat(StrSubstr(s1, Int(0), i),
                                 StrSubstr(s1, Plus(i, Int(1)),
                                           StrLength(s1))),
                       s1))
        self.assertUnsat(f)

    @skipIfNoSolverForLogic(QF_SLIA)
    def test_str_prefixof(self):
        s1 = Symbol("s1", STRING)
        s2 = Symbol("s2", STRING)
        f = And(GT(StrLength(s1), Int(2)),
                GT(StrLength(s2), StrLength(s1)),
                And(StrPrefixOf(s2, s1), StrContains(s2, s1)))
        self.assertUnsat(f)

    @skipIfNoSolverForLogic(QF_SLIA)
    def test_str_suffixof(self):
        s1 = Symbol("s1",STRING)
        s2 = Symbol("s2",STRING)
        f = And(GT(StrLength(s1), Int(2)),
                GT(StrLength(s2), StrLength(s1)),
                And(StrSuffixOf(s2, s1), StrContains(s2, s1)))
        self.assertUnsat(f)

    @skipIfNoSolverForLogic(QF_SLIA)
    def test_str_to_int(self):
        s = String("1")
        f = Not(Equals(StrToInt(s), Int(1)))
        self.assertUnsat(f)

    @skipIfNoSolverForLogic(QF_SLIA)
    def test_int_to_str(self):
        s = String("1")
        f = Not(Equals((IntToStr(Int(1))), s))
        self.assertUnsat(f)

    @skipIfNoSolverForLogic(QF_SLIA)
    def test_str_to_unit16(self):
        s = String("1")
        f = Not(Equals(StrToUint16(s), Int(1)))
        self.assertUnsat(f)

    @skipIfNoSolverForLogic(QF_SLIA)
    def test_uint16_to_str(self):
        s = String("1")
        f = Not(Equals((IntToStr(Int(1))), s))
        self.assertUnsat(f)

    @skipIfNoSolverForLogic(QF_SLIA)
    def test_str_to_uint32(self):
        s = String("1")
        f = Not(Equals(StrToUint32(s), Int(1)))
        self.assertUnsat(f)

    @skipIfNoSolverForLogic(QF_SLIA)
    def test_uint32_to_str(self):
        s = String("1")
        f = Not(Equals((IntToStr(Int(1))), s))
        self.assertUnsat(f)

    @skipIfNoSolverForLogic(QF_SLIA)
    def test_str_charat(self):
        s1 = String("Hello")
        f =  Not(Equals(StrCharAt(s1, Int(0)), String("H")))
        self.assertUnsat(f)



if __name__ == "__main__":
    from pysmt.test import main
    main()
