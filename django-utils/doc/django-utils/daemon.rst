Daemon
======

.. py:module:: djutils.daemon

A class that encapsulates the initialization required by a well-behaved
daemon.  Based on the code found here: http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/

.. py:class:: Daemon(object)

    .. py:method:: __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null')
    
        :param pidfile: full path to file in which to store pid of daemon
        :param stdin: file to use for stdin
        :param stdout: file to use for stdout
        :param stderr: file to use for stderr
    
    .. py:method:: run(self)
    
        override this method with your daemon code

See an example in `djutils.queue.bin.consumer`
