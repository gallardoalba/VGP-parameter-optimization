#!/usr/bin/python3

import pandas as pd
from matplotlib import pyplot as plt
from os import walk,path,makedirs,listdir

font = {'family' : 'sans-serif',
        'weight' : 'normal',
        'size'   : 16}

OUTPUT_FOLDER = "../outputs/"
headers = ["values","scaffold_L50","scaffold_N50","scaffold_L90","scaffold_N90",
           "scaffold_NG50","scaffold_len_max","scaffold_len_min","scaffold_len_mean",
           "scaffold_len_median","scaffold_len_std","scaffold_num_A","scaffold_num_T",
           "scaffold_num_C","scaffold_num_G","scaffold_num_N","scaffold_num_bp",
           "scaffold_num_bp_not_N","scaffold_num_seq","scaffold_GC_content_overall",
           "contig_L50","contig_N50","contig_L90","contig_N90","contig_NG50",
           "contig_len_max","contig_len_min","contig_len_mean","contig_len_median",
           "contig_len_std","contig_num_bp","contig_num_seq","number_of_gaps"]


def main():
    files = [path.join(OUTPUT_FOLDER,x) for x in listdir(OUTPUT_FOLDER) if "pkl" in x]
    for file in files:
        parameter = file.strip(".pkl")
        #df = pd.read_csv(file,sep="\t",encoding = "UTF-8")
        df = pd.read_pickle(file)
        columns = df.columns.tolist()[:10]
        plt.figure(1,figsize=(16, 10), dpi=300)
        plt.rc('font', **font)
        #ax = plt.gca()
        fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
        df.plot(use_index=True, y=columns,ax=ax)
        plt.title("Effect of the parameter {}\n".format(parameter.split("/")[-1]))
        ax.set_xlabel('\nParameter value')
        ax.set_ylabel('Statistic value\n')
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left',fontsize=12,title="Assembly statistics")
        plt.tight_layout()
        plt.savefig('..{}.png'.format(parameter))
        #plt.show()
        #print(df)


    


if __name__ == "__main__":
    main()
