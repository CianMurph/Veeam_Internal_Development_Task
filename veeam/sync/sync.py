#Utility functions for saving the state of source folder 
import os
import hashlib
import shutil
import logs

def scan_folder(path):
    state = {}
    for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()
                state[file_path] = file_hash
    return state

#The replica dictionary is set to track files in the source, but this means that
#if we scan for a new file in the replica directory that the next comparison with the 
#source dictionary will allways require us to copy every file over
#so to prevent this we need a function that replaces the keys in the replica dictionary
#with their relative counterparts
def convert_keys(rep_dict, rep_dir, src_dir):
    new_dict = {}
    for file_dir, file_hash in rep_dict.items():
        relative_rep_path = os.path.relpath(file_dir, rep_dir)
        corresponding_src_path = os.path.join(src_dir,relative_rep_path)
        new_dict[corresponding_src_path] = file_hash
    return new_dict

def state_changed(last_state, new_state) -> bool:
    #If ther have been no changes then return false i.e. no changes
    if last_state == new_state:
        return False
    #There have been changes so return true
    return True

def get_changes(src_state, rep_state):
     #loop through replica dict
     #add any files that don't exist in src to delete list
     #add any files that are different to source to update list
    delete_list = []
    update_list = []
    copy_list = []
    for file, file_hash in rep_state.items():
        if file not in src_state.keys():
            #The file has been removed from the src folder and should be deleted
            delete_list.append(file)
        if file in src_state.keys():
            if src_state[file] != file_hash:
                #The MD5 in src is different so we need to update the file in rep
                update_list.append(file)
     #loop through src dict
    for file in src_state:
        if file not in rep_state.keys():
            copy_list.append(file)
     #add any files that don't exist in rep to copy list
    return copy_list, update_list, delete_list




def update_files(src_dict, rep_dict, src_dir, rep_dir, changes_list, log_stream, update = False):
    #loop through list and copy or update file from src to replica
    for file_path in changes_list:
        #get the file path relative to the source folder including subdirs etc
        #since this will be the same relaive to the replica folder
        relative_src_path = os.path.relpath(file_path, src_dir)
        corresponding_replica_file_path = os.path.join(rep_dir, relative_src_path)
        split_corresponding_path = os.path.split(corresponding_replica_file_path)
        parent = split_corresponding_path[0]
        if not os.path.exists(parent):
            os.makedirs(parent)
        shutil.copy2(file_path, parent)
        message = f"Copied {file_path} to {corresponding_replica_file_path}" if not update else f"Updated value of {corresponding_replica_file_path} to match {file_path}"
        logs.log(log_stream, message)
        rep_dict[file_path] = src_dict[file_path]
    return rep_dict



def delete_files(rep_dict, src_dir, rep_dir, delete_list, log_stream):
    for file in delete_list:
        relative_src_path = os.path.relpath(file, src_dir)
        replica_file_path = os.path.join(rep_dir, relative_src_path)
        os.remove(replica_file_path)
        logs.log(log_stream,  f"Deleted {replica_file_path} from {rep_dir}")
        del rep_dict[file]
    
    return rep_dict