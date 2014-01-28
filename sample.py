#!/usr/bin/python
# -*- coding: utf-8 -*-

import executor_manager


def sendMail(subject, body):
    print 'Sending subject "%s" with body "%s"' % (subject, body)


def mergeEmails(emailList):
    """
    The email bodies are merged
    """

    assert len(emailList) > 0
    subject = emailList[0][0]
    bodies = [body for (_, body) in emailList]
    msg = ('\n' + '-' * 30 + '\n').join(bodies)
    return (subject, msg)


def getKey(email):
    """
    Returns the subject of the argument
    """

    (subject, _) = email
    return subject


executor_manager.ExecutorManager.avvia(sendMail, mergeEmails, getKey)
try:
    executor_manager.ExecutorManager.execute(('subject', 'body'))
finally:
    executor_manager.ExecutorManager.stop()
