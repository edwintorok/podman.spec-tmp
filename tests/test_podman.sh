#!/bin/bash
#
# Simple podman tests
#

rm -f /tmp/test.log /tmp/test.debug.log

# Log program versions
rpm -q podman podman-tests >/tmp/test.debug.log

bats /usr/share/podman/test/system &> /tmp/test.log

echo "bats completed with status $?" >>/tmp/test.debug.log
