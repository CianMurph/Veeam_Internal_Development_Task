## Technical Assignment for Internal Development Team
----------

### Overview
----------


This repository contains my solution to the problem proposed by Veeam as part of the recruitment process for the rol of QA Automation Engineer.
The specifications for this program can be found in the [Specifications.pdf](./Specifications.pdf) file in this directory.

The program performs a one way synchronisation between a specified source folder and a specified replia folder, synchronisation is performed periodically at a user defined interval measured in seconds. Logs are written to the command line and to a log file specified by the user.

The program can be used via the command line where the user can enter the path to the source folder, replica folder, log file and a synchronisation interval in seconds.

### Motivation
----------

The assignment was completed using Python. 
I chose Python for this assignment as it offers high-level abstractions and dynamic typing that reduces the amount of code needed to complete the same task as compared to C++ or C#. Python has an extensive set of built-in libraries, including utility functions that significantly speed up development. While Python's execution time is generally slower than C++ or C#, it is more than sufficient for this assignment, where code execution occurs periodically. Moreover, Python's garbage collector automatically manages memory, allowing developers to focus more on application logic rather than memory allocation and deallocation. This feature, combined with Python's ease of use, makes it a better choice for rapidly prototyping and developing simple programs.

### Tech Stack
----------

This project was written with python version 3.10.11\
Pip is used to manage dependencies\
Pytest is used to run tests

### Install
----------

In order to use this program you must install python 3 and pip on your device. For information on how to install python on your specific device please refer to the offical documentation [here](https://docs.python.org/3/using/index.html)

Once you have python installed you can use this program by pulling this repository to your local device.

It is recommended that you use a python virtual environment to run this program. To setup and activate a virtual environment navigate to the root of this repository on your local device and enter the following commands:

##### Windows
`python -m venv venv`\
`.\venv\scripts\activate`

##### Unix
`sudo apt-get install python3-venv`\
`python3 -m venv venv\n`\
`source venv/bin/activate`

For both windows and Unix you can exit the cirtual environment by entering the following line into your terminal:
`deactivate`

Now you can install the dependencies for this project by typing the following lines into your terminal:
`pip install -r requirements.txt`

These requirements are only necessary if you want to run the tests located in the tests subdirectory. The main program relies only on libraries that are included in the python standard library.

### Usage
----------
Once python and the project are installed then you are ready to run the program. To do so enter the following command into the command line from the root folder\
`python veeam/main.py [path_to_source_folder] [path_to_replica_folder] [path_to_log_file] [synchronisation_interval_in_seconds]`

To quickly test the functionality of the program you can use the sample folder located in the root of this repository. It contains a source folder, an empty replica folder and an empty log file. To run the program using these directories simply run the following command in the terminal from the root folder:\
`python3 veeam/main.py sample/src/ sample/replica/ sample/log.txt 30`

You can also run:\
`python veeam/main.py -h`\
To recieve a helper prompt.

The program expects absolute paths (from the root of your PC) to the source folder, replica folder and log file. It expects a positve whole number for the sync interval.
If any of the paths do not exist the program will exit and print out which argument needs to be entered properly. Enter a valid path and the program will run. 


### Testing
There are a number of unit tests in the tests subdirectory of this project. They test the functionality of the various functions used to read and verify user input and to synchronise the two folders. To run the tests pytest is required. Enter the following command in the root directory to run the tests.\
`pytest`
