import re
import redis

from djutils.queue.backends.base import BaseQueue


class RedisQueue(BaseQueue):
    """
    A simple Queue that uses the redis to store messages
    """
    def __init__(self, name, connection):
        """
        QUEUE_CONNECTION = 'host:port:database' or defaults to localhost:6379:0
        """
        super(RedisQueue, self).__init__(name, connection)
        
        if not connection:
            connection = 'localhost:6379:0'
        
        self.queue_name = 'djutils.redis.%s' % re.sub('[^a-z0-9]', '', name)
        host, port, db = connection.split(':')

        self.conn = redis.Redis(
            host=host, port=int(port), db=int(db)
        )
    
    def write(self, data):
        self.conn.lpush(self.queue_name, data)
    
    def read(self):
        return self.conn.rpop(self.queue_name)
    
    def flush(self):
        self.conn.delete(self.queue_name)
    
    def __len__(self):
        return self.conn.llen(self.queue_name)


class RedisBlockingQueue(RedisQueue):
    """
    Use the blocking right pop, should result in messages getting
    executed close to immediately by the consumer as opposed to
    being polled for
    """
    blocking = True

    def read(self):
        return self.conn.brpop(self.queue_name)
