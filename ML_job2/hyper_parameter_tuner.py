#!/usr/bin/python3

import yaml
import re

def tuned_file_constructor(dir_path,counter,config):
        with open(dir_path+'new_file.py','w') as new_file:
            with open(dir_path+'test_model.py','r') as old_file:
                for key in config['HyperParameter'].keys():
                    # Change the hyper parameters
                    print("key:",key)
                    change_this_line=""
                    for line in old_file:
                        if 'S'+key not in line:
                            new_file.writelines(line)
                            continue
                        else:
                            new_file.writelines('\n')
                            break
                    for line in old_file:
                        if 'E'+key not in line:
                            print(line)
                            change_this_line+=line
                        else:
                            break
                    new_file.writelines(line_replacer(config,change_this_line,key))
                else:
                    # HyperParameters changed
                    # therefore copying the rest of code as it is
                    new_file.write(old_file.read())
                    new_file.writelines(construct_stats(config, counter))
                old_file.close()
            new_file.close()

            
def line_replacer(config,change_this_line,key):
    """This function return the replaced hyperparameter line"""
    for arg in config['HyperParameter'][key]: 
        pattern=r'{}[ ]*=.*,'.format(arg)
        replace_value=config['HyperParameter'][key][arg][counter]
        if type(replace_value) is str:
            replace_value="'"+replace_value+"'"
        change_this_line=re.sub(pattern,"{}= {},".format(arg,replace_value),change_this_line)
        return change_this_line
    
def construct_stats(config, counter):
    """This function returns the lines that let us maintain the database(accuracy with hyper parameter)"""
    hyp_para_parsing=""
    for param in config['HyperParameter']:
        hyp_para_parsing=hyp_para_parsing+param+":- "
        for sub_variable in config['HyperParameter'][param]:
            hyp_para_parsing+=sub_variable+": "+str(config['HyperParameter'][param][sub_variable][counter])+" , "
        hyp_para_parsing+='  |  '
    cnn_lines="""
import csv
with open('/workspace/saved_models/stats_{3}.csv','a') as stats_file:
    additional_data= dict()
    additional_data['accuracy']= str({0})
    additional_data['stats_name']='{3}'
    additional_data['HyperParameter']="{1}"
    additional_data['Serial_No']={2}
    writer=csv.DictWriter(stats_file,fieldnames=[f_name for f_name in additional_data], delimiter= ':')
    if additional_data['Serial_No']==0:
        writer.writeheader()
    writer.writerow(additional_data)

""".format(config['AccuracyVariable'],hyp_para_parsing,counter,config['Name'])
    if 'Kind' in config:
        if config['Kind']=="CNN":
            cnn_lines+="model.save('/workspace/saved_models/model_{}{}.h5')".format(config['Name'],counter)
    return cnn_lines

                        

import os
import sys
os.chdir('/workspace/{}'.format(sys.argv[2]))
yaml_file=open('config.yml')
config=yaml.load(yaml_file, Loader= yaml.FullLoader)
for counter in range(int(sys.argv[1]),config['Counter']):
    tuned_file_constructor('./',counter,config)
    os.system("chmod +x new_file.py")
    os.system("./new_file.py")
