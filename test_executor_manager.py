#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import time

import executor_manager


def sendMail(subject, body):
    """
    Mock of mail sender.
    """

    return (subject, body)


def separateEmails(argsList):
    """
    The email bodies are separate by lines
    """

    assert len(argsList) > 0
    subject = argsList[0][0]
    bodies = [body for (_, body) in argsList]
    msg = ('\n' + '-' * 30 + '\n').join(bodies)
    return (subject, msg)


def getKey(arg):
    """
    Returns the subject of the argument
    """

    (subject, _) = arg
    return subject


class TestExecutorManager(unittest.TestCase):

    def setUp(self):
        self.lastSend = u''

    def sendMail(self, subject, body):
        """
        Mock of mail sender.
        """

        self.lastSend = sendMail(subject, body)

    def test_1(self):
        executor_manager.ExecutorManager.avvia(self.sendMail,
                separateEmails, getKey)

        executor_manager.ExecutorManager.execute((u's1', u'b1'))
        time.sleep(1)
        self.assertEqual(self.lastSend, (u's1', u'b1'))

        executor_manager.ExecutorManager.execute((u's1', u'b2'))
        executor_manager.ExecutorManager.execute((u's1', u'b3'))
        time.sleep(1)
        self.assertEqual(self.lastSend, (u's1', u'b1'))

        executor_manager.ExecutorManager.stop()
        self.assertEqual(self.lastSend, (u's1',
                         u'''b2
------------------------------
b3'''))

    def test_2(self):
        executor_manager.ExecutorManager.avvia(self.sendMail,
                separateEmails, getKey)

        executor_manager.ExecutorManager.execute((u's1', u'b1'))
        time.sleep(1)
        self.assertEqual(self.lastSend, (u's1', u'b1'))

        executor_manager.ExecutorManager.execute((u's2', u'b1'))
        time.sleep(1)
        executor_manager.ExecutorManager.execute((u's2', u'b2'))
        time.sleep(1)
        self.assertEqual(self.lastSend, (u's2', u'b1'))

        executor_manager.ExecutorManager.stop()
        self.assertEqual(self.lastSend, (u's2', u'b2'))

    def test_3(self):
        executor_manager.ExecutorManager.avvia(self.sendMail,
                separateEmails, getKey)
        executor_manager.ExecutorManager.stop()
        self.assertEqual(self.lastSend, u'')

    def test_4(self):
        executor_manager.ExecutorManager.avvia(self.sendMail,
                separateEmails)

        executor_manager.ExecutorManager.execute((u's1', u'b1'))
        time.sleep(1)
        self.assertEqual(self.lastSend, (u's1', u'b1'))

        executor_manager.ExecutorManager.execute((u's2', u'b1'))
        time.sleep(1)
        executor_manager.ExecutorManager.execute((u's2', u'b2'))
        time.sleep(1)
        self.assertEqual(self.lastSend, (u's1', u'b1'))

        executor_manager.ExecutorManager.stop()
        self.assertEqual(self.lastSend, (u's2',
                         u'''b1
------------------------------
b2'''))

    def tearDown(self):
        if executor_manager.ExecutorManager.t.isAlive():
            executor_manager.ExecutorManager.stop()


if __name__ == '__main__':
    unittest.main()
