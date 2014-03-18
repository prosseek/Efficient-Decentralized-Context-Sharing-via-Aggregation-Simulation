#!/bin/sh
param=$@

cd context
sh runtests.sh $param
cd -
cd context_aggregator
sh runtests.sh $param
cd -
cd aggregation_simulator
sh runtests.sh $param
cd -