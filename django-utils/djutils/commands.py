from djutils.queue.decorators import queue_command
from djutils.utils.images import resize, Image


if Image:
    @queue_command
    def delayed_resize(source, dest, width, height=None):
        resize(source, dest, width, height)
