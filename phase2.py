# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 16:06:03 2018

@author: lavee
"""
from sklearn.decomposition import PCA
import fnmatch
import pandas as pd
import  numpy as np
import os
from sklearn.tree import DecisionTreeClassifier as dst
from sklearn.metrics import precision_recall_fscore_support as prf
from sklearn import svm
from sklearn.neural_network import MLPClassifier

def apply_pca(rootdir, myoData):
     for dirs, subdirs, files in os.walk(rootdir+groundTruth):
        #print("here " + dirs)
        #print(subdirs)
        
            for s in subdirs:
                    working_dir = rootdir + myoData + "/" + s + "/fork"
                    for f in os.listdir(working_dir):
                        
                        if(fnmatch.fnmatch(f,'featurematrix_eat_*.csv')):
                            working_file = working_dir + "/" + f
                            eating_df = pd.read_csv(working_file, encoding = "utf-8", header = None, sep = ',')
                            eating_df = eating_df.replace([np.inf, -np.inf], np.nan).fillna(0)
                            
                            eating_df = eating_df.values
                      #      print(eating_df.shape)        
                            eat_count = eating_df.shape[0]
                        if(fnmatch.fnmatch(f,'featurematrix_noneat_*.csv')):
                            working_file = working_dir + "/" + f
                            noneating_df = pd.read_csv(working_file, encoding = "utf-8", header = None, sep = ',')
                            noneating_df = noneating_df.replace([np.inf, -np.inf], np.nan).fillna(0)
                            
                            noneating_df = noneating_df.values
                            noneat_count = noneating_df.shape[0]
                            
                    combined_df = np.vstack((eating_df,noneating_df))        
                    print(combined_df.shape)        
                    pca = PCA(n_components = 15)
                    pca.fit(combined_df)
                    print(s)
                    combined_df = pca.transform(combined_df)
                    print(combined_df.shape)
                    
                    np.savetxt(working_dir+"/reducedfeaturematrix_eat_" + s + ".csv", combined_df[0:eat_count,:], delimiter=",")
                    np.savetxt(working_dir+"/reducedfeaturematrix_noneat_" + s + ".csv", combined_df[eat_count+1:,:], delimiter=",")
                            
                           
                            
                    
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

def apply_classifiers(rootdir, myoData):
    for dirs, subdirs, files in os.walk(rootdir+groundTruth):
        
            for s in subdirs:
                    working_dir = rootdir + myoData + "/" + s + "/fork"
                    for f in os.listdir(working_dir):
                        
                        if(fnmatch.fnmatch(f,'reducedfeaturematrix_eat_*.csv')):
                            working_file = working_dir + "/" + f
                            eating_df = pd.read_csv(working_file, encoding = "utf-8", header = None, sep = ',')
                            eating_df = eating_df.replace([np.inf, -np.inf], np.nan).fillna(0)
                            
                            eating_df = eating_df.values
                      #      print(eating_df.shape)        
                            eat_count = eating_df.shape[0]
                        if(fnmatch.fnmatch(f,'reducedfeaturematrix_noneat_*.csv')):
                            working_file = working_dir + "/" + f
                            noneating_df = pd.read_csv(working_file, encoding = "utf-8", header = None, sep = ',')
                            noneating_df = noneating_df.replace([np.inf, -np.inf], np.nan).fillna(0)
                            
                            noneating_df = noneating_df.values
                            #noneat_count = noneating_df.shape[0]
                            
                    noTr_eat = int(len(eating_df)*0.6)
                    noTe_eat = len(eating_df) - noTr_eat
                    noTr_noneat = int(len(noneating_df)*0.6)
                    noTe_noneat = len(noneating_df) - noTr_noneat
                    
                    train_eat = eating_df[:noTr_eat , :]
                    train_noneat = noneating_df[:noTe_noneat , :]
                    test_eat = eating_df[noTr_eat: , :]
                    test_noneat = noneating_df[noTe_noneat: , :]
                    
                    train_data = np.vstack((train_eat,train_noneat))
                    test_data = np.vstack((test_eat, test_noneat))
                    
                    labels_tr_eat = np.full((1,train_eat.shape[0]),1).flatten()
                    labels_tr_noteat = np.full((1,train_noneat.shape[0]),0).flatten()
                    labels_train = np.hstack((labels_tr_eat,labels_tr_noteat))

                            
                    labels_te_eat = np.full((1,test_eat.shape[0]),1).flatten()
                    labels_te_noteat = np.full((1,test_noneat.shape[0]),0).flatten()
                    labels_test = np.hstack((labels_te_eat,labels_te_noteat))
                    
                
                    #print(labels_train)
                
###DST CLASSIFICATION STARTS HERE##########                
                    dst_clf = dst()
                    dst_clf = dst_clf.fit(train_data,labels_train)

                    labels_predicted = dst_clf.predict(test_data)

                    
                    #print(labels_predicted)
                    pre, re, f, x = prf(labels_test,labels_predicted, average = 'macro' )
                    dst_metrics = []
                    dst_metrics.append(['Precision',pre])
                    dst_metrics.append(['Recall',re])
                    dst_metrics.append(['F1 score',f])
                    
#                    print(s)
#                    print(pre, end = ' ')
#                    print(re, end = ' ')
#                    print(f)
                    final_metrics_dst = working_dir + "/dst_precision_recall_f1.csv"
                    with open(final_metrics_dst, 'w') as file_handler:
                            for item in dst_metrics:
                                file_handler.write("{}\n".format(item))
                    print("dst metrics")
                    
###SVM CLASSIFICATION STARTS HERE##########          
                    svm_clf = svm.SVC(gamma=0.001)
                    svm_clf.fit(train_data,labels_train)
                            
                    labels_predicted_svm = svm_clf.predict(test_data)
                            
                
                    pre, re, f, x = prf(labels_test,labels_predicted_svm, average = 'macro' )
                    svm_metrics = []
                    svm_metrics.append(['Precision',pre])
                    svm_metrics.append(['Recall',re])
                    svm_metrics.append(['F1 score',f])
                    
#                    print(s)
#                    print(pre, end = ' ')
#                    print(re, end = ' ')
#                    print(f)
                    final_metrics_svm = working_dir + "/svm_precision_recall_f1.csv"
                    with open(final_metrics_svm, 'w') as file_handler:
                            for item in svm_metrics:
                                file_handler.write("{}\n".format(item))
                    print("svm metrics")
                    
###SVM CLASSIFICATION STARTS HERE##########          
                    nn_clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(5, 2), random_state=1)
                    nn_clf.fit(train_data,labels_train)
                            
                    labels_predicted_nn = nn_clf.predict(test_data)
                            
                
                    pre, re, f, x = prf(labels_test,labels_predicted_nn, average = 'macro' )
                    nn_metrics = []
                    nn_metrics.append(['Precision',pre])
                    nn_metrics.append(['Recall',re])
                    nn_metrics.append(['F1 score',f])
                    
#                    print(s)
#                    print(pre, end = ' ')
#                    print(re, end = ' ')
#                    print(f)
                    final_metrics_nn = working_dir + "/nn_precision_recall_f1.csv"
                    with open(final_metrics_nn, 'w') as file_handler:
                            for item in nn_metrics:
                                file_handler.write("{}\n".format(item))
                    
                    print("nn metrics")
            break
    

if __name__ == '__main__':
    rootdir = './'
    groundTruth = "/groundTruth"
    myoData = "/MyoData"
    
    apply_pca(rootdir, myoData)

    apply_classifiers(rootdir, myoData)
    
    #create_test_and_training(rootdir, myoData)
    #print("separated testing and training data")


