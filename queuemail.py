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


class Queue(object):

    def __init__(self):
        self.cond = threading.Condition()
        self.items = []

    def put(self, item):
        with self.cond:
            self.items.append(item)
            self.cond.notify()

    def getAll(self):
        """
        Blocking method. It returns a list instead of a single value.

        It blocks until some values are in the queue. Then it return all the
        values in a single list.
        """

        with self.cond:
            while len(self.items) == 0:
                self.cond.wait()
            (items, self.items) = (self.items, [])
        return items


class QueueMail(threading.Thread):

    t = None

    q = Queue()
    e = threading.Event()

    send_mail = None

    @staticmethod
    def avvia(sendMail):
        QueueMail.send_mail = staticmethod(sendMail)
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
                    QueueMail.send_mail(subject, msg)

            if exit:
                return

            QueueMail.e.wait(60.0 * 2)


