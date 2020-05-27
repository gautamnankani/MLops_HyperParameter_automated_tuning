#!/usr/bin/python3

import os
import construct_docker_file  as maker
import subprocess
################################# IMAGE NAMES
sklearn_image_name='mlops_sklearn'
cnn_image_name='mlops_cnn'

################################# Container Names
sklearn_container_name='mlops_sklearn_con'
cnn_container_name='mlops_cnn_con'

################################### DATASET VOLUN=ME
cnn_dataset="/root/Desktop/cnn_dataset"
sklearn_dataset="/root/Desktop/sklearn_dataset"

##########################################
config_file_location='../ML_job1/config.yml'
import yaml
yaml_file=open(config_file_location)
config=yaml.load(yaml_file)

clone_directory= "./{}/".format(config['RepoName'])
clone_from= config['RepoURL']

lib=[]
file_names=maker.find_files('/var/lib/jenkins/workspace/'+'ML_job1'+'/')
for file_name in file_names:
        lib+= maker.find_libraries(file_name)
if 'keras' in lib:
        image=cnn_image_name
        container=cnn_container_name
        dataset=cnn_dataset
if 'sklearn' in lib:
        image=sklearn_image_name
        container=sklearn_container_name
        dataset=sklearn_dataset


if 'models' not in os.listdir('./'):
    os.mkdir('models')
# here pass the directory name containing code files i.e. job1 directory
# replace the 'ML_job1' with you job1 name according to question statement
if maker.main('../'+'ML_job1'+'/'):
    print("Done")
else:
    if container in subprocess.getoutput('sudo docker ps -a'):
        print("container is present but stopped")
        if container in subprocess.getoutput('sudo docker ps'):
            pass
        else:
            print("starting container")
            os.system('sudo docker start {}'.format(container))
        
        # Doing the setup for new push

        requirement_file= subprocess.getoutput("sudo docker exec {} ls {} | grep requirement".format(container,config['RepoName']))
        print(requirement_file)
        if requirement_file:
            os.system("sudo docker exec {} pip3 install -r {}{}".format(container,clone_directory, requirement_file))

    else:
        maker.launch_docker(image, container, dataset)
        
if subprocess.getoutput("sudo docker exec {} ls | grep {}".format(container, config['RepoName'])):
        
    os.system("sudo docker exec {} rm -rf {}".format(container, clone_directory))

os.system("sudo docker exec {} git clone {}".format(container,clone_from))


os.system("sudo docker cp hyper_parameter_tuner.py  {}:/workspace/{}/".format(container, config['RepoName']))
os.system("sudo docker exec {} chmod +x {}/hyper_parameter_tuner.py".format(container, config['RepoName']))
os.system("sudo docker exec {0} ./{1}/hyper_parameter_tuner.py 0 {1}".format(container,config['RepoName']))








