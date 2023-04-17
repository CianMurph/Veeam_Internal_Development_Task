import sync
import pathlib
import os
import hashlib
test_dir = str(pathlib.Path(__file__).parent.resolve())


def write_files_and_compute_hash(file_dict, file_list, file_list_src, update = False):
    #we need to create a number of files and compute their hashes for most of these tests
    #this function is intended to reduce the amount of duplicated code in each tet

    message = "Testing that scan will return a dict with reference to this file\n" if update == False else "Testing that scan will return a dict with reference to this file edited\n"
    for index, file in enumerate(file_list):
        with open(file, "w") as f:
            f.write(message + f"Level {index}")
            f.close
        with open(file, 'rb') as f:
            file_hash_0 = hashlib.md5(f.read()).hexdigest()
            f.close
        file_dict[file_list_src[index]] = file_hash_0
    return file_dict


def test_scan_returns_dict():
    test_case_dir = os.path.join(test_dir, "test_sync", 'test_scan_fn_0')
    if not os.path.exists(test_case_dir):
        os.makedirs(test_case_dir)
    assert type(sync.scan_folder(test_case_dir)) == dict

def test_scan_returns_correct_dict():
    test_case_dir = os.path.join(test_dir, "test_sync", 'test_scan_fn_1')
    if not os.path.exists(test_case_dir):
        os.makedirs(os.path.join(test_case_dir,"test_sub_dir","test_sub_sub_dir"))
    message = "Testing that scan will return a dict with reference to this file\n"
    files = [os.path.join(test_case_dir, "test_file_0.txt"), 
os.path.join(test_case_dir ,"test_sub_dir", "test_file_1.txt"),
os.path.join(test_case_dir ,"test_sub_dir","test_sub_sub_dir", "test_file_2.txt")]
    #manually create files and sub directories and create state dict
    test_dict = write_files_and_compute_hash({},files, files)

    #check that the scan function creates the expected item
    assert sync.scan_folder(test_case_dir) == test_dict

def test_state_changed_returns_false_for_same_dicts():
    test_case_dir = os.path.join(test_dir, "test_sync", 'test_state_change_fns')
    if not os.path.exists(test_case_dir):
        os.makedirs(os.path.join(test_case_dir,"test_sub_dir","test_sub_sub_dir"))
    #manually create files and sub directories and create state dict
    files = [os.path.join(test_case_dir, "test_file_0.txt")]
    test_dict = write_files_and_compute_hash({},files, files)
        
    
    #Since last test passed we can assume that sync.scan folder gives same as test dict
    assert sync.state_changed(test_dict, sync.scan_folder(test_case_dir)) == False

def test_state_changed_returns_true_for_different_dicts():
    test_case_dir = os.path.join(test_dir, "test_sync", 'test_state_change_fns')
    if not os.path.exists(test_case_dir):
        os.makedirs(os.path.join(test_case_dir,"test_sub_dir","test_sub_sub_dir"))
    files = [os.path.join(test_case_dir, "test_file_0.txt")]
    #manually create files and sub directories and create state dict
    test_dict = write_files_and_compute_hash({},files, files)
    
    assert sync.state_changed(test_dict,{"key_0" : 5, "key_1": 10}) == True

def test_get_changes_returns_three_lists():

    src_dict = {}
    rep_dict = {}
    list_1, list_2, list_3 = sync.get_changes(src_dict, rep_dict)
    
    assert list_1 == []
    assert list_2 == []
    assert list_3 == []

