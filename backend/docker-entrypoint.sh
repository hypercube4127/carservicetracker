#!/bin/bash

if [ "$DEBUG_MODE" == 'True' ] || [ "$DEBUG_MODE" == 'true' ] || [ "$DEBUG_MODE" == '1' ]; then
    echo "Debug mode enabled. Run service as a background process."
    service start
    sleep infinity
else 
    service startfg
fi
