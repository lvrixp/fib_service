# Development Environment #

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

### 2.Deploy fib service to production environment ###

2.1 Copy fib\_ws into /var/www/ folder (web root folder)

2.2 Create a WSGI file under /var/www/fib\_ws/ folder, named fib\_ws.wsgi. Apache will use this file to access the fib\_ws service.

    import sys
    sys.path.append('/var/www/fib_ws/')
    from fib_ws import app as application

2.3  Create your virtual host, update file /etc/apache2/sites-enabled/000-default.conf 

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

2.5 restart apache

    $ /etc/init.d/apache2 restart

Check the Apache error logs at /var/log/apache2/error.log if it failed.

