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

bats /usr/share/podman/test/system
