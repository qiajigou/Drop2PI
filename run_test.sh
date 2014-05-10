#!/bin/bash

TEST_DIR="tests"

CMD="py.test -s $TEST_DIR"

echo $CMD

$CMD || result=$?

echo unnitest result is $result

exit $result