'''Simple message definition for the client-server communication

TODO:
    Add more sophicated schema for the message
    Eg, for server-client message, add return code, error mssage.
'''

import json

class FibMsg(object):
    '''Base message class placeholder
    '''
    def serialize(self):
        pass

class FibCliSrvMsg(FibMsg):
    '''Client-Server message definition

    Schema:
    {
        'N' : <integer> # front N number is required
    }
    '''
    def __init__(self, n = 0):
        self.N = int(n)

    def serialize(self):
        return json.dumps({'N' : self.N})

    @staticmethod
    def deserialize(msg):
        res = json.loads(msg)
        return FibCliSrvMsg(res['N'])


class FibSrvCliMsg(FibMsg):
    '''Server-Client message definition

    Schema:
    {
        'N' : <integer> # original value sent by client
        'result' : <string> # front N fibonacci numbers
    }
    '''
    def __init__(self, n = 0, res = ''):
        self.N = int(n)
        self.result = res

    def serialize(self):
        return json.dumps({'N' : self.N, 'result' : self.result})

    @staticmethod
    def deserialize(msg):
        res = json.loads(msg)
        return FibSrvCliMsg(res['N'], res['result'])