def test_get_changes_returns_deleted_file():
    test_case_dir = os.path.join(test_dir, "test_sync", 'test_get_change_fn_0')
    test_case_src_dir = os.path.join(test_case_dir, "src")
    test_case_rep_dir = os.path.join(test_case_dir, "rep")
    if not os.path.exists(test_case_src_dir):
        os.makedirs(test_case_src_dir)
    if not os.path.exists(os.path.join(test_case_rep_dir ,"test_sub_dir")):
        os.makedirs(os.path.join(test_case_rep_dir ,"test_sub_dir"))
    
    #Create src folder 
    message = "Testing that scan will return a dict with reference to this file\n"
    
    files_src = [ os.path.join(test_case_src_dir, "test_file_0.txt")]
    files_rep = [os.path.join(test_case_rep_dir, "test_file_0.txt"), os.path.join(test_case_rep_dir ,"test_sub_dir", "test_file_1.txt")]
    #create src ref for deleted file
    files_src_ref = [os.path.join(test_case_src_dir, "test_file_0.txt") ,os.path.join(test_case_src_dir ,"test_sub_dir", "test_file_1.txt")]
    
    
    
    #manually create files and sub directories and create state dict
    src_dict = write_files_and_compute_hash({},files_src, files_src_ref)

    #Create Replica Folder with additional files 
    # keys reference src folder
    # Additional files emulate deleting files in src folder
    rep_dict = write_files_and_compute_hash({}, files_rep, files_src_ref)
    
    #File ref in position 1 does not exist in original array so should be returned
    expected_ret = [files_src_ref[1]]
    list_1, list_2, list_3 = sync.get_changes(src_dict, rep_dict)
    assert list_1 == []
    assert list_2 == []
    print(list_3)
    assert list_3 == expected_ret


def test_get_changes_returns_updated_file():
    test_case_dir = os.path.join(test_dir, "test_sync", 'test_get_change_fn_1')
    test_case_src_dir = os.path.join(test_case_dir, "src")
    test_case_rep_dir = os.path.join(test_case_dir, "rep")
    if not os.path.exists(test_case_src_dir):
        os.makedirs(test_case_src_dir)
    if not os.path.exists(test_case_rep_dir):
        os.makedirs(test_case_rep_dir)
    #Both source and replica folders will have the same file names
    files_src = [os.path.join(test_case_src_dir, "test_file_0.txt")]
    files_rep = [os.path.join(test_case_rep_dir, "test_file_0.txt")]

    #Write to the source and replica files
    src_dict = write_files_and_compute_hash({}, files_src, files_src)
    #True flag means that the content of the file in src and replica will be different
    rep_dict = write_files_and_compute_hash({}, files_rep, files_src, True)

    #Since file content is different the file name will be returned as the difference
    expected_ret = [files_src[0]]
    list_1, list_2, list_3 = sync.get_changes(src_dict, rep_dict)
    assert list_1 == []
    assert list_3 == []
    print(list_3)
    assert list_2 == expected_ret

def test_get_changes_returns_new_file():
    test_case_dir = os.path.join(test_dir, "test_sync", 'test_get_change_fn_2')
    test_case_src_dir = os.path.join(test_case_dir, "src")
    test_case_rep_dir = os.path.join(test_case_dir, "rep")
    if not os.path.exists(test_case_src_dir):
        os.makedirs(test_case_src_dir)
    if not os.path.exists(test_case_rep_dir):
        os.makedirs(test_case_rep_dir)

    #Create a new file in the src dir that does not exist in the rep directory
    files_src = [os.path.join(test_case_src_dir, "test_file_0.txt")]
    #Create the dictionary represesting src dir
    src_dict = write_files_and_compute_hash({}, files_src, files_src)
    #Rep directory intialised as empty
    rep_dict = {}
    
    #The new file should be returned as a change
    expected_ret = files_src
    list_1, list_2, list_3 = sync.get_changes(src_dict, rep_dict)
    assert list_1 == expected_ret
    assert list_3 == []
    print(list_3)
    assert list_2 == []


def test_update_files_returns_dict():
    test_case_dir = os.path.join(test_dir, "test_sync", 'test_update_files_fn_0')
    test_case_src_dir = os.path.join(test_case_dir, "src")
    test_case_rep_dir = os.path.join(test_case_dir, "rep")
    test_log_file = os.path.join(test_case_dir, "log.txt")
    if not os.path.exists(test_case_src_dir):
        os.makedirs(test_case_src_dir)
    if not os.path.exists(test_case_rep_dir):
        os.makedirs(test_case_rep_dir)
    if not os.path.exists(test_log_file):
        with open(test_log_file, 'w') as f:
            f.write("")
    test_log_stream = open(test_log_file, 'a')
    #Create a new file in the src dir that does not exist in the rep directory
    files_src = [os.path.join(test_case_src_dir, "test_file_0.txt")]
    #Create the dictionary represesting src dir
    src_dict = write_files_and_compute_hash({}, files_src, files_src)
    #Rep directory intialised as empty
    rep_dict = {}

    #Since above test passed we know that get changes will return the correct list 1
    list_1, list_2, list_3 = sync.get_changes(src_dict, rep_dict)
    #call update files and check that it returns a dictionary 
    rep_dict = sync.update_files(src_dict, rep_dict, test_case_src_dir, test_case_rep_dir,list_1,test_log_stream)

    assert type(rep_dict) == dict
    
    

