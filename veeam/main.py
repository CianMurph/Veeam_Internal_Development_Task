import cli
import sync
import logs
import time

def main():
    args = cli.read()
    #verify the arguments and exit if they are invalid i.e. non existing folders
    if not cli.verify(args):
        return -1
    
    #Write initialisation message to the console and the log file
    # set up logging
    log_stream = open(args.log_file, 'a')
    logs.log(log_stream,"Initialising Sync")
    start_time = time.time()  
    
    while True:
        #get the state of the source folder
        source_dict = sync.scan_folder(args.source_folder)
        #get the state of the replica folder
        replica_dict = sync.scan_folder(args.replica_folder)
        #convert the keys of the replica folder 
        replica_dict = sync.convert_keys(replica_dict, args.replica_folder, args.source_folder)

        
        #check if replica folder is different to source
        if sync.state_changed(replica_dict, source_dict):
            #if so apply changes
            copy_list, update_list, delete_list = sync.get_changes(source_dict, replica_dict)
            #if there are files to delete from the replica folder then do so
            if delete_list != []:
                replica_dict = sync.delete_files(replica_dict, args.source_folder, args.replica_folder, delete_list, log_stream)
            #if there are files to copy then copy them
            if copy_list != []:
                replica_dict = sync.update_files(source_dict, replica_dict, args.source_folder, args.replica_folder, copy_list, log_stream)
            #If any of the source files have been changed then update their counterparts
            if update_list != []:
                replica_dict = sync.update_files(source_dict, replica_dict, args.source_folder, args.replica_folder, update_list, log_stream, True)
        
        #sleep for specified interval
        time.sleep(args.sync_interval - ((time.time() - start_time) % args.sync_interval))
    
        

if __name__ == "__main__":
    main()