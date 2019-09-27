classdef makeFeatureMatrix

    methods(Static)
        % Clear workspace
            function featureMatrix1 = make_feature_matrix(file_name, action)

                % Create this directory if there isn't one
                % Declare all global variables
                Fs = 50;
                T = 1/Fs;

                selectedActions = {'eatingIMU', 'noneatingIMU'};
                EAT_features = [2,3,4,5,6,8,9,10,11];
                %KEYBOARD_features = { 'gyroX', 'gyroZ', 'pitch' };
                %EAT_EMG_features = {'emg1', 'emg3', 'emg4'};
                %KEYBOARD_EMG_features = { 'emg1','emg3','emg4', 'emg6','emg8'};


                    %file name will be passed into the function
                    rawData = readtable(file_name);
                    %disp("Print raw_data")
                    %disp(rawData)
                    %action will be passed into the function call, IMU or EMG
                    L = height(rawData);
                    switch action
                        case 'IMU'
                            disp("inside switch case");
                            featureMatrix1 = [];
                            %if action is selectedEatFood1, use EAT_features
                            for feature = 1:length(EAT_features)
                                input = table2array(rawData(1:end, EAT_features(feature)));
                                %disp("print input")
                                %disp(input)

                                %apply FFT & pick 3 peak values
                                %disp("input")
                                %disp(input)
                                fftFeaturesValues = feature_functions.fftFeatures(input,L);
                                featureMatrix1 = cat(2, featureMatrix1, fftFeaturesValues');

                                %apply PSD & pick 3 peak values
                                psdFeaturesValues = feature_functions.psdFeatures(input);
                                featureMatrix1 = cat(2, featureMatrix1, psdFeaturesValues');

                                %apply DWT & pick 3 peak values
                                dwtFeaturesValues = feature_functions.dwtFeatures(input);
                                featureMatrix1 = cat(2, featureMatrix1, dwtFeaturesValues');

                                %calculate Mean for every choosed attributes  
                                meanValues = mean(input);
                                featureMatrix1 = cat(2, featureMatrix1, meanValues);

                                %calculate STD for every choosed attributes
                                stdValues = std(input);
                                featureMatrix1 = cat(2, featureMatrix1, stdValues);

                            end
                %         case {2,4,6,8}
                %             %if action is selectedEatFood_EMG, use EAT_EMG_features
                %             for feature = 1:length(EAT_EMG_features)
                %                 input = table2array(rawData(1:end, feature));
                %                 
                %                 %apply FFT & pick 3 peak values
                %                 fftFeaturesValues = fftFeatures(input,L);
                %                 featureMatrix1 = cat(2, featureMatrix1, fftFeaturesValues');
                %                 
                %                 %apply PSD & pick 3 peak values
                %                 psdFeaturesValues = psdFeatures(input);
                %                 featureMatrix1 = cat(2, featureMatrix1, psdFeaturesValues');
                %                 
                %                 %apply DWT & pick 3 peak values
                %                 dwtFeaturesValues = dwtFeatures(input);
                %                 featureMatrix1 = cat(2, featureMatrix1, dwtFeaturesValues');
                %                 
                %                 %calculate Mean for every choosed attributes  
                %                 meanValues = mean(input);
                %                 featureMatrix1 = cat(2, featureMatrix1, meanValues);
                %                 
                %                 %calculate STD for every choosed attributes
                %                 stdValues = std(input);
                %                 featureMatrix1 = cat(2, featureMatrix1, stdValues);
                %                 
                %             end
                            %xlswrite(strcat(char(selectedActions(action-1)),'_FeatureMatrix.xlsx'),featureMatrix1);
                            disp('EatFeatureMatrix is made')
                            disp(size(featureMatrix1))

                    end
            end






            % function which performs FFT and returns the top 3 peak values.
            
    end
end

