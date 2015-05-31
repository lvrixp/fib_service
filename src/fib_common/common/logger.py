'''A logger provide simpler interface:

   - main script to decides the log with init_log
   - imported script will follow the main log with get_log
'''

import sys
import os
import logging

class InfoWarningFilter(logging.Filter):
    """special filter only allow INFO and WARNING messages pass
    """
    def filter(self, rec):
        """filter out levels other than INFO and WARNING
        """
        return (rec.levelno == logging.INFO) or (rec.levelno == logging.WARNING)


class DebugInfoWarningFilter(logging.Filter):
    """special filter only allow DEBUG, INFO and WARNING messages pass
    """
    def filter(self, rec):
        """filter out levels other than DEBUG, INFO and WARNING
        """
        return ((rec.levelno == logging.DEBUG) or (rec.levelno == logging.INFO) \
            or (rec.levelno == logging.WARNING))

# this log will be initialized by init_log when some main script call it
log = None

# use main script name as the name of logger
logname = os.path.basename(sys.argv[0])+'full'

def init_log(logfile = None, verbose = False):
    """initiate logging streams
    """
    global log
    if log is not None: 
        return log

    # common format that we required
    short_format = "%(levelname)s:%(message)s"
    short_formatter = logging.Formatter(short_format)
    long_format = "%(asctime)s %(filename)s:%(lineno)d - PID:%(process)d:- %(levelname)s: %(message)s"
    long_formatter = logging.Formatter(long_format)

    global logname
    log = logging.getLogger(logname)
    log.setLevel(logging.DEBUG)

    # create file log handler
    if logfile:
        basedir = os.path.dirname(logfile)
        if not os.path.exists(basedir):
            os.makedirs(basedir)
        tmp_log_handler = logging.FileHandler(logfile)
        tmp_log_handler.setLevel(logging.DEBUG)
        tmp_log_handler.setFormatter(long_formatter)
        log.addHandler(tmp_log_handler)

    # create stdout handler
    tmp_log_handler = logging.StreamHandler(sys.stdout)
    tmp_log_handler.setLevel(logging.DEBUG)
    if verbose:
        tmp_log_handler.addFilter(DebugInfoWarningFilter())
    else:
        tmp_log_handler.addFilter(InfoWarningFilter())
    tmp_log_handler.setFormatter(short_formatter)
    log.addHandler(tmp_log_handler)

    # create stderr handler
    tmp_log_handler = logging.StreamHandler(sys.stderr)
    tmp_log_handler.setLevel(logging.ERROR)
    tmp_log_handler.setFormatter(short_formatter)
    log.addHandler(tmp_log_handler)
    return log

def get_log():
    """Get the universal logger shared by different tools
    The log use command line script name as it's ID
    Every tool has its own logger and share it with all its libs
    """
    global logname
    return logging.getLogger(logname)

