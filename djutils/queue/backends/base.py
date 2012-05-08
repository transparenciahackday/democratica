class BaseQueue(object):
    """
    Base implementation for a Queue, all backends should subclass
    """
    blocking = False
    
    def __init__(self, name, connection):
        """
        Initialize the Queue - this happens once when the module is loaded
        """
        self.name = name
        self.connection = connection
    
    def write(self, data):
        """
        Push 'data' onto the queue
        """
        raise NotImplementedError
    
    def read(self):
        """
        Pop 'data' from the queue, returning None if no data is available --
        an empty queue should not raise an Exception!
        """
        raise NotImplementedError
    
    def flush(self):
        """
        Delete everything from the queue
        """
        raise NotImplementedError
    
    def __len__(self):
        """
        Used primarily in tests, but return the number of items in the queue
        """
        raise NotImplementedError