def test_update_files_copies_new_file(capfd):
    test_case_dir = os.path.join(test_dir, "test_sync", 'test_update_files_fn_0')
    test_case_src_dir = os.path.join(test_case_dir, "src")
    test_case_rep_dir = os.path.join(test_case_dir, "rep")
    test_log_file = os.path.join(test_case_dir, "log.txt")
    if not os.path.exists(test_case_src_dir):
        os.makedirs(test_case_src_dir)
    if not os.path.exists(test_case_rep_dir):
        os.makedirs(test_case_rep_dir)
    if not os.path.exists(test_log_file):
        with open(test_log_file, 'w') as f:
            f.write("")
    test_log_stream = open(test_log_file, 'a')
    #Create a new file in the src dir that does not exist in the rep directory
    files_src = [os.path.join(test_case_src_dir, "test_file_0.txt")]
    #Create the dictionary represesting src dir
    src_dict = write_files_and_compute_hash({}, files_src, files_src)
    #Rep directory intialised as empty
    rep_dict = {}

    #Since above test passed we know that get changes will return the correct list 1
    list_1, list_2, list_3 = sync.get_changes(src_dict, rep_dict)
    #call update files and check that it returns a dictionary 
    rep_dict = sync.update_files(src_dict, rep_dict, test_case_src_dir, test_case_rep_dir,list_1,test_log_stream)

    #update files should have updated both the rep_dict and the actual directory
    #we will check that both are equal to each other and that they are equal to the source
    assert rep_dict == src_dict
    #Scan the src folder because file names referece the src in rep dict
    assert rep_dict == sync.scan_folder(test_case_src_dir)
    #Not best practice to test multiple things in one case but 
    #to avoid repeating setup code I will also test that logs are correct here
    out,err = capfd.readouterr()
    assert f"Copied {files_src[0]} to " in out
    
def test_update_files_updates_edited_file(capfd):
    #since get changes passed above we can reuse the code from that test to 
    #initialise the changes list here
    test_case_dir = os.path.join(test_dir, "test_sync", 'test_update_files_fn_2')
    test_case_src_dir = os.path.join(test_case_dir, "src")
    test_case_rep_dir = os.path.join(test_case_dir, "rep")
    test_log_file = os.path.join(test_case_dir, "log.txt")
    if not os.path.exists(test_case_src_dir):
        os.makedirs(test_case_src_dir)
    if not os.path.exists(test_case_rep_dir):
        os.makedirs(test_case_rep_dir)
    #initialise a log file for this test
    if not os.path.exists(test_log_file):
        with open(test_log_file, 'w') as f:
            f.write("")
    test_log_stream = open(test_log_file, 'a')
    #Both source and replica folders will have the same file names
    files_src = [os.path.join(test_case_src_dir, "test_file_0.txt")]
    files_rep = [os.path.join(test_case_rep_dir, "test_file_0.txt")]

    #Write to the source and replica files
    src_dict = write_files_and_compute_hash({}, files_src, files_src)
    #True flag means that the content of the file in src and replica will be different
    rep_dict = write_files_and_compute_hash({}, files_rep, files_src, True)

    #Since file content is different the file name will be returned as the difference
    expected_ret = [files_src[0]]

    #list 2 will be passed to the update function
    list_1, list_2, list_3 = sync.get_changes(src_dict, rep_dict)

    rep_dict = sync.update_files(src_dict, rep_dict, test_case_src_dir, test_case_rep_dir,list_2,test_log_stream, True)

    #update files should have updated both the rep_dict and the actual directory
    #we will check that both are equal to each other and that they are equal to the source
    assert rep_dict == src_dict
    #Scan the src folder because file names referece the src in rep dict
    assert rep_dict == sync.scan_folder(test_case_src_dir)
    #Not best practice to test multiple things in one case but 
    #to avoid repeating setup code I will also test that logs are correct here
    out,err = capfd.readouterr()
    assert f"Updated value of {files_rep[0]} to match {files_src[0]}" in out

