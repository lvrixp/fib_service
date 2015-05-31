'''An utility to provide daemonize function
'''

import os
import sys
import logging

from common import logger

LOGGING = logger.get_log()

# make a the process a daemon. 
#If any error happen, it will raise an exception.
def daemonize(root_dir="/", \
              pidfile="", \
              stdin="/dev/null", \
              stdout="/dev/null", \
              stderr="/dev/null"):
    '''
    Make the process into a daemon
    '''

    # Perform the first fork.
    try:
        LOGGING.info("before fork")
        pid = os.fork()
        if pid > 0:
            # Directly exit first parent without SystemExit exception
            os._exit(0)
    except OSError, excep:
        msg = "fork failed: (%d) %s" % (excep.errno, excep.strerror)
        LOGGING.error(msg)
        raise Exception(msg)
    LOGGING.info("after fork")

    # Decouple from parent environment.
    try:
        os.chdir(root_dir)
    except OSError, excep:
        msg = "chdir(%s) failed: (%d) %s" % (root_dir, excep.errno, excep.strerror)
        LOGGING.error(msg)
        raise Exception(msg)

    try:
        os.umask(0)
    except OSError, excep:
        msg = "umask failed: (%d) %s" % (excep.errno, excep.strerror)
        LOGGING.error(msg)
        raise Exception(msg)

    # create a new session and become the leader
    try:
        os.setsid()
    except OSError, excep:
        msg = "setsid failed: (%d) %s" % (excep.errno, excep.strerror)
        LOGGING.error(msg)
        raise Exception(msg)

    # Perform the second fork.
    try:
        pid = os.fork()
        if pid > 0:
            # Directly exit second parent without SystemExit exception
            os._exit(0)
    except OSError, excep:
        msg = "fork failed: (%d) %s" % (excep.errno, excep.strerror)
        LOGGING.error(msg)
        raise Exception(msg)

    # The process is now daemonized, redirect standard file descriptors.
    for filedesc in sys.stdout, sys.stderr:
        filedesc.flush()
    si = file(stdin, 'r')
    so = file(stdout, 'a+')
    se = file(stderr, 'a+', 0)

    try:
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
    except OSError, excep:
        msg = "dup2 failed: (%d) %s" % (excep.errno, excep.strerror)
        LOGGING.error(msg)
        raise Exception(msg)

    # Create the pid file if specified
    if pidfile != "":
        # remove any existing one before create the new one
        if os.path.exists(pidfile):
            os.remove(pidfile)
        pidfile_fd = open(pidfile, "w")
        pidfile_fd.write("%d" % os.getpid())
        pidfile_fd.close()
