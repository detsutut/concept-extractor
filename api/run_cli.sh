#!/bin/bash
set -e
source ../.env

if [[ -n ${SSL_KEYFILE} && -n ${SSL_CERTFILE} ]]; then
    echo "Starting server with HTTPS..."
    uvicorn --app-dir=.. api:app --host 0.0.0.0 --port 7878 --ssl-keyfile ${SSL_KEYFILE} --ssl-certfile ${SSL_CERTFILE}
else
    echo -e "\e[43;30mWARNING: No SSL config. Starting HTTP server sith HTTP\e[0m"
    uvicorn --app-dir=.. api:app --host 0.0.0.0 --port 7878
fi