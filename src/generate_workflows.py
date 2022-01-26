#!/usr/bin/python

import sys
import json
from numpy import linspace as ls
from os import path,mkdir

workflow_file = sys.argv[1]
config_file = sys.argv[2]
n = int(sys.argv[3]) # number 
output_folder = sys.argv[4]


def main():
    if not path.exists(output_folder):
        mkdir(output_folder)
    config_raw = open(config_file).readlines()[1:]
    config = {}
    for i in config_raw:
        entry = i.strip().split(",")
        config[entry[0]] = {}
        config[entry[0]]["type"] = entry[1]
        config[entry[0]]["default"] = entry[2]
        config[entry[0]]["min"] = entry[3]
        config[entry[0]]["max"] = entry[4]

    workflow = json.load(open(workflow_file))
    if "purgedups_getseqs" in config_file:
        purgedups_json = json.loads(workflow["steps"]["4"]["tool_state"])
    else:
        purgedups_json = json.loads(workflow["steps"]["4"]["tool_state"])
    purgedups_params = purgedups_json["function_select"]
    for param in config.keys():
        if config[param]["type"] in ["int","float"]:
            min = int(config[param]["min"])
            max = int(config[param]["max"])
            if config[param]["type"] == "int":
                range_values = [int(x) for x in ls(min,max,n)]
            else:
                range_values = [x for x in ls(min,max,n)]
            states = []
            for i in range_values:
                purgedups_params[param] = str(i)
                workflow["steps"]["6"]["tool_state"] = json.dumps(purgedups_params)
                filename = "{}_{}.ga".format(param,i)
                param_folder = path.join(output_folder,param)
                if not path.exists(param_folder):
                    mkdir(param_folder)
                fullpath = path.join(param_folder,filename)
                output = json.dumps(workflow)
                with open(fullpath,"w") as tmp:
                    tmp.write(output)


if __name__ == "__main__":
    main()
