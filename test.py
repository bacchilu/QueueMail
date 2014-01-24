#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import time

import queuemail


class TestQueueMail(unittest.TestCase):

    def setUp(self):
        self.lastSend = u''

    def sendMail(self, subject, body):
        """
        Mock of mail sender.
        """

        self.lastSend = (subject, body)

    def test_1(self):
        queuemail.QueueMail.avvia(self.sendMail)

        queuemail.QueueMail.send(u's1', u'b1')
        time.sleep(1)
        self.assertEqual(self.lastSend, (u's1', u'b1'))

        queuemail.QueueMail.send(u's2', u'b2')
        queuemail.QueueMail.send(u's2', u'b3')
        time.sleep(1)
        self.assertEqual(self.lastSend, (u's1', u'b1'))

        queuemail.QueueMail.stop()
        self.assertEqual(self.lastSend, (u's2',
                         u'''b2
------------------------------
b3'''))

    def test_2(self):
        queuemail.QueueMail.avvia(self.sendMail)

        queuemail.QueueMail.send(u's1', u'b1')
        time.sleep(1)
        self.assertEqual(self.lastSend, (u's1', u'b1'))

        queuemail.QueueMail.send(u's2', u'b1')
        time.sleep(1)
        self.assertEqual(self.lastSend, (u's1', u'b1'))

        queuemail.QueueMail.stop()

    def tearDown(self):
        if queuemail.QueueMail.t.isAlive():
            queuemail.QueueMail.stop()


if __name__ == '__main__':
    unittest.main()
