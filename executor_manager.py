#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
executor_manager.py

ExecutorManager makes you configure a system to execute tasks.

Every task is not executed immediatly, but according to a politics defined in
the object configuration.

Es:

    ExecutorManager.avvia(sendMail, separateEmails)
    ExecutorManager.execute((u'subject1', u'body1'))
    ...
    ExecutorManager.stop()

sendMail is a function with arguments (subject, mail).
separateEmails takes a list of tuples (subject, mail) and returns a new tuple
(subject, mail) merging the bodies


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


class ExecutorJob(threading.Thread):

    def __init__(
        self,
        cb_fn,
        merge_fn,
        timeout=60.0,
        ):

        threading.Thread.__init__(self)
        self.cb_fn = cb_fn
        self.merge_fn = merge_fn

        self.timeout = timeout

        self.q = Queue()
        self.e = threading.Event()

    def stop(self):
        self.q.put(None)
        self.e.set()
        self.join()

    def putArg(self, arg):
        """
        Append the argument to be executed
        """

        self.q.put(arg)

    def getArguments(self):
        """
        Extract all pending arguments from the queue and returns them.
        """

        argsList = self.q.getAll()

        ret = []
        exit = False
        for arg in argsList:
            if arg is None:
                exit = True
                continue
            ret.append(arg)

        return (ret, exit)

    def run(self):
        """
        Get all messages, merges them and pass to the cb_fn function
        """

        while True:
            (argsList, exit) = self.getArguments()

            if len(argsList) > 0:
                arg = self.merge_fn(argsList)
                self.cb_fn(*arg)

            if exit:
                return

            self.e.wait(self.timeout)


from Queue import Queue as StlQueue


class ExecutorManager(threading.Thread):

    t = None

    q = StlQueue()

    cb_fn = None
    merge_fn = None
    key_fn = None

    job = {}

    @staticmethod
    def avvia(cb_fn, merge_fn, key_fn=None):
        ExecutorManager.cb_fn = staticmethod(cb_fn)
        ExecutorManager.merge_fn = staticmethod(merge_fn)
        if key_fn is not None:
            ExecutorManager.key_fn = staticmethod(key_fn)
        else:
            ExecutorManager.key_fn = None
        ExecutorManager.t = ExecutorManager()
        ExecutorManager.t.start()

    @staticmethod
    def stop():
        ExecutorManager.q.put(None)
        ExecutorManager.t.join()
        for job in ExecutorManager.job.itervalues():
            job.stop()
        ExecutorManager.job = {}

    @staticmethod
    def execute(arg):
        """
        Append the argument to be executed
        """

        ExecutorManager.q.put(arg)

    def sendJob(self, arg):
        """
        This message is sent to correct job thread, according to the subject
        """

        k = 'all'
        if ExecutorManager.key_fn is not None:
            k = ExecutorManager.key_fn(arg)

        job = ExecutorManager.job.get(k,
                ExecutorJob(ExecutorManager.cb_fn,
                ExecutorManager.merge_fn))
        ExecutorManager.job[k] = job
        if not job.isAlive():
            job.start()
        job.putArg(arg)

    def run(self):
        """
        Get all messages, joins them and send.
        """

        while True:
            arg = ExecutorManager.q.get()

            if arg is None:
                return

            self.sendJob(arg)


