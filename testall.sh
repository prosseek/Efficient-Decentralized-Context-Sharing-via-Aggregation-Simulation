#!/bin/sh
param=$@

cd context
bash runtests.sh $param
cd -
cd context_aggregator
bash runtests.sh $param
cd -
cd aggregation_simulator
bash runtests.sh $param
cd -