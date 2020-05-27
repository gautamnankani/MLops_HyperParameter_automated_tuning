#!/usr/bin/python3

import re
import os
import subprocess

job1_directory='../'+'ML_job1'+'/'
sklearn_container_name='mlops_sklearn_con'
cnn_container_name='mlops_cnn_con'





config_file_location='../ML_job1/config.yml'
import yaml
yaml_file=open(config_file_location)
config=yaml.load(yaml_file)
yaml_file.close()


def find_files(job1_directory):
    """This function returns a list of absolute path of all files cloned in job1"""
    # list all the files cloned in job1
    file_and_dir=os.listdir(job1_directory)
    files=[]
    for file_name in file_and_dir:
        if os.path.isfile('{}{}'.format(job1_directory,file_name)):
            # making list of all files with there absolute path
            files.append(os.path.abspath(job1_directory+file_name))
    return files


def find_libraries(file_name):
    """This function takes the program(python) file path as input
    and Returns list of all libraries used in the program file"""
    libraries=[]
    with open(file_name,'r') as file:
        for line in file:
            if re.search(r'import', line):
                # serarch some common libraries from each line of code containing import word
                lib_found=re.search(r'keras|sklearn',line)
                if lib_found is not None:
                    libraries.append(lib_found.group())
    return libraries

def rerun_container():
    if not subprocess.getoutput("sudo docker ps | grep {}".format(container)):
        os.system("docker start {}".format(container))
    
    stats_file_location='../ML_job2/models/stats_{}.csv'.format(config['Name'])
    import pandas as pd
    dataset=pd.read_csv(stats_file_location,delimiter=':')
    
    starting_number= len(dataset)

    if starting_number < config['Counter']:
        os.system("docker exec {} ./{}/hyper_parameter_tuner.py {}".format(container, config['RepoName'], starting_number))
        rerun_container()


lib=[]
file_names=find_files(job1_directory)
for file_name in file_names:
    lib+= find_libraries(file_name)

if 'keras' in lib:
    container=cnn_container_name
if 'sklearn' in lib:
    container=sklearn_container_name

    


rerun_container()
