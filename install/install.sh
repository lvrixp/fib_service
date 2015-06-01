#!/bin/bash

# TODO
#    Customized installation
#    Consider autoconfig
#    Consider upgrade
#    

# This script is in TODO list  #
# NOT finished  #

BASEDIR=/usr/local/fib
BINDIR=$BASEDIR/bin
LIBDIR=$BASEDIR/lib
WSDIR=/var/www/fib_ws

echo "Checking ..."

# placeholder

echo "Checking finished ..."

mkdir -p $BINDIR
mkdir -p $LIBDIR
mkdir -p $WSDIR

echo "Copying files ..."
cp src/fib_server/* $BINDIR/
cp src/fib_client/* $BINDIR/
cp src/fib_common/*.py $BINDIR/
cp -r src/fib_common/common $LIBDIR/
cp src/fib_ws/* $WSDIR/
cp script/* /etc/init.d/

#cp script/* /etc/init.d/
echo "Copy files finished..."


