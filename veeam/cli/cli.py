import sys
import os
import time
import argparse

#This module covers everything to do with the command line
#i.e. reading input from user, parsing that input and logging actions

def read(args = None):
    #Read in the command line arguments we will pass them as a list for testing 
    if not args:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser(description='Hello! This program will allow you to synchronise two folders. Let\'s Go!')
    parser.add_argument('source_folder', metavar = 'source_folder', type = str, help = 'Enter the path to your source folder')
    parser.add_argument('replica_folder', metavar = 'replica_folder', type = str, help = 'Enter the path to the replica folder')
    parser.add_argument('log_file', metavar = 'log_file', type = str, help = 'Enter the path to the log file')
    parser.add_argument('sync_interval', metavar = 'sync_interval', type = int, help = 'Enter synchronisation interval in seconds' )
    args = parser.parse_args(args)

    return args

def verify(args) -> bool:
    #Verify if the supplied sources exist and are valid
    

    #Check the file paths 
    paths = {
        "source_folder" : args.source_folder,
        "replica_folder" : args.replica_folder,
        "log_file" : args.log_file
    }
    return_value = True
    for path in paths:
        if not os.path.exists(paths[path]):
            print("Please enter a valid path for the ", path )
            return_value = False
    
    #check that time is an integer
    if not type(args.sync_interval) is int:
        print("Please enter an integer for sync period" )
        return_value = False
    
    #check that time is a positive number
    if args.sync_interval < 0:
        print("Please enter a positive integer for sync period")
        return_value = False
    
    # if all above conditions are met then the input should be valid
    return return_value

    
