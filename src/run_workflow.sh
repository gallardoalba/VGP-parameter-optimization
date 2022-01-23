#!/usr/bin/bash

#generate_workflows


python3 generate_workflows.py ../data/purgedups_partial_pipeline.ga ../config_files/purgedups_purgedups.csv 20 ../workflows/purgedups_purgedups/

python3 generate_workflows.py ../data/purgedups_partial_pipeline.ga ../config_files/purgedups_getseqs.csv 20 ../workflows/purgedups_getseqs/

