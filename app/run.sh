#!/bin/bash
env=${1:-local}
if [ "$env" == "local" ]; then
    echo "Running app on localhost:8000"
    source ../.venv/bin/activate
    uvicorn main:app --reload --host 127.0.0.1
elif [ "$env" == "pub" ]; then
    echo "You might need to run the following command for this to work:"
    echo "sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080"
    echo "Running app on 0.0.0.0:80"
    source ../.venv/bin/activate
    uvicorn main:app --reload --host 0.0.0.0 --port 8080
else
    echo "Wrong value given, must be 'pub' or 'local'"
    echo "Input was: $1"
fi
