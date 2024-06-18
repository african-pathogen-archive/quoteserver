#!/bin/bash

if [[ -n "$DEBUG" ]] ; then
    if [[ -f /app/env.sh ]] ; then
        source /app/env.sh
    elif [[ -f ./env.sh ]] ; then
        source ./env.sh
    fi
    echo "DEBUG mode" >&2
fi

if [[ -d /app/venv ]] ; then
    source /app/venv/bin/activate
fi

uvicorn --app-dir /app --port ${PORT:-9000} --host 0.0.0.0 main:app
