"""
 Copyright (C) 2000, 2001, 2002, 2003 RiskMap srl

 This file is part of QuantLib, a free-software/open-source library
 for financial quantitative analysts and developers - http://quantlib.org/

 QuantLib is free software: you can redistribute it and/or modify it
 under the terms of the QuantLib license.  You should have received a
 copy of the license along with this program; if not, please email
 <quantlib-dev@lists.sf.net>. The license is also available online at
 <http://quantlib.org/license.shtml>.

 This program is distributed in the hope that it will be useful, but WITHOUT
 ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 FOR A PARTICULAR PURPOSE.  See the license for more details.
"""

import mxdevtool as ql
import unittest

flag = None


def raiseFlag():
    global flag
    flag = 1


class InstrumentTest(unittest.TestCase):
    def testObservable(self):
        "Testing observability of stocks"
        global flag
        flag = None
        me1 = ql.SimpleQuote(0.0)
        h = ql.RelinkableQuoteHandle(me1)
        s = ql.Stock(h)
        s.NPV()

        obs = ql.Observer(raiseFlag)
        obs.registerWith(s)

        me1.setValue(3.14)
        if not flag:
            self.fail("Observer was not notified of instrument change")

        s.NPV()
        flag = None
        me2 = ql.SimpleQuote(0.0)
        h.linkTo(me2)
        if not flag:
            self.fail("Observer was not notified of instrument change")

        s.NPV()
        flag = None
        s.freeze()
        me2.setValue(2.71)
        if flag:
            self.fail("Observer was notified of frozen instrument change")
        s.unfreeze()
        if not flag:
            self.fail("Observer was not notified of instrument change")


if __name__ == "__main__":
    print("testing QuantLib " + ql.__version__)
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(InstrumentTest, "test"))
    unittest.TextTestRunner(verbosity=2).run(suite)
