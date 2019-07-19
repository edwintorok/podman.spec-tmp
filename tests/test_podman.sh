#!/bin/bash -e
#
# Simple podman tests
#

# Log program versions
rpm -q podman podman-tests

bats /usr/share/podman/test/system
