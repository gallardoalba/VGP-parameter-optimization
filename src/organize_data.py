#!/usr/bin/python3

import pandas as pd
from matplotlib import pyplot as plt
from os import walk,path,makedirs,listdir

OUTPUT_FOLDER = "../outputs/"
CONFIG_FILE = "../data/config.csv"
stats_name = "Paste on data 6 and data 5"

def main():
    folders = [x for x in listdir(OUTPUT_FOLDER) if ".pkl" not in x]
    parameters = list(set(["_".join(x.split("_")[:-1]) for x in folders]))
    for parameter in parameters:
        values = []
        database = pd.DataFrame()
        pfolder = sorted([x for x in folders if parameter in x])
        sfiles = [path.join(OUTPUT_FOLDER,x + "/" + stats_name) for x in pfolder]
        for i,f in enumerate(sfiles):
            option = f.split("/")[2].split("_")[-1]
            if "." in option:
                values.append(float(option))
            else:
                values.append(int(option))
            if database.empty:
                df = pd.read_csv(f, sep="\t", header=None).iloc[:,0:2]
            else:
                df = pd.read_csv(f, sep="\t", header=None).iloc[:,1]
            database = pd.concat([database, df],axis=1)
        database = database.transpose()
        header = database.iloc[0] #grab the first row for the header
        database = database[1:] #take the data less the header row
        database.columns = header #set the header row as the df header
        database.reset_index(drop="True")
        database["Values"] = values
        database = database.set_index("Values")
        database = database.sort_index(axis=0)
        filename = "../outputs/{}.pkl".format(parameter)
        database.to_pickle(filename)
        #filename = "../outputs/{}.csv".format(parameter)
        #database.to_csv(filename, sep='\t')



    


if __name__ == "__main__":
    main()
