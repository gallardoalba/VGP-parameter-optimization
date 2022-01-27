#!/usr/bin/python3


from os import walk,path,makedirs,listdir
from multiprocessing import Process, Semaphore
from subprocess import Popen, PIPE
from time import sleep

def launch_planemo(RUN,LOG,SEMA):
    process = Popen(RUN, stdout=PIPE)
    output, error = process.communicate()
    if error:
        open(LOG,"a").write(error)
    SEMA.release()

def generate_RUNS(LOG):
    WORKFLOWS_FOLDER = "../workflows/"
    DATA = "../data/partial_default_inputs.yml"
    CMMD = 'planemo run {} {} --download_outputs --profile EU --history_name {} --output_directory {}'
    #CMMD = 'planemo run {} {} --profile EU --history_name {} --no_wait'
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
                else:
                    FILES = [path.join(OUTPUT_PATH,x) for x in listdir(OUTPUT_PATH)]
                    if len(FILES) < 2:
                        RUN = (CMMD.format(workflow,DATA,HISTORY_NAME,OUTPUT_PATH))
                        RUN = [x for x in RUN.split(" ") if x != ""]
                        RUNS.append(RUN)
                    for f in FILES:
                        size = path.getsize(f)
                        if size != 837 and size != 12134118:
                            RUN = (CMMD.format(workflow,DATA,HISTORY_NAME,OUTPUT_PATH))
                            RUN = [x for x in RUN.split(" ") if x != ""]
                            RUNS.append(RUN)
                        
    print("\n\n[x] {} workflows will be launched...".format(len(RUNS)))
    sleep(2)
    return(RUNS)

def main():
    LOG = "../outputs/outputs.log"
    RUNS = generate_RUNS(LOG)
    #for RUN in RUNS:
    #    launch_planemo(RUN, LOG)
    nThreads = 200
    sema = Semaphore(nThreads)
    processes = [Process(target=launch_planemo, args=(RUN, LOG, sema)) for RUN in RUNS]
    for p in processes:
        sema.acquire()
        p.start()
        
    for p in processes: p.join()



if __name__ == "__main__":
    main()
