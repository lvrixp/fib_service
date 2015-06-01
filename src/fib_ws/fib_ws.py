#!/usr/bin/python

'''Entry point that will handle wsgi request and provide REST service

WS side will call fib client library which handles the RPC call to backend server.
'''

from flask import Flask, abort, jsonify
import sys
sys.path.insert(0, '/usr/local/fib/bin/')

from fib_client_lib import FibClientLib

__all__ = ['app']

# TODO:
#     all such configuration should be managed by
#     common configuration management object
client = FibClientLib(30, "localhost", 2003)

# Web service object
app = Flask(__name__)

# Basic routing
@app.route('/')
def index():
    return "Hello, World!\n"

# Routing request for /fib/*
@app.route('/fib/<int:front_n>', methods=['GET'])
def get_front_n(front_n):
    if front_n < 1:
        # return bad request code
        abort(400)
        
    res = client.get_fib_n(front_n)
    return jsonify(res)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=False)
