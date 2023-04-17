import cli
import os
import pathlib
import time

def main():
    #args = cli.read()
    project_dir = pathlib.Path(__file__).parent.resolve()
    source_dir = project_dir + "/sample/src/"
    replica_dir = project_dir + "/sample/replica/"
    log_flie = project_dir + "/sample/log.txt"
    interval = 10


    # if args:
    #     print(args)
    # else:
    #     return -1

if __name__ == "__main__":
    main()