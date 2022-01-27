#!/usr/bin/python3


from os import walk,path,makedirs,listdir
from multiprocessing import Process, Semaphore
from subprocess import Popen, PIPE
from time import sleep

OUTPUT_FOLDER = "../outputs/"
anames = ["purged_assembly.fasta","Purge overlaps on data 1 and data 8: get_seqs purged sequences"]
snames = ["Paste on data 6 and data 5","stats_assembly.tabular"]
def generate_RUNS(OUTPUT_FOLDER):
    assemblies = []; stats = []; aids = []; sids = []
    for root, dirs, files in walk(OUTPUT_FOLDER):
        if files:
            outputs = [path.join(root,f) for f in files]
            for f in outputs:
                content = open(f).read()
                fname = f.split("/")[-1]
                pname = f.split("/")[-2]
                if fname in anames:
                    print(fname)
                    if content not in assemblies:
                        assemblies.append(content)
                        aids.append("{}-{}".format(fname,pname))
                        
                elif fname in snames:
                    if content not in stats:
                        stats.append(content)
                        sids.append("{}-{}".format(fname,pname))
                
    return(aids,sids)

def main():
    aids,sids = generate_RUNS(OUTPUT_FOLDER)
    print(aids,sids)



if __name__ == "__main__":
    main()
