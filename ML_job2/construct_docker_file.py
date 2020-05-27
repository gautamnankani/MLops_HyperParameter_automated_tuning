#!/usr/bin/python3

import os
import re
import subprocess

################################# IMAGE NAMES
sklearn_image_name='mlops_sklearn'
cnn_image_name='mlops_cnn'

################################# Container Names
sklearn_container_name='mlops_sklearn_con'
cnn_container_name='mlops_cnn_con'

################################### VOLUMES
cnn_dataset="/root/Desktop/cnn_dataset"
sklearn_dataset="/root/Desktop/sklearn_dataset"
model_volume="/var/lib/jenkins/workspace/ML_job2/models"


################################### git repo

config_file_location='../ML_job1/config.yml'
import yaml
yaml_file=open(config_file_location)
config=yaml.load(yaml_file)


clone_directory= "/workspace/{}/".format(config['RepoName'])
clone_from= config['RepoURL']



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



def construct_dockerfile(libraries,file_names):
    """This function takes the libraries required as input
    and returns the string/Dockerfile content to make Dockerfile"""
    
    #Installing requirements to install python libraries
    docker_file="""FROM centos
RUN yum install epel-release -y
RUN yum -y install gcc gcc-c++ python3-pip python3-devel atlas atlas-devel gcc-gfortran openssl-devel libffi-devel
RUN pip3 install PyYAML"""
    
    # Installing python libraries
    if 'sklearn' in libraries:
        docker_file='\n'.join([docker_file,
            "RUN pip3 install scikit-learn",
            "RUN pip3 install numpy",
            "RUN pip3 install pandas"
            ])
    if 'keras' in libraries:
        docker_file='\n'.join([docker_file,
            "RUN pip3 install numpy",
            "RUN pip3 install Pillow",
            "RUN pip3 install tensorflow",
            "RUN pip3 install keras"
            ])

    # Adding working directory and files in container
    docker_file+="""
RUN mkdir workspace/
RUN yum install git -y
WORKDIR /workspace/
RUN mkdir dataset/
RUN mkdir saved_models/
"""
    return docker_file


def docker_image_present(lib):
    if 'keras' in lib:
        if cnn_image_name in subprocess.getoutput('docker images'):
            print("image already present")
            return True
        else:
            return False
    if 'sklearn' in lib:
        if sklearn_image_name in subprocess.getoutput('docker images'):
            print("image already present")
            return True
        else:
            return False



def launch_docker(image, container, dataset_volume):
    os.system("docker run -dit --name {} -v {}:/workspace/dataset -v {}:/workspace/saved_models {}".format(container, dataset_volume, model_volume, image))
    requirement_file= subprocess.getoutput("sudo docker exec {} ls {} | grep requirement".format(container,config['RepoName']))
    if requirement_file:
        os.system("sudo docker exec {} pip3 install -r {}{}".format(container,clone_directory, requirement_file))



def main(job1_directory):
    """Here we use the above function to construct Dockerfile 
    And also build and run the image if not present"""
    lib=[]
    file_names=find_files(job1_directory)
    for file_name in file_names:
        lib+= find_libraries(file_name)
    if not docker_image_present(lib):
        #now getting docker file as string
        dockerfile= construct_dockerfile(set(lib),file_names.copy())
        print("Your Docker File looks like: \n")
        print(dockerfile)
        #Now writing the dockerfile
        with open('Dockerfile','w') as file:
            file.write(dockerfile)
        if 'keras' in lib:
            os.system('docker build -t {} .'.format(cnn_image_name))
            launch_docker(cnn_image_name, cnn_container_name ,cnn_dataset)
        if 'sklearn' in lib:
            os.system('docker build -t {} .'.format(sklearn_image_name))
            launch_docker(sklearn_image_name, sklearn_container_name, sklearn_dataset)
        return 1
    else:
        print("image present hence returning 0")
        return 0
