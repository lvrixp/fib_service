# Project Summary #

**fib_service** is a simple rest service that resturn the front N fibonacci numbers.

## Design ##
### Front end ###

**Web service implementation**

* Web service is based on flask framework, it calls FibClientLib library to communicate backend RPC service to retrieve the result.
        
        ws REST <- call -> FibClientLib  <- call ->  Fib RPC service
    
**Client library implementation**

* Client lib to start a thread pool.
* When interface is called, a task will be added to the task queue.
* Client interface is sync, it will wait for task finish.
* Simple caching is adopted at client side.

### Backend ###

**RPC service implementation**

* RPC service will epoll and serve client lib request
    * epoll server will hold a thread pool    
    * Accept request from client lib will be added to the thread pool
    
* Server side thread pool will handle request
    * An array that hold front N fibonacci numbers will be hold
    * If incoming request ask for more result, someone will do calculation to update the array.
    * Simple caching is adopted at server side.


### Summary ###

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

## TODO list ##
1. Deployment refinement to support distributed RPC servers.
2. Configuration management to support distributed deployment.
3. Monitoring mechinism in case of service down.
4. Sophisicated caching mechanism.

## Code Structure ##


    ├── conf							# configuration, in TODO list
    ├── doc
    │   └── project_summary.md		# summary of this project
    ├── install
    │   └── install.sh		# installation script, in TODO list
    ├── README.md				# this file
    ├── script
    │   └── fibserver			# service init script in /etc/init.d
    ├── src
    │   ├── fib_client
    │   │   └── fib_client_lib.py		# client lib to access fib RPC service 
    │   ├── fib_common
    │   │   ├── common
    │   │   │   ├── daemon_tool.py	# utility to demonize service
    │   │   │   ├── __init__.py
    │   │   │   ├── logger.py			# common logger
    │   │   │   └── simple_cache.py	# simple cache decorator
    │   │   ├── fib_msg.py	# message definition to client-server communication
    │   │   └── fib_workers.py		# Thread pool definition
    │   ├── fib_server
    │   │   ├── fib_rpc_server.py		# epoll server for RPC call
    │   │   ├── fib_server.py			# agent object to hold RPC server
    │   │   └── fib_srv_app			# daemon service to hold agent object
    │   └── fib_ws
    │       ├── fib_ws.py				# web service code implement REST API
    │       └── fib_ws.wsgi			# wsgi file to integrate with apache
    └── test
    	├── performance_data.md		# simple performance data with apache AB
    	└── test_plan.md				# test plan document


## Testing ##
    Please reference test/test_plan.md


## Performance ##
    Please reference test/performance_data.md

## Limitation ##
    Please reference TODO list

## TODO list ##
1. Deployment refinement to support distributed RPC servers.
2. Configuration management to support distributed deployment.
3. Monitoring mechinism in case of service down.
4. Sophisicated caching mechanism.

## Maintenance ##
**TBD**
