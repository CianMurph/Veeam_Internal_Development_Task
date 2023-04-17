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

    #get initial state of src folder and store in dictionary
    initial_state = sync.create_state_store(args.source_folder)
    
    while True:
        #
        time.sleep(args.sync_interval - ((time.time() - start_time) % args.sync_interval))
    
        

if __name__ == "__main__":
    main()