#!/usr/bin/env python
# coding=utf-8

class A(object):
    def __init__(self):
        print "A() init"

class B(A):
    def __init__(self):
#        A.__init__(self)
        super(B,self).__init__()
#        super().__init__()
        print "B() init"

b = B()

