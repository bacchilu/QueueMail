#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
queuemail.py

QueueMail is a software architecture that let you send as many emails as you
need. But if you're sending emails too freequently, the system keeps them in a
buffer and sends them grouped in one single email, or fewer emails groups by
subject.

So using QueueMail only one mail every 2 minutes is sent. Not more frequently
than every 2 minutes.


Luca Bacchi <bacchilu@gmail.com> - http://www.lucabacchi.it
"""

import threading
import Queue


def sendMail(subject, msg):
    """
    Executes email send.
    """

    print '''Sending
%s
''' % msg


class Queue2(Queue.Queue):

    def __init__(self, maxsize=0):

        self.lock = threading.Lock()
        Queue.Queue.__init__(self, maxsize)

    def getAll(self):
        """
        Blocking method. It returns a list instead of a single value.

        It blocks until some values are in the queue. Then it return all the
        values in a single list.
        """

        with self.lock:
            ret = []
            m = self.get()
            ret.append(m)
            while True:
                try:
                    m = self.get(False)
                    ret.append(m)
                except Queue.Empty:
                    break
            return ret


class QueueMail(threading.Thread):

    t = None

    q = Queue2()
    e = threading.Event()

    @staticmethod
    def avvia():
        QueueMail.t = QueueMail()
        QueueMail.t.start()

    @staticmethod
    def stop():
        QueueMail.q.put(None)
        QueueMail.e.set()
        QueueMail.t.join()

    @staticmethod
    def send(subject, body):
        """
        Encode the message to be sent
        """

        QueueMail.q.put((subject, body))

    def getMessages(self):
        """
        Extract all pending messages from the queue.
        It encapsulates them in a data structure like this:
            {'subject1': ['msg1', 'msg2', '...'],
            'subject2': ['msg1', 'msg2', '...']}
        """

        msgList = QueueMail.q.getAll()

        ret = {}
        exit = False
        for msg in msgList:
            if msg is None:
                exit = True
                continue
            (subject, body) = msg
            ret[subject] = ret.get(subject, [])
            ret[subject].append(body)

        return (ret, exit)

    def run(self):
        """
        Get all messages, joins them and send.
        """

        while True:
            (msgList, exit) = self.getMessages()

            for (subject, messages) in msgList.items():
                if len(messages) > 0:
                    msg = ('\n' + '-' * 30 + '\n').join(messages)
                    sendMail(subject, msg)

            if exit:
                return

            QueueMail.e.wait(60.0 * 2)


if __name__ == '__main__':
    QueueMail.avvia()
    try:
        QueueMail.send(u'Ciao', u'Hello World! 1')
        QueueMail.send(u'Ciao', u'Hello World! 2')
        QueueMail.send(u'Ciao2', u'Hello World! 3')
    finally:
        QueueMail.stop()
