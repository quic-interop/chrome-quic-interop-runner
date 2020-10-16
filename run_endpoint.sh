#!/bin/bash

# Set up the routing needed for the simulation.
/setup.sh

if [ ! -z "$TESTCASE" ]; then
    case "$TESTCASE" in
        "http3") ;;
        *) exit 127 ;;
    esac
fi

service dbus start

CERTHASH=$(openssl x509 -pubkey < /certs/cert.pem | openssl pkey -pubin -outform der | openssl dgst -sha256 -binary | base64)

/wait-for-it.sh sim:57832 -s -t 30

python3 run.py --certhash "$CERTHASH"
