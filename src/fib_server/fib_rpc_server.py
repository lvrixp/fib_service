'''RPC server listen and serve requests

Server will delegate the task to server workers.

TODO: 
   1. Graceful shutdown: there's no signal handler for SIGTERM for now.
   Thus, tasks in the queue will be lost

   2. Code level abstraction: this server is a general epoll server. We
   can extract FibRPC specific logic and make the epoll server reusable
   in case that we may need more service that based on epoll server.
'''

import socket
import select, errno
import struct
import sys
sys.path.insert(0, '/usr/local/fib/lib')

from common import logger
from fib_workers import FibServerWorkers, FibServerTask

LOGGING = logger.get_log()
HEADERLEN = 8

class FibRPCServer(object):
    '''FibRPCServer listen and server RPC requests.

    This server will initialize FibServerWorkers that do the real job.
    '''
    def __init__(self, worker_cnt, host, port):
        self._worker_cnt = worker_cnt
        self._host = host
        self._port = port


    def serve_forever(self):
        # initlaize FibServersWorkers which is a thread pool
        workers = FibServerWorkers(self._worker_cnt)
        workers.start()
    
        try:
            listen_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        except socket.error, msg:
            LOGGING.error("create a socket failed")
        
        try:
            listen_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except socket.error, msg:
            LOGGING.error("setsocketopt error")
        
        try:
            # just binding localhost
            listen_fd.bind(('', self._port))
        except socket.error, msg:
            LOGGING.error("listen file id bind ip error")
        
        try:
            # wait queue length set to 100
            # TODO:
            #    This will impact on concurrent level of serving request
            #    Need performance to test to configure a default value
            listen_fd.listen(100)
        except socket.error, msg:
            LOGGING.error(msg)
        
        try:
            epoll_fd = select.epoll()
            epoll_fd.register(listen_fd.fileno(), select.EPOLLIN)
        except select.error, msg:
            LOGGING.error(msg)
        
        LOGGING.info("Start to serve")
        connections = {}
        addresses = {}
        datalist = {}
        while True:
            epoll_list = epoll_fd.poll()
            for fd, events in epoll_list:
                if fd == listen_fd.fileno():
                    conn, addr = listen_fd.accept()
                    LOGGING.debug("accept connection from %s, %d, fd = %d" % (addr[0], addr[1], conn.fileno()))
                    conn.setblocking(0)
                    epoll_fd.register(conn.fileno(), select.EPOLLIN | select.EPOLLET)
                    connections[conn.fileno()] = conn
                    addresses[conn.fileno()] = addr
                elif select.EPOLLIN & events:
                    datas = ''
                    # need while loop to handle edge trigger mode
                    # as there may be data hasn't been fetched
                    while True:
                        try:
                            data = connections[fd].recv(10)
                            if not data and not datas:
                                epoll_fd.unregister(fd)
                                connections[fd].close()
                                LOGGING.debug("%s, %d closed" % (addresses[fd][0], addresses[fd][1]))
                                break
                            else:
                                datas += data
                        except socket.error, msg:
                            if msg.errno == errno.EAGAIN:
                                LOGGING.debug("%s receive %s" % (fd, datas))
                                task = FibServerTask(datalist, fd, datas, epoll_fd)
                                workers.add_task(task)
                                break
                            else:
                                epoll_fd.unregister(fd)
                                connections[fd].close() 
                                LOGGING.error(msg)
                                break        
                elif select.EPOLLHUP & events:
                    epoll_fd.unregister(fd)
                    connections[fd].close()
                    LOGGING.debug("%s, %d closed" % (addresses[fd][0], addresses[fd][1])) 
                elif select.EPOLLOUT & events:
                    total_len = len(datalist[fd])
                    header = struct.pack('q', total_len)

                    # firstly, we send a header stands for the data
                    # then we send the outgoing data of this length
                    early_exit = False
                    try:
                        # we cannot even send 8 bytes, remove this connection
                        if HEADERLEN != connections[fd].send(header):
                            early_exit = True
                    except socket.error, msg:
                        LOGGING.error(str(msg))
                        early_exit = True

                    if early_exit:
                        epoll_fd.unregister(fd)
                        connections[fd].close()
                        LOGGING.error("Send header failure, remove this connection")
                        continue

                    send_len = 0             
                    while True:
                        try:
                            send_len += connections[fd].send(datalist[fd][send_len:])
                            if send_len == len(datalist[fd]):
                                epoll_fd.modify(fd, select.EPOLLIN | select.EPOLLET)
                                break
                        except socket.error, msg:
                            # need to wait for tcp free buffer
                            if msg.errno == errno.EAGAIN:
                                LOGGING.debug("tcp busy, try sending again")
                                continue
                            else:
                                epoll_fd.unregister(fd)
                                connections[fd].close()
                                LOGGING.error("Sending faulure: %s" % str(msg))
                                break
                else:
                    continue

if __name__ == '__main__':
    LOGGING = logger.init_log('/var/log/fib/fib_rpc_server.log')
    server = FibRPCServer(1, 'localhost', 2003)
    server.serve_forever()
