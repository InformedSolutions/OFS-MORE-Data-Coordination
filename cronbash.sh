#!/usr/bin/env bash
/usr/local/bin/python3.5m /source/manage.py runcrons --force --settings=$PROJECT_SETTINGS
printenv
echo 'Cronbash running'