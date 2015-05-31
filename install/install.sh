#!/bin/bash

# TODO
#    Customized installation
#    Consider autoconfig
#    Consider upgrade
#    

# In TODO list  #
# NOT finished  #

BASEDIR=/usr/local/fibtest
BINDIR=$BASEDIR/bin
LIBDIR=$BASEDIR/lib
WSDIR=/var/www/fib_ws_test

echo "Checking ..."

test ! -e $WSDIR && echo -e "Error: $WSDIR doesn't exist.\nPlease configure flask virtual environment first" && exit 1

echo "Checking finished ..."

mkdir -p $BINDIR
mkdir -p $LIBDIR

echo "Copying files ..."
cp src/fib_server/* $BINDIR/
cp src/fib_client/* $BINDIR/
cp src/fib_common/*.py $BINDIR/
cp -r src/fib_common/common $LIBDIR/
cp src/fib_ws/* $WSDIR/

#cp script/* /etc/init.d/
echo "Copy files finished..."


