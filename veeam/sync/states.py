#Utility functions for saving the state of source folder 
import os
import pickle
import sync

def create_state_store(path):
    #Create a temp file to store the last recorded state of the source folder
    #Need to fully scan all dirs and subdirectories so will use source scan fn from sync module
    #loop through every file, directory and subdirectory in the path
    #compute the MD5 hash of the file content
    #save in a dict with the filename as index and md5 hash as value
    state = sync.scan_source(path)
    
    
    

def update_state_store(path, new_state):
    #Overwrite the previously stored state with the up to date state
    with open(path, 'w') as f:
        pickle.dump(new_state, f)
        

def compare_state(last_state, new_state) -> bool:
    #If ther have been no changes then return false i.e. no changes
    if last_state == new_state:
        return False
    #There have been changes so return true
    return True