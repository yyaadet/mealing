#!/bin/bash
#
# Init file for uwsgi mealing server daemon
#
# chkconfig: 2345 55 25
# description: Mealing server daemon
#
# processname: uwsgi-mealing.sh
#

name=uwsgi-mealing
PID=/var/run/uwsgi-mealing.pid
command=/usr/bin/uwsgi
PORT=3051
LOGFILE=/home/web_log/uwsgi-mealing.log
HOME=/home/webapps/mealing/mealing

wait_for_pid () {
    try=0

    while test $try -lt 3 ; do

        case "$1" in
            'created')
            if [ -f "$2" ] ; then
                try=''
                break
            fi
            ;;

            'removed')
            if [ ! -f "$2" ] ; then
                try=''
                break
            fi
            ;;
        esac

        echo -n .
        try=`expr $try + 1`
        sleep 1

    done

}

case "$1" in
    start)
        echo -n "Starting $name " 
        ulimit -n 10000
        $command -w ${HOME}/app_uwsgi -M -p 4 --socket :$PORT -d $LOGFILE --pidfile $PID --max-request 1024 --limit-post 1048576 --logdate --uid nginx --gid nginx --disable-logging

        if [ "$?" != 0 ] ; then
            echo " failed" 
            exit 1
        fi

        wait_for_pid created $PID

        if [ -n "$try" ] ; then
            echo " failed" 
            exit 1
        else
            echo " done" 
        fi
    ;;
    stop)
        echo -n "Gracefully shutting down $name " 

        if [ ! -r $PID ] ; then
            echo "warning, no pid file found - $name is not running ?" 
            exit 1
        fi

        $command --stop $PID

        wait_for_pid removed $PID

        if [ -n "$try" ] ; then
            echo " failed. Use force-exit" 
            exit 1
        else
            echo " done" 
        fi
    ;;
    restart)
        $0 stop
        $0 start
    ;;
    *)
        echo "Usage: $0 {start|stop|restart}" 
        exit 1
    ;;

esac

