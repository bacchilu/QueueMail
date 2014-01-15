# QueueMail

QueueMail is a software architecture that let you send as many emails as you need. But if you're sending emails too freequently, the system keeps them in a buffer and sends them grouped in one single email, or fewer emails groups by subject.

So using QueueMail only one mail every 2 minutes is sent. Not more frequently than every 2 minutes.

Usage:


    import queuemail
    
    
    QueueMail.avvia()
    try:
        QueueMail.send(u'Ciao', u'Hello World! 1')
        QueueMail.send(u'Ciao', u'Hello World! 2')
        QueueMail.send(u'Ciao2', u'Hello World! 3')
    finally:
        QueueMail.stop()

# Queue2

Queue2 is a subclass of Queue.Queue of the Python STL. Queue2 as a getAll method very similar to the parent get method: getAll is a blocking method that waits if there are no values in the queue. But if there are values, they are all returned in a list.

# License

This software is distributed under the terms of the MIT license.