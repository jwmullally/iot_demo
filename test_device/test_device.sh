#!/bin/sh
set -x

ENDPOINT=${1:-device-endpoint:8080}

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
    "serial": "1234"
}
EOF
}

send_data() {
    curl \
        -sS \
        --header "Content-Type: application/json" \
        --request POST http://$ENDPOINT/ \
        --data "$(gen_data)"
    echo
}

while [ 1 ]; do
    send_data
    sleep 5
done
