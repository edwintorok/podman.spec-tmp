#!/bin/bash
#
# Simple podman tests
#

set -x

exec >/tmp/test.debug.log 2>&1

echo "************************************************************************"
echo "* This log contains the debug output from test_podman.sh."
echo "*"
echo "* Short test PASS/FAIL summary is in test.log"
echo "************************************************************************"

rm -f /tmp/test.log
touch /tmp/test.log

counter_file=/tmp/test.counter.txt
echo 0 >| $counter_file

do_test() {
    local cmd="$1"; shift
    local expected_status="$1"; shift
    local expected_stdout="$1"; shift

    counter=$(expr $(< $counter_file) + 1)
    echo $counter >| $counter_file

    # Make debug log easier to read
    echo
    echo "--------------------------------------------------------------------"
    echo "-- test $counter"
    echo

    stdout=$(eval podman $cmd)
    status=$?
    if [ $status -ne $expected_status ]; then
        echo "FAIL $counter $cmd: status=$status (expected $expected_status)" >>/tmp/test.log
        return
    fi

    if [ "$expected_stdout" = "-" ]; then
        :
    elif [ -z "$expected_stdout" ]; then
        if [ -n "$stdout" ]; then
            echo "FAIL $counter $cmd : stdout='$stdout' (expected '')" >>/tmp/test.log
            return
        fi
    else
        if ! expr "$stdout" : "$expected_stdout"; then
            echo "FAIL $counter $cmd : stdout='$stdout' (expected '$expected_stdout')" >>/tmp/test.log
            return
        fi
    fi

    echo "PASS $counter $cmd" >>/tmp/test.log
}

# Clean slate
do_test "rm -a -f"  0 "-"
do_test "rmi -a -f" 0 "-"

do_test "info --format '{{.host.rootless}}'"         0 "false"
do_test "info --format '{{.store.GraphDriverName}}'" 0 "overlay"

do_test "pull alpine" 0 "-"
do_test "images --format {{.Repository}}:{{.Tag}}"  0 \
        "docker.io/library/alpine:latest"

do_test "run alpine sh -c 'echo hi'" 0 "hi"
do_test "run alpine date"            0 "-"
do_test "run alpine /bin/false"      1 ""

do_test "ps -a | wc -l"                             0 "4"
do_test "ps -a | grep false | grep -q 'Exited (1)'" 0 ""

# Final exit status: nonzero if the word FAIL is present in results
if grep -q FAIL /tmp/test.log; then
    exit 1
fi
exit 0
