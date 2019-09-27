# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 23:38:13 2018

@author: lavee
"""

import os
import pandas as pd
import fnmatch

def create_index_file(rootdir, groundTruth):
    for dirs, subdirs, files in os.walk(rootdir+groundTruth):
        #print("here " + dirs)
        #print(subdirs)
        
        for s in subdirs:
                working_dir = rootdir + groundTruth + "/" + s + "/fork"
         #       print(working_dir)
                for f in os.listdir(working_dir):
                    working_file = working_dir + "/" + f
                    writing_file = rootdir +myoData + "/" + s + "/fork" + "/write" + s
                    with open(writing_file,'w+') as fwrite:
                        with open(working_file,'r') as fopen:
                             for x in fopen:
                                if len(x.split()) == 0:
                                    continue
                                split_x = x.split(",")
                                start = int(split_x[0])*50//30
                                end = int(split_x[1])*50//30
                                fwrite.write(str(start) + " , " + str(end) + "\n")
                    break
        break


def create_eating_noneating(rootdir, myoData):
        for dirs, subdirs, files in os.walk(rootdir + myoData):
            for s in subdirs:
                    working_dir = rootdir + myoData + "/" + s + "/fork"
                    for f in os.listdir(working_dir):
                        if(fnmatch.fnmatch(f,'*_IMU.txt')):
                            working_file = working_dir + "/" + f
                            data_file = pd.read_csv(working_file, header = None, encoding = "utf-8")
                        
                            eating_file = working_dir + "/eating_" + s
                            
                            noneating_file = working_dir + "/noneating_" + s
                        if(fnmatch.fnmatch(f,'write*')):
                            index_f = working_dir + "/write" + s
                            index_file = pd.read_csv(index_f,header = None, sep =',')
                            
                        
                    eating_df = pd.DataFrame()    
                    noneating_start = 0
                                        
                    for index,row in index_file.iterrows():
                        
                        noneating_end = row[0]-1 
                        
                        eating_df = pd.DataFrame()    
                        eating_df = eating_df.append(data_file[row[0]:row[1]])
                        if(eating_df.shape[0]!=0):
                            eating_df.to_csv(eating_file + "_" + str(row[0]) + "_" + str(row[1]) + ".csv",sep=',',index=False,header=False)   
                        
                        
                        noneating_df = pd.DataFrame()    
                        noneating_df = noneating_df.append(data_file[noneating_start:noneating_end])
                        if(noneating_df.shape[0]!=0):
                            noneating_df.to_csv(noneating_file + "_" + str(noneating_start) + "_" + str(noneating_end) + ".csv",sep=',',index=False,header=False)   
                        
                        noneating_start = row[1]+1
                    
                    noneating_df = pd.DataFrame()    
                    noneating_df = noneating_df.append(data_file[noneating_start:])
                    if(noneating_df.shape[0]!=0):
                        noneating_df.to_csv(noneating_file + "_" + str(noneating_start) + "_end" + ".csv",sep=',',index=False,header=False)   
                    
                    noneating_start = row[1]+1        
                
                    #noneating_df = pd.concat([data_file, eating_df]).drop_duplicates(keep=False)
                        
                    #eating_df.to_csv(eating_file,sep=',',index=False,header=False)   
                    #noneating_df.to_csv(noneating_file,sep=',',index=False,header=False)   
                       
            break 
        
def create_test_and_training(rootdir, myoData):
        for dirs, subdirs, files in os.walk(rootdir + myoData):
            for s in subdirs:
                    working_dir = rootdir + myoData + "/" + s + "/fork"
                    for f in os.listdir(working_dir):
                        if(fnmatch.fnmatch(f,'eating_'+s)):
                            working_file = working_dir + "/" + f
                            
                            data_file = pd.read_csv(working_file, header = None, encoding = "utf-8")
                        
                            no_of_records = data_file.shape[0]
                            
                            training_records = int(0.6*no_of_records)
                            test_records= no_of_records - training_records
                            
                            #print(training_records)
                            #print(test_records)
                            
                            training_data = data_file[0:training_records]
                            test_data = data_file[training_records+1:]
                            
                            training_data.to_csv(working_file + "_training")
                            test_data.to_csv(working_file + "_test")
                        if(fnmatch.fnmatch(f,'noneating_'+s)):
                            working_file = working_dir + "/" + f
                            
                            data_file = pd.read_csv(working_file, header = None, encoding = "utf-8")
                        
                            no_of_records = data_file.shape[0]
                            
                            training_records = int(0.6*no_of_records)
                            test_records= no_of_records - training_records
                            
                            #print(training_records)
                            #print(test_records)
                            
                            training_data = data_file[0:training_records]
                            test_data = data_file[training_records+1:]
                            
                            training_data.to_csv(working_file + "_training",index=False,header=False)
                            test_data.to_csv(working_file + "_test",index=False,header=False)
                       
            break 

        
if __name__ == '__main__':
    rootdir = './'
    groundTruth = "/groundTruth"
    myoData = "/MyoData"
    
    create_index_file(rootdir, groundTruth)
    print("fetched indexes")
    create_eating_noneating(rootdir, myoData)
    print("separated eating and non eating data")
    


