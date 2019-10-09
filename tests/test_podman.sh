#!/bin/bash -e
#
# Simple podman tests
#

# Log program and kernel versions
echo "Important package versions:"
(
    uname -r
    rpm -qa | egrep 'podman|conmon|crun|runc|iptable|slirp|systemd' | sort
) | sed -e 's/^/  /'

# Log environment; or at least the useful bits
echo "Environment:"
env | grep -v LS_COLORS= | sort | sed -e 's/^/  /'

bats /usr/share/podman/test/system
