import datetime
import os

from django.conf import settings

from djutils.queue.exceptions import QueueException
from djutils.queue.registry import registry
from djutils.utils.helpers import load_class


def get_queue_class():
    return load_class(getattr(
        settings, 'QUEUE_CLASS', 'djutils.queue.backends.database.DatabaseQueue'
    ))

def get_queue_name():
    if hasattr(settings, 'QUEUE_NAME'):
        return settings.QUEUE_NAME
    else:
        return 'queue-%s' % (os.path.basename(settings.DATABASES['default']['NAME']))


class Invoker(object):
    """
    The :class:`Invoker` is responsible for reading and writing to the queue
    and executing messages.  It talks to the :class:`CommandRegistry` to load
    up the proper :class:`QueueCommand` for each message
    """
    
    def __init__(self, queue):
        self.queue = queue
    
    def write(self, msg):
        self.queue.write(msg)
    
    def enqueue(self, command):
        if getattr(settings, 'QUEUE_ALWAYS_EAGER', False):
            # if the queue is set to always eager, run commands in-process --
            # useful if you're running DEBUG
            return command.execute()
        
        self.write(registry.get_message_for_command(command))
    
    def read(self):
        return self.queue.read()
    
    def dequeue(self):
        msg = self.read()
        
        if msg:
            command = registry.get_command_for_message(msg)
            command.execute()
            return msg
    
    def flush(self):
        self.queue.flush()
    
    def enqueue_periodic_commands(self, dt=None):
        dt = dt or datetime.datetime.now()
        
        for command in registry.get_periodic_commands():
            if command.validate_datetime(dt):
                self.enqueue(command)


class QueueCommandMetaClass(type):
    def __init__(cls, name, bases, attrs):
        """
        Metaclass to ensure that all command classes are registered
        """
        registry.register(cls)


class QueueCommand(object):
    """
    A class that encapsulates the logic necessary to 'do something' given some
    arbitrary data.  When enqueued with the :class:`Invoker`, it will be
    stored in a queue for out-of-band execution via the consumer.  See also
    the :func:`queue_command` decorator, which can be used to automatically
    execute any function out-of-band.
    
    Example::
    
    class SendEmailCommand(QueueCommand):
        def execute(self):
            data = self.get_data()
            send_email(data['recipient'], data['subject'], data['body'])
    
    invoker.enqueue(
        SendEmailCommand({
            'recipient': 'somebody@spam.com',
            'subject': 'look at this awesome website',
            'body': 'http://youtube.com'
        })
    )
    """
    
    __metaclass__ = QueueCommandMetaClass
    
    def __init__(self, data=None):
        """
        Initialize the command object with a receiver and optional data.  The
        receiver object *must* be a django model instance.
        """
        self.set_data(data)

    def get_data(self):
        """Called by the Invoker when a command is being enqueued"""
        return self.data

    def set_data(self, data):
        """Called by the Invoker when a command is dequeued"""
        self.data = data

    def execute(self):
        """Execute any arbitary code here"""
        raise NotImplementedError


class PeriodicQueueCommand(QueueCommand):
    def validate_datetime(self, dt):
        """Validate that the command should execute at the given datetime"""
        return False


# dynamically load up an instance of the Queue class we're using
Queue = get_queue_class()

queue_name = get_queue_name()
queue = Queue(queue_name, getattr(settings, 'QUEUE_CONNECTION', None))
invoker = Invoker(queue)
