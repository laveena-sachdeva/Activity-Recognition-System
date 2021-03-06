% Clear workspace
clear; close all; clc;

% Declare all global variables
HIGHSTANDARD = 0.4;

actions = {'EAT', 'keyboard1'};
features = {'accX', 'accY', 'accZ', 'gyroX', 'gyroY', 'gyroZ', 'roll','pitch','yaw' };


% Calculate correaltion coefficient between each sensors for measuring
% similarity


for i = 1:length(actions)
    rawData = readtable(char(strcat(actions(i),'.csv')));
    for j = 1:length(features)-1
        for k = j+1:length(features)
            input_first = table2array(rawData(1:end, j));
            input_second = table2array(rawData(1:end, k));
            
            R = corrcoef(input_first,input_second);
            coeff = abs(R(1,2));
            
            if coeff > HIGHSTANDARD
              
                X = sprintf('%s action correlation of %s & %s  = %d, correaltion is so high. one of them will be deleted for making feature matrix ',char(strcat(actions(i))), char(strcat(features(j))),char(strcat(features(k))),coeff);
                disp(X)
            end
            
        end
    end
end


%result by extraction: 
%EAT features = {'accX', 'accY', 'accZ', 'gyroX','gyroZ', 'oriX', 'oriY'}
%KEYBOARD features = { 'gyroX', 'gyroZ', 'pitch'}

% we will make feature matrix from these features + emg features
