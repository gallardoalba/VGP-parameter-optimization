#!/usr/bin/python3

import pandas as pd
from matplotlib import pyplot as plt
from os import walk,path,makedirs,listdir
import numpy as np

font = {'family' : 'sans-serif',
        'weight' : 'normal',
        'size'   : 14}

OUTPUT_FOLDER = "../outputs/"
CONFIG_FILE = "../data/config.csv"

def main():
    config_raw = open(CONFIG_FILE).readlines()[1:]
    config = {}
    for i in config_raw:
        entry = i.strip().split(",")
        config[entry[0]] = {}
        config[entry[0]]["type"] = entry[1]
        config[entry[0]]["default"] = entry[2]
        config[entry[0]]["min"] = entry[3]
        config[entry[0]]["max"] = entry[4]
    files = [path.join(OUTPUT_FOLDER,x) for x in listdir(OUTPUT_FOLDER) if "pkl" in x]
    print(config)
    for file in files:
        parameter = file.split(".")[-2]
        #df = pd.read_csv(file,sep="\t",encoding = "UTF-8")
        df = pd.read_pickle(file)
        columns = []; index = [0,1,2,3,4,5,6,7,8,9,15]
        for i in index:
            columns.append(df.columns.tolist()[i])
        for i in columns:
            df[i] = pd.to_numeric(df[i], downcast='integer')
            df[i] = np.log2(df[i])
        plt.figure(1,figsize=(16, 10), dpi=300)
        plt.rc('font', **font)
        #ax = plt.gca()
        fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
        df.plot(use_index=True, y=columns,ax=ax)
        plt.title("Effect of the parameter {}\n".format(parameter.split("/")[-1]))
        ax.set_xlabel('\nParameter value')
        ax.axvline(float(config[parameter.split("/")[-1]]["default"]), color="green", linestyle="dashed")
        ax.set_ylabel('Statistic value\n')
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left',fontsize=12,title="Assembly statistics")
        plt.tight_layout()
        plt.savefig('..{}.png'.format(parameter))
        #plt.show()
        #print(df)


    


if __name__ == "__main__":
    main()