def test_delete_files_removes_deleted_file(capfd):
    #same as with last two we can use the setup from the comparison test 
    test_case_dir = os.path.join(test_dir, "test_sync", 'test_update_files_fn_3')
    test_case_src_dir = os.path.join(test_case_dir, "src")
    test_case_rep_dir = os.path.join(test_case_dir, "rep")
    test_log_file = os.path.join(test_case_dir, "log.txt")
    if not os.path.exists(test_case_src_dir):
        os.makedirs(test_case_src_dir)
    if not os.path.exists(os.path.join(test_case_rep_dir ,"test_sub_dir")):
        os.makedirs(os.path.join(test_case_rep_dir ,"test_sub_dir"))
          #initialise a log file for this test
    if not os.path.exists(test_log_file):
        with open(test_log_file, 'w') as f:
            f.write("")
    test_log_stream = open(test_log_file, 'a')
    
   
    files_src = [ os.path.join(test_case_src_dir, "test_file_0.txt")]
    files_rep = [os.path.join(test_case_rep_dir, "test_file_0.txt"), os.path.join(test_case_rep_dir ,"test_sub_dir", "test_file_1.txt")]
    #create src ref for deleted file
    files_src_ref = [os.path.join(test_case_src_dir, "test_file_0.txt") ,os.path.join(test_case_src_dir ,"test_sub_dir", "test_file_1.txt")]
    
    
    
    #manually create files and sub directories and create state dict
    src_dict = write_files_and_compute_hash({},files_src, files_src_ref)

    #Create Replica Folder with additional files 
    # keys reference src folder
    # Additional files emulate deleting files in src folder
    rep_dict = write_files_and_compute_hash({}, files_rep, files_src_ref)
    
    #File ref in position 1 does not exist in original array so should be returned
    expected_ret = [files_src_ref[1]]
    list_1, list_2, list_3 = sync.get_changes(src_dict, rep_dict)
    rep_dict = sync.delete_files(rep_dict, test_case_src_dir, test_case_rep_dir, list_3, test_log_stream)

    #we will check that both are equal to each other and that they are equal to the source
    assert rep_dict == src_dict
    #Scan the src folder because file names referece the src in rep dict
    assert rep_dict == sync.scan_folder(test_case_src_dir)

    #Not best practice to test multiple things in one case but 
    #to avoid repeating setup code I will also test that logs are correct here
    out,err = capfd.readouterr()
    assert f"Deleted {files_rep[1]} from {test_case_rep_dir}" in out


def test_convert_keys_fn():
    test_case_dir = os.path.join(test_dir, "test_sync", 'test_convert_keys_fn_0')
    test_case_src_dir = os.path.join(test_case_dir, "src")
    test_case_rep_dir = os.path.join(test_case_dir, "rep")

    #create dummy file directories in replica folder
    rep_files = [os.path.join(test_case_rep_dir, 'file_0.txt'),os.path.join(test_case_rep_dir, 'file_1.txt'),os.path.join(test_case_rep_dir, 'file_2.txt')]
    rep_dict = {}
    #populate replica dictionary with dummy hash values
    for i, file in enumerate(rep_files):
        rep_dict[file] = {12345 + i}
    
    #do the same for the source folder
    src_files = [os.path.join(test_case_src_dir, 'file_0.txt'),os.path.join(test_case_src_dir, 'file_1.txt'),os.path.join(test_case_src_dir, 'file_2.txt')]
    src_dict = {}
    for i, file in enumerate(src_files):
        src_dict[file] = {12345 + i}

    assert src_dict == sync.convert_keys(rep_dict, test_case_rep_dir, test_case_src_dir)