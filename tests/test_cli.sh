#!/bin/bash

PREFIX="$1"

fail() {
    echo "$@" >&2
    exit 1
}

reset_lock() {
    local current
    current=$(stormlock current $1 --id-only)
    if [[ $? -eq 0 ]]; then
        stormlock release $1 "$current"
    fi
}

resource1="${PREFIX}test"
resource2="${PREFIX}test2"

# clear any existing locks
reset_lock $resource1
reset_lock $resource2

id1=$(stormlock acquire $resource1)
echo "Locked $resource1 with $id1"

stormlock is-held $resource1 "$id1" || fail "lock not held"

read principle timestamp lease_id < <(stormlock current $resource1)
echo "principle=$principle created=$timestamp id=$lease_id"

[[ "$principle" == "test_user" ]] || fail "unexpected principle ${principle}"
[[ "$lease_id" == "$id1" ]] || fail "unexpected lease id ${lease_id}"

stormlock acquire $resource1 && fail "able to acquire held lock" || true

res2_id=$(stormlock acquire $resource2) 
[[ $? -eq 0 ]] || fail "unable to acquire lock on another resource"

stormlock release $resource1 "$id1"

id2=$(stormlock acquire $resource1 -t '4 seconds')
echo "Reacquired lock with id $id2"

stormlock is-held $resource1 "$id1" && fail "old lock still held" || true

sleep 2
stormlock renew $resource1 "$id2" -t '4 seconds'
sleep 2

stormlock acquire $resource1 && fail "able to acquire held lock" || true
sleep 2

stormlock renew $resource1 "$id2" -t '4 seconds' && fail "able to renew expired lock" || true

stormlock is-held $resource1 "$id2" && fail "expired lock still held" || true

stormlock release $resource2 "$res2_id"

