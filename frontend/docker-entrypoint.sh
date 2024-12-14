#!/bin/bash
envtoconfig -f /opt/project/dist/cst-app/browser/assets/config.json -d 'true' &
service start
sleep infinity
