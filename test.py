#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

import queuemail


def sendMail(subject, msg):
    """
    Mock of mail sender.
    """

    print '''=== Sending === 
%s
=============== 
''' % msg


class TestQueueMail(unittest.TestCase):

    def setUp(self):
        queuemail.QueueMail.avvia(sendMail)

    def test_1(self):
        queuemail.QueueMail.send(u'Ciao', u'Hello World! 1')
        queuemail.QueueMail.send(u'Ciao', u'Hello World! 2')
        queuemail.QueueMail.send(u'Ciao2', u'Hello World! 3')

    def tearDown(self):
        queuemail.QueueMail.stop()


if __name__ == '__main__':
    unittest.main()
