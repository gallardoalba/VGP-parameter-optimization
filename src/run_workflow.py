#!/usr/bin/python3


from os import walk,path,makedirs,listdir
from multiprocessing import Process, Semaphore
from subprocess import Popen, PIPE
from time import sleep
from numpy import linspace as ls


WORKFLOW = "../data/purgedups_partial_pipeline_no_FASTA.ga"
PARAMETERS = "../data/partial_default_inputs.yml"
CONFIG_FILE = "../data/config.csv"
OUTPUT_FOLDER = "../outputs/"
CMMD = 'planemo run {} {} --download_outputs --profile EU --history_name {}  --output_directory {}'
QUEUE = []
N = 40

def launch_planemo(RUN,LOG,SEMA):
    process = Popen(RUN, stdout=PIPE)
    output, error = process.communicate()
    if error:
        open(LOG,"a").write(error)
    SEMA.release()

def generate_COMMANDS(temporal_files,LOG):    
    for temporal_file in temporal_files:
        HISTORY_NAME = temporal_file.split("/")[-1][:-4]
        OUTPUT_PATH = "../outputs/{}/".format(HISTORY_NAME)
        if not path.isdir(OUTPUT_PATH):
            makedirs(OUTPUT_PATH)
        files = [path.join(OUTPUT_PATH,x) for x in listdir(OUTPUT_PATH)]
        CMMD_RUN = CMMD.format(WORKFLOW,temporal_file,HISTORY_NAME,OUTPUT_PATH)
        CMMD_RUN = [x for x in CMMD_RUN.split(" ") if x != ""]
        #print(len(files))
        if len(files) == 0:    
            QUEUE.append(CMMD_RUN)
        if files:          
            for f in files:
                size = path.getsize(f)
                if size < 800:
                    QUEUE.append(CMMD_RUN)
    print("\n\n[x] {} workflows will be launched...".format(len(QUEUE)))
    sleep(2)
    return(QUEUE)

def main():
    config_raw = open(CONFIG_FILE).readlines()[1:]
    value_format = "{}: {}\n"; config = {}
    for i in config_raw:
        entry = i.strip().split(",")
        config[entry[0]] = {}
        config[entry[0]]["type"] = entry[1]
        config[entry[0]]["default"] = entry[2]
        config[entry[0]]["min"] = entry[3]
        config[entry[0]]["max"] = entry[4]
    LOG = "../outputs/outputs.log"
    parameters = open(PARAMETERS).readlines()
    temporal_files = []; pindex = 0
    for param in config.keys():
        parameters_temporal = parameters[:]
        if config[param]["type"] in ["int","float"]:
            min = int(config[param]["min"])
            max = int(config[param]["max"])
            if config[param]["type"] == "int":
                range_values = [int(x) for x in ls(min,max,N)]
            else:
                range_values = [round(x,2) for x in ls(min,max,N)]
            for i in range(len(parameters)):
                if param in parameters[i]: 
                    pindex = i; break
            for value in range_values:
                temporal_value = value_format.format(param,value)
                parameters_temporal[pindex] = temporal_value
                parameters_RUN = "".join(parameters_temporal)
                OUTPUT_FILE = "/tmp/{}_{}.yml".format(param,value)
                open(OUTPUT_FILE,"w").write(parameters_RUN)
                temporal_files.append(OUTPUT_FILE)
    CMMDS = generate_COMMANDS(temporal_files,LOG)
    nThreads = 100
    sema = Semaphore(nThreads)
    processes = [Process(target=launch_planemo, args=(CMMD, LOG, sema)) for CMMD in CMMDS]
    for p in processes:
        sema.acquire()
        p.start()
        sleep(0.5)
    for p in processes: p.join()

if __name__ == "__main__":
    main()
