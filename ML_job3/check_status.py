#!/usr/bin/python3

config_file_location='../ML_job1/config.yml'



import yaml
yaml_file=open(config_file_location)
config=yaml.load(yaml_file)


stats_file_location='../ML_job2/models/stats_{}.csv'.format(config['Name'])

import pandas as pd
dataset=pd.read_csv(stats_file_location,delimiter=':')
maximum= -1
for x in range(config['Counter']):
    acc_data=dataset.accuracy[x]
    if type(acc_data) is str:
        acc=max(eval(acc_data))
    else:
        acc=acc_data
    if acc > maximum:
        index_no, maximum = x, acc


content= '\n'.join([str(dataset),
    "\nBest Perfmance at:",
    "\t Serial No.: "+str(index_no),
    "\t Accuracy:"+str(maximum),
    "\nBelow are all the parameters of best performance:\n",
    str(dataset.iloc[index_no])])

import mail_content
mail_content.mail(content)
print(content)



"""
print(dataset)
print("Best Perfmance at:")
print("\t Serial No.:",index_no)
print("\t No. of epochs:",epoch_no)
print("\t Accuracy:",maximum)
print("\nBelow are all the parameters of best performance:\n")
print(dataset.iloc[index_no])
"""
