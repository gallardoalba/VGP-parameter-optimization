#!/usr/bin/python3


from os import walk,path,makedirs
from multiprocessing import Process
from subprocess import Popen, PIPE


def launch_planemo(RUN,LOG):
    process = Popen(RUN, stdout=PIPE)
    output, error = process.communicate()
    if error:
        open(LOG,"a").write(error)            

def generate_RUNS(LOG):
    WORKFLOWS_FOLDER = "../workflows/"
    DATA = "../data/partial_default_inputs.yml"
    CMMD = 'planemo run {} {} --download_outputs --profile EU --history_name {} --output_directory {}'
    RUNS = []
    for root, dirs, files in walk(WORKFLOWS_FOLDER):
        if files:
            workflows_paths = [path.join(root,f) for f in files]
            global workflow
            for workflow in workflows_paths:
                HISTORY_NAME = workflow.split("/")[-1].strip(".ga")
                OUTPUT_PATH = ".." + workflow.strip(".ga")
                OUTPUT_PATH = OUTPUT_PATH.replace("workflow","output")
                if not path.isdir(OUTPUT_PATH):
                    makedirs(OUTPUT_PATH)
                RUN = (CMMD.format(workflow,DATA,HISTORY_NAME,OUTPUT_PATH)).split(" ")
                RUN = [x for x in RUN if x != ""]
                RUNS.append(RUN)
    return(RUNS)

def main():
    LOG = "../outputs/outputs.log"
    RUNS = generate_RUNS(LOG)
    processes = [Process(target=launch_planemo, args=(RUN, LOG,)) for RUN in RUNS]
    for p in processes: p.start()
    for p in processes: p.join()
                #process = Popen(RUN, stdout=PIPE)
                #output, error = process.communicate()


if __name__ == "__main__":
    main()
