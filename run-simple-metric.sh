#!/usr/bin/env bash

DATA_PATH=./tests_amr

for dat in tests_amr_sick tests_amr_fracas tests_amr_hans tests_amr_allen
do
    python3 simple_metric.py  $DATA_PATH/$dat.txt.amrhypothesis $DATA_PATH/$dat.txt.amrpremise > predictions/$dat-simpleMetricP.txt
done
echo "Done"
