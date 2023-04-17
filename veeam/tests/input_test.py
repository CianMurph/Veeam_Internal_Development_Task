#unit tests for functions in cli directory
import pytest
import pathlib
import cli  
import os

def test_incorrect_input(capsys):
    #unit test for function called read
    #assert that a systemerror will occur if the function is called without arguments
    
    with pytest.raises(SystemExit): 
        cli.read()
        captured = capsys.readouterr()
        assert captured.err == "Error: No arguments provided"

def test_incorrect_input_2(capsys):
    #unit test for function called read
    #assert that a systemerror will occur if the function is called with less than 4 arguments
    
    with pytest.raises(SystemExit): 
        cli.read(["a","b","c"])
        captured = capsys.readouterr()
        assert captured.err == "Error: Not enough arguments provided"

def test_incorrect_input_3(capsys):
    #unit test for function called read
    #assert that a systemerror will occur if the function is called with more than 4 arguments
    
    with pytest.raises(SystemExit): 
        cli.read(["a","b","c","d","e"])
        captured = capsys.readouterr()
        assert captured.err == "Error: Too many arguments provided"

def test_incorrect_input_4(capsys):
    #unit test for function called read
    #assert that a systemerror will occur if the function is called with a non-integer for the sync interval
    
    with pytest.raises(SystemExit): 
        cli.read(["a","b","c","d"])
        captured = capsys.readouterr()
        assert captured.err == "Error: Interval must be an integer"

   

def test_correct_input():
    #Need to call the read function with values we know exist
    project_dir = str(pathlib.Path(__file__).parent.parent.resolve())
    source_dir = os.path.join(project_dir, "sample", "src")
    replica_dir = os.path.join(project_dir, "sample", "replica")
    log_file = os.path.join(project_dir, "sample", "log.text")
    interval = "10"
    #check that function returns correct values
    #The function should contain an argument parser with the passed values
    parsed = cli.read([source_dir, replica_dir, log_file, interval])
    result = vars(parsed)
    assert result["source_folder"] == source_dir
    assert result["replica_folder"] == replica_dir
    assert result["log_file"] == log_file
    assert result["sync_interval"] == int(interval)

def test_invalid_input_verfication(capfd):
    #unit test for function called verify
    #Function accepts args and verifies that they are valid
    args = cli.read(["a","b","c","10"])
    assert cli.verify(args) == False
    out,err = capfd.readouterr()
    print(out)
    print(err)
    assert "Please enter a valid path for the  source_folder" in out
    assert "Please enter a valid path for the  replica_folder" in out
    assert "Please enter a valid path for the  log_file" in out

    
    