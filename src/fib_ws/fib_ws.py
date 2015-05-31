#!/home/steve/fib_ws/flask/bin/python
from flask import Flask, abort, jsonify
import sys
sys.path.insert(0, '/home/steve/net')

from fib_client_lib import FibClientLib



__all__ = ['app']

client = FibClientLib(30, "localhost", 2003)

app = Flask(__name__)
cache = {}

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/fib/<int:front_n>', methods=['GET'])
def get_front_n(front_n):
    app.logger.info("info log")
    app.logger.error("info log")
    if front_n < 1:
        abort(404)
    if front_n not in cache:
        res = client.get_fib_n(front_n)
        cache[front_n] = jsonify(res)
    return cache[front_n]
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=False)
