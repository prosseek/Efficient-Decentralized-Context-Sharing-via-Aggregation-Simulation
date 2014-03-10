#!/bin/sh
param=$1

cd context
sh runtests.sh $param
cd -