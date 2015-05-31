'''Definition of core task handling at rpc server and client lib side

Design:
    Server side:
        a. Task is delelated from the epoll server to the server side 
        thread pool.
        b. Task.done embeds the call back to notify epoll server and will
        response to the client side.
        c. Front N fibonacci numbers will be calculated on demand and saved in
        local array.

        TODO:
            server side caching mechnism to boost request handling
            server side data persistence to boost starting

    Client side:
        a. Each client thread create a connection to server at startup
        and serve coming request.
        b. When client thread sends a request, it will block and wait
        the response. When response is back, client thread will call
        task done to notify the object that wait for the event.
        c. When client lib add a task, it will wait on the task done
        event, thus make client lib call a sync call. When the event
        is set, client lib will check the response and return to the 
        caller.       

        TODO:
            client side retry mechism on the failure request.
            client thread reconnect when a connection is broken.
'''

import threading
import Queue
import select
import json
import socket
import sys
sys.path.insert(0, '/usr/local/fib/lib')
sys.path.insert(0, '/usr/local/fib/lib/common')

from fib_msg import FibCliSrvMsg, FibSrvCliMsg
from common import logger

LOGGING = logger.get_log()

class FibServerTask(object):
    '''Server side task definition
    '''
    def __init__(self, datalist, fd, datas, epoll_fd):
        '''Constructor
        '''
        self.datalist = datalist
        self.fd = fd
        self.datas = datas
        self.epoll_fd = epoll_fd

    def done(self, res):
        '''Call back to notify epoll server
        '''
        self.datalist[self.fd] = res

        # ready to send back to client
        self.epoll_fd.modify(self.fd, select.EPOLLET | select.EPOLLOUT)


class FibClientTask(object):
    '''Client side task definition
    '''
    def __init__(self, N):
        '''Constructor
        '''
        self.N = N
        self.res = []
        self.event = threading.Event()

    def done(self, res):
        # use list append to avoid copying string
        self.res.append(res)
        self.event.set()

    def wait(self):
        self.event.wait()


class FibWorkers(object):
    '''Common threading pool definition for server/client workers
    '''
    def __init__(self, thread_cnt):
        self._thread_cnt = thread_cnt
        self._workers = []
        self._tasks = Queue.Queue()

    def start(self):
        '''Start the threads

        TODO:
            Add graceful shut down to handle the task in the queue
        '''
        for i in range(self._thread_cnt):
            worker = threading.Thread(target=self.__class__._do_work, args=(self,))
            self._workers.append(worker)
            worker.setDaemon(True)
            worker.start()

    def add_task(self, task):
        self._tasks.put(task)

    def _do_work(self):
        '''Derived class should implement this
        '''
        pass


class FibServerWorkers(FibWorkers):
    '''Server side workers definition
    '''
    def __init__(self, *args):
        super(FibServerWorkers, self).__init__(*args)

        # this lock will be required when someone
        # need to calculate fibonacci sequence
        self._lock = threading.RLock()

        # initial value of fibonacci array is [0, 1]
        self._N = 2
        self._items = [0, 1]

    def _do_work(self):
        while True:
            task = self._tasks.get()
            msg = FibCliSrvMsg.deserialize(task.datas)

            # input value N by client
            N = msg.N

            # server side defensive check
            if N > 0:
                res = self._get_n_fib(N)
            else:
                res = "what do you expect :)"

            msg = FibSrvCliMsg()
            msg.N = N
            msg.result = res
            task.done(msg.serialize())

    def _get_n_fib(self, n):
        '''Function to get front n fibonacci numbers
        and will calculate on demand

        Front N numbers will be cached in local array
        if incoming n>N, someone will do the calculation
        '''

        if n > self._N:
            self._lock.acquire()
            while self._N < n:
                # fill in the local array
                self._items.append(self._items[-1] + self._items[-2])
                self._N += 1
            self._lock.release()

        # TODO:
        #    Here's heavy string operation, need caching to speed up
        return ' '.join(map(lambda a: str(a), self._items[:n]))


# 64MB, client side receive length should be long enough
RECEIVE_LEN = 64*1024*1024 


class FibClientWorkers(FibWorkers):
    '''Client side workers definition
    '''
    def __init__(self, thread_cnt, host, port):
        '''Constructor
        '''
        super(FibClientWorkers, self).__init__(thread_cnt)
        self._host = host
        self._port = port


    def _do_work(self):
        '''This thread function will create connection with server
        and block waiting the response.

        TODO:
            Need to consider the improvement of blocking manner.
            When the connection failure occur, need to reconnect.
        '''
        try:
            connFd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        except socket.error, msg:
            LOGGING.error(str(msg))
    
        try:
            connFd.connect((self._host, self._port))
            LOGGING.debug("connect to network server success")
        except socket.error,msg:
            LOGGING.error(str(msg))    

        while True:
            task = self._tasks.get()
            msg = FibCliSrvMsg(task.N)
            data = msg.serialize()
            if connFd.send(data) != len(data):
                LOGGING.error("send data to network server failed")
                break

            # TODO:
            #    consider error handling and bad connection
            readData = connFd.recv(RECEIVE_LEN)
            task.done(readData)

        connFd.close()

