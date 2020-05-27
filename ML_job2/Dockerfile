FROM centos
RUN yum install epel-release -y
RUN yum -y install gcc gcc-c++ python3-pip python3-devel atlas atlas-devel gcc-gfortran openssl-devel libffi-devel
RUN pip3 install PyYAML
RUN pip3 install scikit-learn
RUN pip3 install numpy
RUN pip3 install pandas
RUN mkdir workspace/
RUN yum install git -y
WORKDIR /workspace/
RUN mkdir dataset/
RUN mkdir saved_models/
