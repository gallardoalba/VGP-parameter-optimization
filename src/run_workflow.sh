#!/usr/bin/bash

#generate_workflows


#python3 generate_workflows.py ../data/purgedups_partial_pipeline.ga ../config_files/purgedups_purgedups.csv 20 ../workflows/purgedups_purgedups/

#python3 generate_workflows.py ../data/purgedups_partial_pipeline.ga ../config_files/purgedups_getseqs.csv 20 ../workflows/purgedups_getseqs/

WORKFLOW=../data/purgedups_partial_pipeline.ga
DATA=../data/partial_default_inputs.yml
GALAXY_URL=https://usegalaxy.eu/

planemo run $WORKFLOW $DATA --galaxy_url $GALAXY_URL --galaxy_user_key $GALAXY_API_KEY --history_name "Test optimization WF" --tags "purgedups"
