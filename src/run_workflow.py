#!/usr/bin/python3

from os import walk,path

workflows_folder = "../workflows/"
DATA="../data/partial_default_inputs_local.yml"
COMMD = 'planemo run {} {} --download_outputs --profile LOCAL --history_name {}  --output_directory {}'
def main():
    for root, dirs, files in walk(workflows_folder):
        if files:
            workflows_paths = [path.join(root,f) for f in files]
            for workflow in workflows_paths:
                HISTORY_NAME = workflow.split("/")[-1].strip(".ga")
                output_dir = "/".join(workflow.split("/")[:-1]).replace("workflows","outputs")
                print(output_dir)
                print(workflow)


if __name__ == "__main__":
    main()
