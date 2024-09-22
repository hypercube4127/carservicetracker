#!/bin/bash
PIDFILE="/run/app.pid"

PROGRAM="poetry"
ARGS="-v run start"
OUTPUT="/proc/1/fd/1"

start() {
  if [ -f "$PIDFILE" ]; then
    echo "Program already running (PID: $(cat $PIDFILE))"
    exit 1
  fi
  
  echo "Starting program..."
  nohup $PROGRAM $ARGS > $OUTPUT 2>&1 &
  echo $! > "$PIDFILE"
  echo "Program started with PID $(cat $PIDFILE)"
}

startfg() {
  if [ -f "$PIDFILE" ]; then
    echo "Program already running (PID: $(cat $PIDFILE))"
    exit 1
  fi
  
  echo "Starting program in foreground..."
  $PROGRAM $ARGS
}

stop() {
  if [ -f "$PIDFILE" ]; then
      PID=$(cat "$PIDFILE")
      if [ -d "/proc/$PID" ]; then
          echo "Stopping service (PID: $PID)..."
          kill $PID
          rm -f "$PIDFILE"
          echo "service stopped"
      else
          echo "Process not found for PID $PID. Removing stale PID file $PIDFILE"
          rm -f "$PIDFILE"
      fi
  else
      echo "Service is not running"
  fi
}

status() {
    if [ -f "$PIDFILE" ]; then
        PID=$(cat "$PIDFILE")
        if [ -d "/proc/$PID" ]; then
            echo "Service is running (PID: $PID)"
        else
            echo "Service is not running, but PID file exists. Removing stale PID file $PIDFILE"
            rm -f "$PIDFILE"
        fi
    else
        echo "Service is not running"
    fi
}

restart() {
  echo "Restarting program..."
  stop
  start
}

case "$1" in
  start)
    start
    ;;
  startfg)
    startfg
    ;;
  status)
    status
    ;;
  stop)
    stop
    ;;
  restart)
    restart
    ;;
  *)
    echo "Usage: $0 {start|startfg|stop|restart|status}"
    exit 1
    ;;
esac
