
# Activity Recognition System

## Description
We use Myo armbands to capture Accelerometer, Gyroscope, Orientation and EMG data for daily actvities. We then extract features from that raw data, apply dimensionality reduction technqiues and then train classification models on that data in reduced dimensions to distinguish between eating and non-eating activities.

For feature extraction, we have used the following five feature extraction methods:

1. Mean
2. Standard Deviation
3. Max
4. Fast Fourier Transform
5. Discrete Wavelet Transform.
6. Power Spectral Density

#### Please note that we are using fork data in the eating dataset.

1. fetch_records.py: This program reads the ground_truth file for each user and separates the IMU file into eating and non-eating for each interval in the MtoData/user/fork directory with the name as eating_user<number>_<start_idx>_<end_index>.csv and noneating_user<number>_<start_idx>_<end_index>.csv

2. makeFeatureMatrixWrapper.m : Once this is done, we create a feature matrix with the fft, psd, dwt, mean, standard deviation of OrientationX, OrientationY, OrientationZ, OrientationW, AccelerometerX, AccelerometerZ, Gyroscope X, Gyroscope Y and Gyroscope Z.
This is done for each user and data is written in featurematrix_noneat_user<number>.csv and featurematrix_eat_user<number>.csv files in the same directory for each user. makeMakeMatrix.m and feature_functions.m are the helper programs.

3. phase2.py: In this program, first we apply PCA on the feature matrix, eating and non-eating to project the data on 15 dimensions.  Then we divide the eating data into 60% trainig data and 40% test data for each user. Similarly we divide the non-eating data.
Then, for each user, Decision Tree, Support Vector Machine and Neural Networks are trained with the training data, and used to predict the class labels for test data and then the accuracy is reported using Precision, Recall and F1 score metrics. The accuracy is reported in dst_precision_recall_f1.csv, svm_precision_recall_f1.csv, nn_precision_recall_f1.csv in the same directory.

4. phase3.py: In this program, first we apply PCA on the feature matrix, eating and non-eating to project the data on 15 dimensions.  Then we divide the eating data into 60% trainig data and 40% test data for each user. Similarly we divide the non-eating data.
Now, we use 60% of the 30 users as our training data. So all the eating and non-eating data of first 18 users is fed to DST, SVM, NN to train the classifiers and then these machines are used to predict the class labels for test data of each f teh rest of the users and then the accuracy is reported using Precision, Recall and F1 score metrics. The accuracy is reported in phase3_dst_precision_recall_f1.csv, phase3_svm_precision_recall_f1.csv, phase3_nn_precision_recall_f1.csv

Expected Directory Structure:

./groundTruth/user<number>/fork/<file> 
./MyoData/user<number>/fork/<file> 
./fetch_records.py 
./phase2.py 
./phase3.py 
./matlab/makeFeatureMatrixWrapper.m 
./matlab/makeMakeMatrix.m 
./matlab/feature_functions.m 

## Results

The original matrix after feature selection has total 99 features for eating data. This causes complexities in classification as the classifiers requires amount of data exponential to the number of features. With 15 principal components the PCA captures 98% variance in overall eating data.

In our training and testing for phase 2 and phase 3 using the fork data for all the users, the overall accuracy is better when each user is treated independently to train and test the models, as compared to using 60% of all users for training.

Also, for our data and experiments, DST outperforms the other two classifiers based on the accuracy measures.

