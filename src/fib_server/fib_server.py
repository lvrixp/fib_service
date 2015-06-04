'''FibServer handle daemonization and hold RPC server object to serve RPC requests
'''

import fcntl
import os
import sys
import signal

from fib_rpc_server import FibRPCServer

sys.path.insert(0, '/usr/local/fib/lib/')

from common import daemon_tool as daemon
from common import logger

SLEEP_INTERVAL = 5
LOGGING = logger.get_log()


class FibServer(object):
    '''FibServer handle daemonization and 
       hold RPC server object to serve RPC requests
    '''

    def __init__(self, pidfile, lockfile, daemonize = False, verbose=False):
        '''Constructor
        '''
        self.pidfile = pidfile
        self.lockfile = lockfile
        self.daemonize = daemonize
        self.verbose = verbose
        self.running_flag = False  
        
    def register_signal_handler(self):
        '''Register the signal handler
        '''
        def agent_signal_handler(signum, frame):
            '''Agent signal handler

            TODO:
                Add debug infomation for the signal
            '''
            self.stop()

        signal.signal(signal.SIGINT, agent_signal_handler)
        signal.signal(signal.SIGTERM, agent_signal_handler)
        signal.signal(signal.SIGPIPE, signal.SIG_IGN)


    def start(self):
        '''Daemonize the service
        '''
        self.running_flag = True
        LOGGING.info("starting now")

        # Check the lockfile to make sure there is only one instance running
        self.lockfile_fd = open(self.lockfile, "a+")
        try:
            fcntl.flock(self.lockfile_fd.fileno(), fcntl.LOCK_EX|fcntl.LOCK_NB)
        except IOError, excep:
            msg = "lock file (%s) failed, (%d) %s" % \
                  (self.lockfile, excep.errno, excep.strerror)
            LOGGING.error(msg)
            sys.exit(1)
       
        try:
            if self.daemonize:                
                if self.verbose:
                    daemon.daemonize("/",
                                     self.pidfile,
                                     "/dev/stdin",
                                     "/dev/stdout",
                                     "/dev/stderr")
                else:
                    daemon.daemonize("/", self.pidfile)
        except Exception, excep:
            msg = "daemonize failed, pid %d. Error: %s" % (os.getpid(), excep)
            LOGGING.error(msg)

            # Release the file lock
            self.lockfile_fd.close()
            os.remove(self.lockfile)
            sys.exit(2)

        # Setup the signal handler
        self.register_signal_handler()
       
        msg = "Fibonacci RPC server is starting."
        LOGGING.info(msg)

        server = FibRPCServer(3, 'localhost', 2003)
        server.serve_forever()

        msg = "Fibonacci RPC server is running."
        LOGGING.info(msg)
        

    def stop(self):
        '''Stop the the service

        TODO:
            More cleanup work like pid/lock file handling
        '''
        if not self.running_flag:
            msg = "Stop fib server failed: " \
                  "already stopped."
            LOGGING.error(msg)
            raise Exception(msg)

        # set the running flag and inform the thread
        self.running_flag = False
        sys.exit(0)
