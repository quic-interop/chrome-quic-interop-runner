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

for req in $REQUESTS; do
  echo "<a href=\"$req\" class=\"download\" download>download</a>" >> /save.html
done
echo "</body>\n</html>" >> /save.html

python3 run.py --certhash "$CERTHASH"
