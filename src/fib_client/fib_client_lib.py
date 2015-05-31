'''Client library to provide RPC call to get front N fibonacci elements
'''

import sys
import random
import json
from fib_workers import FibClientTask, FibClientWorkers


class FibClientLib(object):
    '''Client library to communicate with fibonacci service

    This class will initialize client side worker thread to \
    create connection with server side and the RPC call will \
    be handled by the thread pool and reuse the connections \
    that created by each threads
    '''
    def __init__(self, worker_cnt, host, port):
        '''Constructor will initialize the workers to connect
        to fibonacci server
        '''
        self._workers = FibClientWorkers(worker_cnt, host, port)
        self._workers.start()

    def get_fib_n(self, n):
        '''This sync RPC call will add a client task to the workers

        Args:
            n: front N elements that is required

        Returns:
            json object that contains the result
        '''

        # TODO:
        #    Add retry mechinism for failure task
        task = FibClientTask(n)
        self._workers.add_task(task)

        # wait for the task to finish
        task.wait()
        return json.loads(task.res[0])

if __name__ == '__main__':
    lib = FibClientLib(5, "localhost", 2003)
    try:
        for i in range(10):
            print lib.get_fib_n(random.randint(i,5*i))
    except ValueError, err:
        msg = "ValueError: too big input\n"
        print str(err)
        sys.stderr.write(msg)


