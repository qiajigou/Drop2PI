#!/bin/bash

LINT="pylint -E d2pi --msg-template={path}:{line}-{msg_id}"

echo $LINT

$LINT || result=$?

echo lint result is $result

exit $result