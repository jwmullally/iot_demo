#!/bin/sh
set -x

ENDPOINT=${1:-http://device-endpoint}

rand() {
    NEW_RAND="$(awk "BEGIN{ srand($(cat /tmp/random | cut -c3-)); print rand() }")"
    echo "$NEW_RAND" > /tmp/random
    echo "$NEW_RAND"
}

gen_data() {
    cat <<EOF
{
    "sensors": {
        "a": $(rand),
        "b": $(rand)
    },
    "serial": "$1"
}
EOF
}

send_data() {
    curl \
        -sS \
        --header "Content-Type: application/json" \
        --request POST "$ENDPOINT" \
        --data "$(gen_data "$1")"
    echo
}

while [ 1 ]; do
    for serial in 1001 1002 1003 2001 2002 2003; do
        send_data "$serial"
    done
    sleep 5
done
