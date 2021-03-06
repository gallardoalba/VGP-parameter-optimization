#!/usr/bin/bash

#generate_workflows


#python3 generate_workflows.py ../data/purgedups_partial_pipeline.ga ../config_files/purgedups_purgedups.csv 20 ../workflows/purgedups_purgedups/

#python3 generate_workflows.py ../data/purgedups_partial_pipeline.ga ../config_files/purgedups_getseqs.csv 20 ../workflows/purgedups_getseqs/

WORKFLOW="../data/purgedups_partial_pipeline.ga"
DATA="../data/partial_default_inputs_local.yml"
GALAXY_URL="https://usegalaxy.eu/"
OUTDIR="../outputs/default_parameters/"


#planemo run $WORKFLOW $DATA --download_outputs --profile EU --history_name "Test_optimization_WF" --tags "purgedups" --output_directory $OUTDIR

planemo -v run $WORKFLOW $DATA --download_outputs --profile LOCAL --history_name "Test_optimization_WF" --output_directory ../outputs/
