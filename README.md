## Description ##
**fib_service** is a simple rest service that resturn the front N fibonacci numbers.

## Directory structure ##

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
    	
## Design ##

### Core components and consideration ###
* Flask web server
    * Act as access point and rovide REST interface to end user
    * Call fib client library to delegate the real work
    * Extendable to support more interface on demand
    * Scalability potential gained by deploying more access point
* Fib client library
    * Provide RPC call interface to access the core business logic
    * Support more client implementation besides REST service
    * flexible and lightweighted deployment with limited dependency
* Fib RPC server
    * Service to handle potential heavy business logic
    * Scale out by deployment in distributed envrionment
    * Decoupling access point and business logic handling
    * Better performance potential with effective caching at server side

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
5. Server side robustness improvement including error detection, etc.

## Deployment (automation in TODO LIST) ##
### 0. Layout ###

* /usr/local/fib

		├── bin
		│   ├── fib_client_lib.py
		│   ├── fib_msg.py
		│   ├── fib_rpc_server.py
		│   ├── fib_server.py
		│   ├── fib_srv_app
		│   └── fib_workers.py
		└── lib
		    └── common
        		├── daemon_tool.py
        		├── __init__.py
        		├── logger.py
        		└── simple_cache.py
        		
* /var/www/fib_ws

		├── fib_ws.wsgi
		└── fib_ws.py

* /etc/init.d
		
		├── fibserver


### 1.Create a development environment ###

1.1 Install Python.

1.2 Install the Apache WSGI module and it’s prerequisites and then restart Apache.

    $ sudo aptitude install apache2 apache2.2-common apache2-mpm-prefork apache2-utils libexpat1 ssl-cert

    $ sudo aptitude install libapache2-mod-wsgi

    $ /etc/init.d/apache2 restart

1.3 Install Pip(Guide : http://www.jakowicz.com/flask-apache-wsgi/”http://pip.readthedocs.org/en/latest/installing.html”)

1.4 Install Flask

    $ pip install Flask

    Note:   If you want to create separate environments with different dependencies, Use the virtualenvwrapper tool(http://www.jakowicz.com/flask-apache-wsgi/”http://virtualenvwrapper.readthedocs.org/en/latest/”)

### 2.Deploy code ###
2.1 go to <git repo>/install

2.2 run ./install.sh (TODO)


### 3.Configure web service and start Fib rpc server ###

3.1  Create your virtual host, update file /etc/apache2/sites-enabled/000-default.conf 

    <virtualhost *:80>
        ServerAdmin webmaster@locahost
        DocumentRoot /var/www/fib_ws/
        WSGIScriptAlias / /var/www/fib_ws/fib_ws.wsgi

        <directory /var/www/fib_ws>
            WSGIProcessGroup webtool
            WSGIApplicationGroup %{GLOBAL}
            WSGIScriptReloading On
            <files>
                Order deny,allow
                Allow from all
            </files>
        </directory>
        ErrorLog ${APACHE_LOG_DIR}/error.log
        LogLevel warn
        CustomLog ${APACHE_LOG_DIR}/access.log combined
    </virtualhost>

3.2 Start fibserver

    $ sudo service fibserver start 

3.3 Restart apache

    $ sudo service apache2 restart

Check the Apache error logs at /var/log/apache2/error.log if it failed.

## Limitation  ##

**TODO**

## Trouble shooting ##

1. Service no response to normal input

    sudo service fibserver restart

    sudo service apache2 restart


